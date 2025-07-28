from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .services.agent_manager import DynamicAgentFactory
from .services.voice_service import MultiLanguageVoiceService
from .services.authentication import AuthenticationService

from .models.agent_config import AgentConfiguration, AIModelType

app = FastAPI(
    title="AI Virtual Assistant",
    description="Intelligent multi-agent virtual assistant"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/agents/configure")
async def configure_agent(
    config: AgentConfiguration, 
    current_user = Depends(AuthenticationService.get_current_user)
):
    """
    Configure and load a dynamic AI agent
    
    Args:
        config: Agent configuration details
        current_user: Authenticated user
    
    Returns:
        Configured agent instance
    """
    try:
        agent = DynamicAgentFactory.create_agent(config)
        return {"status": "success", "agent": str(agent)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/voice/transcribe")
async def transcribe_audio(
    audio_data: bytes, 
    language: str = "en",
    current_user = Depends(AuthenticationService.get_current_user)
):
    """
    Transcribe audio input using multi-language voice service
    
    Args:
        audio_data: Raw audio bytes
        language: Language code
        current_user: Authenticated user
    
    Returns:
        Transcribed text
    """
    voice_service = MultiLanguageVoiceService(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    voice_service.set_language(language)
    
    transcription = voice_service.transcribe(audio_data)
    return {"transcription": transcription}
