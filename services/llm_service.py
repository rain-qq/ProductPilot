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
        # OpenAI LLM
        self.openai_llm = None
        if settings.OPENAI_API_KEY:
            try:
                self.openai_llm = ChatOpenAI(
                    model="gpt-4",
                    temperature=0.7,
                    openai_api_key=settings.OPENAI_API_KEY,
                    openai_api_base=settings.OPENAI_API_BASE
                )
                logger.info("OpenAI LLM initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI LLM: {e}")
        
        # Gemini LLM
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
    
    def get_llm(self, provider: str = "auto"):
        """
        获取LLM实例
        
        Args:
            provider: 选择的提供商 ("openai" / "gemini" / "claude" / "auto")
                     "auto" 会自动选择第一个可用的
            
        Returns:
            LLM实例
        """
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
            # 自动选择第一个可用的
            if self.openai_llm:
                logger.info("Auto-selected OpenAI LLM")
                return self.openai_llm
            elif self.gemini_llm:
                logger.info("Auto-selected Gemini LLM")
                return self.gemini_llm
            elif self.claude_llm:
                logger.info("Auto-selected Claude LLM")
                return self.claude_llm
            else:
                raise ValueError("No LLM available. Please configure at least one API key in .env")
        
        else:
            raise ValueError(f"Unknown provider: {provider}. Use 'openai', 'gemini', 'claude', or 'auto'")
    
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
