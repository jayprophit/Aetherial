from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel
import asyncio
import json
import logging
from typing import Dict, List, Optional
import speech_recognition as sr
import smtplib
import email.message
from datetime import datetime
import aiofiles
import yaml
import sqlite3
import face_recognition
import numpy as np
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(title="Virtual Assistant API")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Message(BaseModel):
    content: str
    type: str
    timestamp: datetime = None

class User(BaseModel):
    id: str
    name: str
    email: str
    voice_profile: Optional[bytes]
    face_profile: Optional[bytes]

class VirtualAssistant:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.active_sessions: Dict[str, WebSocket] = {}
        self.recognizer = sr.Recognizer()
        self.load_config()
        self.setup_database()

    def load_config(self):
        try:
            with open('config.yaml', 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            logger.error("Config file not found")
            self.config = {}

    def setup_database(self):
        self.conn = sqlite3.connect('assistant.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            content TEXT,
            timestamp DATETIME,
            type TEXT
        )
        ''')
        self.conn.commit()

    async def process_message(self, message: Message, user_id: str) -> Message:
        """Process incoming messages and generate responses"""
        try:
            # Log message
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO messages (user_id, content, timestamp, type) VALUES (?, ?, ?, ?)",
                (user_id, message.content, datetime.now(), message.type)
            )
            self.conn.commit()

            # Process command
            response_content = await self.handle_command(message.content, user_id)
            
            return Message(
                content=response_content,
                type="assistant",
                timestamp=datetime.now()
            )

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def handle_command(self, command: str, user_id: str) -> str:
        """Handle different types of commands"""
        command = command.lower()
        
        if "email" in command:
            return await self.handle_email_command(command, user_id)
        elif any(word in command for word in ["schedule", "remind", "plan"]):
            return await self.handle_schedule_command(command, user_id)
        elif "play" in command:
            return await self.handle_media_command(command, user_id)
        else:
            return "I'm not sure how to help with that. Could you please rephrase?"

    async def handle_email_command(self, command: str, user_id: str) -> str:
        """Handle email-related commands"""
        # Email handling logic here
        return "Email functionality is being processed"

    async def handle_schedule_command(self, command: str, user_id: str) -> str:
        """Handle scheduling-related commands"""
        # Scheduling logic here
        return "Schedule functionality is being processed"

    async def handle_media_command(self, command: str, user_id: str) -> str:
        """Handle media playback commands"""
        # Media handling logic here
        return "Media playback functionality is being processed"

# Initialize assistant
assistant = VirtualAssistant()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    assistant.active_sessions[user_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            message = Message(**json.loads(data))
            response = await assistant.process_message(message, user_id)
            await websocket.send_text(response.json())
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        del assistant.active_sessions[user_id]

@app.post("/register_user")
async def register_user(user: User):
    assistant.users[user.id] = user
    return {"status": "success", "message": "User registered successfully"}

@app.post("/register_voice")
async def register_voice(user_id: str, audio_data: bytes):
    if user_id not in assistant.users:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Process and store voice profile
    assistant.users[user_id].voice_profile = audio_data
    return {"status": "success", "message": "Voice profile registered"}

@app.post("/register_face")
async def register_face(user_id: str, image_data: bytes):
    if user_id not in assistant.users:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Process and store face profile
    face_encoding = face_recognition.face_encodings(
        face_recognition.load_image_file(image_data)
    )[0]
    assistant.users[user_id].face_profile = face_encoding.tobytes()
    return {"status": "success", "message": "Face profile registered"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
