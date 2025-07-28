import speech_recognition as sr
import openai
from typing import Optional

class VoiceInteractionService:
    def __init__(
        self, 
        openai_api_key: str, 
        model: str = "whisper-1"
    ):
        self.recognizer = sr.Recognizer()
        openai.api_key = openai_api_key
        self.transcription_model = model

    def listen(self, timeout: int = 5) -> Optional[str]:
        """
        Capture audio input from microphone
        
        Args:
            timeout (int): Maximum listening time in seconds
        
        Returns:
            Optional transcribed text
        """
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=timeout)
                return self._transcribe_audio(audio)
            except sr.WaitTimeoutError:
                return None

    def _transcribe_audio(self, audio) -> str:
        """
        Transcribe captured audio using OpenAI Whisper
        
        Args:
            audio: Audio data from speech recognizer
        
        Returns:
            Transcribed text
        """
        try:
            # Convert audio to compatible format
            audio_data = audio.get_wav_data()
            
            # Use OpenAI Whisper for transcription
            transcription = openai.Audio.transcribe(
                model=self.transcription_model,
                file=audio_data
            )
            return transcription['text']
        
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""
