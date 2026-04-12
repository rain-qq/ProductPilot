"""
LLM服务 - 封装大语言模型调用
"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from typing import Dict, Any, Optional

from config.settings import settings
from loguru import logger


class LLMService:
    """LLM服务"""
    
    def __init__(self):
        self.openai_llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_base=settings.OPENAI_API_BASE
        )
        
        self.claude_llm = ChatAnthropic(
            model="claude-3-opus-20240229",
            temperature=0.7,
            anthropic_api_key=settings.ANTHROPIC_API_KEY
        ) if settings.ANTHROPIC_API_KEY else None
    
    def get_llm(self, provider: str = "openai"):
        """获取LLM实例"""
        if provider == "openai":
            return self.openai_llm
        elif provider == "claude" and self.claude_llm:
            return self.claude_llm
        else:
            logger.warning(f"Provider {provider} not available, using OpenAI")
            return self.openai_llm
    
    def get_embeddings(self):
        """获取Embedding模型"""
        return OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_base=settings.OPENAI_API_BASE
        )
