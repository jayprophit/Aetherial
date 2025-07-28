# tests/test_core.py
import pytest
from core.engine import AIEngine
from security.auth import SecurityManager

@pytest.fixture
def ai_engine():
    config = {
        "openai_key": "test_key",
        "aws_key": "test_aws_key"
    }
    return AIEngine(config)

@pytest.fixture
def security_manager():
    return SecurityManager("test_secret")

class TestAIEngine:
    async def test_code_generation(self, ai_engine):
        prompt = "Create a simple API"
        code = await ai_engine.generate_code(prompt)
        assert code is not None
        
    async def test_self_improvement(self, ai_engine):
        await ai_engine.improve_self()
        assert len(ai_engine.improvement_history) > 0

class TestSecurity:
    def test_token_creation(self, security_manager):
        token = security_manager.create_token({"user_id": 1})
        assert token is not None

    def test_token_verification(self, security_manager):
        token = security_manager.create_token({"user_id": 1})
        payload = security_manager.verify_token(token)
        assert payload["user_id"] == 1
