from typing import Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class AIModelType(Enum):
    GPT4 = "gpt-4"
    WHISPER = "whisper-1"
    CLAUDE = "claude-3-opus"
    CUSTOM = "custom"

class AgentConfiguration(BaseModel):
    model_type: AIModelType = Field(default=AIModelType.GPT4)
    api_key: str = Field(default="")
    max_tokens: int = Field(default=1000, ge=100, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    custom_endpoint: str = Field(default="")

class AgentManager:
    def __init__(self):
        self._agents: Dict[str, AgentConfiguration] = {}

    def add_agent(
        self, 
        name: str, 
        config: AgentConfiguration
    ) -> None:
        """Add a new AI agent configuration"""
        self._agents[name] = config

    def update_agent(
        self, 
        name: str, 
        updates: Dict[str, Any]
    ) -> None:
        """Update an existing agent's configuration"""
        if name not in self._agents:
            raise ValueError(f"Agent {name} not found")
        
        current_config = self._agents[name]
        for key, value in updates.items():
            setattr(current_config, key, value)

    def get_agent_config(self, name: str) -> AgentConfiguration:
        """Retrieve an agent's configuration"""
        return self._agents.get(name)

    def list_agents(self) -> Dict[str, AgentConfiguration]:
        """List all configured agents"""
        return self._agents
