from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
import importlib

class AIModelType(Enum):
    GPT4 = "gpt-4"
    WHISPER = "whisper-1"
    CLAUDE = "claude-3-opus"
    CUSTOM = "custom"

class AgentConfiguration(BaseModel):
    model_type: AIModelType
    api_key: str
    max_tokens: int = Field(default=1000, ge=100, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    language: str = "en"

class DynamicAgentFactory:
    _agent_registry: Dict[AIModelType, str] = {
        AIModelType.GPT4: "openai_agent.GPT4Agent",
        AIModelType.WHISPER: "whisper_agent.WhisperAgent",
        AIModelType.CLAUDE: "claude_agent.ClaudeAgent"
    }

    @classmethod
    def create_agent(
        cls, 
        config: AgentConfiguration
    ) -> Any:
        """
        Dynamically load and instantiate AI agents
        based on configuration
        """
        if config.model_type == AIModelType.CUSTOM:
            return cls._load_custom_agent(config)
        
        agent_path = cls._agent_registry.get(config.model_type)
        if not agent_path:
            raise ValueError(f"No agent found for {config.model_type}")
        
        module_name, class_name = agent_path.rsplit('.', 1)
        
        try:
            module = importlib.import_module(module_name)
            agent_class = getattr(module, class_name)
            
            return agent_class(
                api_key=config.api_key,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                language=config.language
            )
        except (ImportError, AttributeError) as e:
            raise RuntimeError(f"Failed to load agent: {e}")

    @staticmethod
    def _load_custom_agent(config: AgentConfiguration):
        """
        Support loading custom agent from user-provided path
        """
        # Placeholder for custom agent loading logic
        raise NotImplementedError("Custom agent loading not implemented")
