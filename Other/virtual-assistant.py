# assistant/
#   __init__.py
#   config.py
#   core.py
#   handlers/
#     __init__.py
#     speech.py
#     search.py
#     media.py
#     communication.py
#     scheduling.py

# config.py
from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_load_dotenv

@dataclass
class Config:
    """Configuration settings for the virtual assistant."""
    OPENAI_API_KEY: str
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    WEATHER_API_KEY: str
    TWILIO_SID: str
    TWILIO_AUTH_TOKEN: str
    
    @classmethod
    def from_env(cls):
        """Load configuration from environment variables."""
        load_dotenv()
        return cls(
            OPENAI_API_KEY=os.getenv('OPENAI_API_KEY'),
            EMAIL_ADDRESS=os.getenv('EMAIL_ADDRESS'),
            EMAIL_PASSWORD=os.getenv('EMAIL_PASSWORD'),
            WEATHER_API_KEY=os.getenv('WEATHER_API_KEY'),
            TWILIO_SID=os.getenv('TWILIO_SID'),
            TWILIO_AUTH_TOKEN=os.getenv('TWILIO_AUTH_TOKEN')
        )

# handlers/speech.py
import speech_recognition as sr
import pyttsx3
from typing import Optional
import logging

class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self._configure_speech_engine()
    
    def _configure_speech_engine(self):
        """Configure text-to-speech engine settings."""
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
    
    def listen(self, timeout: int = 5) -> Optional[str]:
        """Listen for speech input with timeout and error handling."""
        try:
            with sr.Microphone() as source:
                logging.info("Listening for input...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=timeout)
                
            text = self.recognizer.recognize_google(audio)
            logging.info(f"Recognized: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            logging.warning("Listening timed out")
            return None
        except sr.UnknownValueError:
            logging.warning("Could not understand audio")
            return None
        except Exception as e:
            logging.error(f"Error in speech recognition: {str(e)}")
            return None
    
    def speak(self, text: str) -> None:
        """Convert text to speech with error handling."""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logging.error(f"Error in text-to-speech: {str(e)}")

# handlers/search.py
import wikipedia
import requests
from typing import Optional, Dict, Any
import logging

class SearchHandler:
    def __init__(self, config: Config):
        self.config = config
    
    def search_wikipedia(self, query: str, sentences: int = 2) -> Optional[str]:
        """Search Wikipedia for information."""
        try:
            return wikipedia.summary(query, sentences=sentences)
        except wikipedia.exceptions.DisambiguationError as e:
            logging.warning(f"Ambiguous search term: {str(e.options)}")
            return None
        except Exception as e:
            logging.error(f"Wikipedia search error: {str(e)}")
            return None
    
    def get_weather(self, city: str) -> Optional[Dict[str, Any]]:
        """Get weather information for a city."""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': self.config.WEATHER_API_KEY,
                'units': 'metric'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Weather API error: {str(e)}")
            return None

# handlers/media.py
import pywhatkit
import webbrowser
from typing import Optional
import logging

class MediaHandler:
    def play_music(self, query: str) -> bool:
        """Play music from YouTube."""
        try:
            pywhatkit.playonyt(query)
            return True
        except Exception as e:
            logging.error(f"Error playing music: {str(e)}")
            return False
    
    def open_website(self, url: str) -> bool:
        """Open a website in the default browser."""
        try:
            webbrowser.open(url)
            return True
        except Exception as e:
            logging.error(f"Error opening website: {str(e)}")
            return False

# core.py
import logging
from typing import Optional
from .handlers.speech import SpeechHandler
from .handlers.search import SearchHandler
from .handlers.media import MediaHandler
from .config import Config

class VirtualAssistant:
    def __init__(self):
        self.config = Config.from_env()
        self.speech = SpeechHandler()
        self.search = SearchHandler(self.config)
        self.media = MediaHandler()
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging for the assistant."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('assistant.log'),
                logging.StreamHandler()
            ]
        )
    
    def process_command(self, command: str) -> Optional[str]:
        """Process user commands and return appropriate responses."""
        try:
            if 'play' in command:
                song = command.replace('play', '').strip()
                if self.media.play_music(song):
                    return f"Playing {song}"
                return "Sorry, I couldn't play that song"
            
            elif 'search' in command:
                query = command.replace('search', '').strip()
                info = self.search.search_wikipedia(query)
                if info:
                    return info
                return "I couldn't find that information"
            
            elif 'weather' in command:
                city = command.replace('weather', '').strip()
                weather = self.search.get_weather(city)
                if weather:
                    temp = weather['main']['temp']
                    desc = weather['weather'][0]['description']
                    return f"The weather in {city} is {desc} with temperature {temp}°C"
                return "I couldn't get the weather information"
            
            else:
                return "I'm not sure how to help with that"
                
        except Exception as e:
            logging.error(f"Error processing command: {str(e)}")
            return "Sorry, I encountered an error"
    
    def run(self):
        """Main loop for the virtual assistant."""
        self.speech.speak("Hello! How can I help you?")
        
        while True:
            command = self.speech.listen()
            
            if command is None:
                self.speech.speak("I didn't catch that. Could you repeat?")
                continue
            
            if 'stop' in command or 'exit' in command:
                self.speech.speak("Goodbye!")
                break
            
            response = self.process_command(command)
            if response:
                self.speech.speak(response)

# Example usage:
if __name__ == "__main__":
    assistant = VirtualAssistant()
    assistant.run()
