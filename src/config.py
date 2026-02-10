"""
Configuration management for the Voice Agent
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class LiveKitConfig(BaseModel):
    """LiveKit connection configuration"""
    url: str = Field(default_factory=lambda: os.getenv("LIVEKIT_URL", ""))
    api_key: str = Field(default_factory=lambda: os.getenv("LIVEKIT_API_KEY", ""))
    api_secret: str = Field(default_factory=lambda: os.getenv("LIVEKIT_API_SECRET", ""))

class DeepgramConfig(BaseModel):
    """Deepgram STT configuration"""
    api_key: str = Field(default_factory=lambda: os.getenv("DEEPGRAM_API_KEY", ""))
    model: str = "nova-2-general"
    language: str = "en-US"

class CartesiaConfig(BaseModel):
    """Cartesia TTS configuration"""
    api_key: str = Field(default_factory=lambda: os.getenv("CARTESIA_API_KEY", ""))
    model: str = "sonic-english"
    voice_id: str = "79a125e8-cd45-4c13-8a67-188112f4dd22"

class LLMConfig(BaseModel):
    """LLM configuration"""
    provider: str = Field(default="openai")
    model: str = Field(default="gpt-4o-mini")
    temperature: float = Field(default=0.7)
    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))

class SupabaseConfig(BaseModel):
    """Supabase database configuration"""
    url: str = Field(default_factory=lambda: os.getenv("SUPABASE_URL", ""))
    key: str = Field(default_factory=lambda: os.getenv("SUPABASE_KEY", ""))

class AgentConfig(BaseModel):
    """Main agent configuration"""
    name: str = Field(default_factory=lambda: os.getenv("AGENT_NAME", "SuperBryn Assistant"))
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    
    livekit: LiveKitConfig = Field(default_factory=LiveKitConfig)
    deepgram: DeepgramConfig = Field(default_factory=DeepgramConfig)
    cartesia: CartesiaConfig = Field(default_factory=CartesiaConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    supabase: SupabaseConfig = Field(default_factory=SupabaseConfig)
    
    def validate_required_keys(self) -> list[str]:
        """Validate that all required API keys are present"""
        missing = []
        
        if not self.livekit.api_key:
            missing.append("LIVEKIT_API_KEY")
        if not self.deepgram.api_key:
            missing.append("DEEPGRAM_API_KEY")
        if not self.cartesia.api_key:
            missing.append("CARTESIA_API_KEY")
        if not self.llm.api_key:
            missing.append(f"{self.llm.provider.upper()}_API_KEY")
        
        return missing
    
config = AgentConfig()