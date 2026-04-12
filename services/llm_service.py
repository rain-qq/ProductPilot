"""
LLM服务 - 封装大语言模型调用
支持 OpenAI、Gemini、Claude 等多种模型
"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any, Optional

from config.settings import settings
from loguru import logger


class LLMService:
    """LLM服务 - 支持多种LLM提供商"""
    
    def __init__(self):
        # OpenAI LLM (用于产品分析、提示词工程、质量审核等文本任务)
        self.openai_llm = None
        if settings.OPENAI_API_KEY:
            try:
                self.openai_llm = ChatOpenAI(
                    model=settings.OPENAI_MODEL,
                    temperature=0.7,
                    openai_api_key=settings.OPENAI_API_KEY,
                    openai_api_base=settings.OPENAI_API_BASE
                )
                logger.info(f"OpenAI LLM initialized successfully (model: {settings.OPENAI_MODEL})")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI LLM: {e}")
        
        # Gemini LLM (通用文本任务)
        self.gemini_llm = None
        if settings.GOOGLE_API_KEY:
            try:
                self.gemini_llm = ChatGoogleGenerativeAI(
                    model=settings.GEMINI_MODEL,
                    temperature=0.7,
                    google_api_key=settings.GOOGLE_API_KEY
                )
                logger.info(f"Gemini LLM initialized successfully (model: {settings.GEMINI_MODEL})")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini LLM: {e}")
        
        # Gemini Image LLM (专门用于图片生成)
        self.gemini_image_llm = None
        if settings.GOOGLE_API_KEY:
            try:
                self.gemini_image_llm = ChatGoogleGenerativeAI(
                    model=settings.GEMINI_IMAGE_MODEL,
                    temperature=0.7,
                    google_api_key=settings.GOOGLE_API_KEY
                )
                logger.info(f"Gemini Image LLM initialized successfully (model: {settings.GEMINI_IMAGE_MODEL})")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini Image LLM: {e}")
        
        # Claude LLM
        self.claude_llm = None
        if settings.ANTHROPIC_API_KEY:
            try:
                self.claude_llm = ChatAnthropic(
                    model="claude-3-opus-20240229",
                    temperature=0.7,
                    anthropic_api_key=settings.ANTHROPIC_API_KEY
                )
                logger.info("Claude LLM initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Claude LLM: {e}")
    
    def get_llm(self, provider: str = "auto", use_case: str = "text"):
        """
        获取LLM实例
        
        Args:
            provider: 选择的提供商 ("openai" / "gemini" / "gemini_image" / "claude" / "auto")
                     "auto" 会根据用例自动选择
            use_case: 使用场景 ("text" / "image")
                     - "text": 文本任务（产品分析、提示词工程等）
                     - "image": 图片生成任务
            
        Returns:
            LLM实例
        """
        # 如果明确指定了 gemini_image，直接返回
        if provider == "gemini_image":
            if not self.gemini_image_llm:
                raise ValueError("Gemini Image LLM not initialized. Please check GOOGLE_API_KEY in .env")
            return self.gemini_image_llm
        
        # 如果是图片生成用例且未指定provider，优先使用 Gemini Image
        if provider == "auto" and use_case == "image":
            if self.gemini_image_llm:
                logger.info("Auto-selected Gemini Image LLM for image generation")
                return self.gemini_image_llm
            elif self.gemini_llm:
                logger.info("Gemini Image LLM not available, falling back to Gemini LLM")
                return self.gemini_llm
            else:
                raise ValueError("No Gemini LLM available for image generation")
        
        # 原有的逻辑处理其他情况
        if provider == "openai":
            if not self.openai_llm:
                raise ValueError("OpenAI LLM not initialized. Please check OPENAI_API_KEY in .env")
            return self.openai_llm
        
        elif provider == "gemini":
            if not self.gemini_llm:
                raise ValueError("Gemini LLM not initialized. Please check GOOGLE_API_KEY in .env")
            return self.gemini_llm
        
        elif provider == "claude":
            if not self.claude_llm:
                raise ValueError("Claude LLM not initialized. Please check ANTHROPIC_API_KEY in .env")
            return self.claude_llm
        
        elif provider == "auto":
            # 自动选择第一个可用的（文本任务）
            if self.openai_llm:
                logger.info("Auto-selected OpenAI LLM for text tasks")
                return self.openai_llm
            elif self.gemini_llm:
                logger.info("Auto-selected Gemini LLM for text tasks")
                return self.gemini_llm
            elif self.claude_llm:
                logger.info("Auto-selected Claude LLM for text tasks")
                return self.claude_llm
            else:
                raise ValueError("No LLM available. Please configure at least one API key in .env")
        
        else:
            raise ValueError(f"Unknown provider: {provider}. Use 'openai', 'gemini', 'gemini_image', 'claude', or 'auto'")
    
    def get_embeddings(self, provider: str = "openai"):
        """获取Embedding模型"""
        if provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OpenAI API key not configured")
            return OpenAIEmbeddings(
                openai_api_key=settings.OPENAI_API_KEY,
                openai_api_base=settings.OPENAI_API_BASE
            )
        else:
            raise ValueError(f"Embeddings not supported for provider: {provider}")
    
    def get_available_providers(self) -> list:
        """获取可用的LLM提供商列表"""
        providers = []
        if self.openai_llm:
            providers.append("openai")
        if self.gemini_llm:
            providers.append("gemini")
        if self.claude_llm:
            providers.append("claude")
        return providers
