# security/auth.py
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt
from datetime import datetime, timedelta

class SecurityManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.api_key_header = APIKeyHeader(name="X-API-Key")
        
    def create_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm="HS256")
        
    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def rate_limit(self, token: str) -> bool:
        # Implement rate limiting logic
        return True

# security/sanitizer.py
class InputSanitizer:
    @staticmethod
    def sanitize_prompt(prompt: str) -> str:
        # Implement input sanitization
        sanitized = prompt.strip()
        return sanitized

    @staticmethod
    def validate_generated_code(code: str) -> bool:
        # Implement code validation
        return True
