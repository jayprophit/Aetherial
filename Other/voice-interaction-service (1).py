import speech_recognition as sr
import openai
from typing import Dict, Optional, Tuple
from enum import Enum

class VoiceProcessingStatus(Enum):
    LISTENING = "listening"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"

class MultiLanguageVoiceService:
    SUPPORTED_LANGUAGES = {
        "en": "English",
        "es": "Spanish", 
        "fr": "French",
        "de": "German",
        "zh": "Chinese"
    }

    def __init__(
        self, 
        openai_api_key: str, 
        default_language: str = "en"
    ):
        self.recognizer = sr.Recognizer()
        openai.api_key = openai_api_key
        self.current_language = default_language

    def set_language(self, language_code: str):
        """Set active language for voice interactions"""
        if language_code not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language_code}")
        self.current_language = language_code

    def listen(
        self, 
        timeout: int = 5
    ) -> Tuple[VoiceProcessingStatus, Optional[str]]:
        """
        Enhanced voice capture with multi-language support
        
        Returns:
            Tuple of (processing status, transcribed text)
        """
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Real-time status update
                yield VoiceProcessingStatus.LISTENING, None
                
                audio = self.recognizer.listen(source, timeout=timeout)
                transcription = self._transcribe_audio(audio)
                
                yield (
                    VoiceProcessingStatus.COMPLETED 
                    if transcription 
                    else VoiceProcessingStatus.ERROR,
                    transcription
                )
        
        except Exception as e:
            yield VoiceProcessingStatus.ERROR, str(e)

    def _transcribe_audio(self, audio) -> Optional[str]:
        """
        Transcribe audio with language-specific configuration
        """
        try:
            transcription = openai.Audio.transcribe(
                model="whisper-1",
                file=audio.get_wav_data(),
                language=self.current_language
            )
            return transcription['text']
        
        except Exception as e:
            print(f"Transcription error: {e}")
            return None

    @classmethod
    def get_supported_languages(cls) -> Dict[str, str]:
        """Retrieve supported language mappings"""
        return cls.SUPPORTED_LANGUAGES
