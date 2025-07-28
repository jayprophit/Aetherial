# ai_services/openai_client.py
from typing import Optional, Dict, List
import openai
import asyncio
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

class OpenAIService:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.logger = logging.getLogger(__name__)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def generate_code(self, prompt: str, model: str = "gpt-4") -> Optional[str]:
        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a specialized code generation AI."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000,
                top_p=1.0
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            return None

    async def enhance_prompt(self, base_prompt: str) -> str:
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Enhance the following prompt for optimal code generation:"},
                    {"role": "user", "content": base_prompt}
                ],
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Prompt enhancement error: {e}")
            return base_prompt

    async def validate_code(self, code: str) -> Dict[str, any]:
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Analyze this code for security and quality:"},
                    {"role": "user", "content": code}
                ]
            )
            return {
                "safe": True,
                "analysis": response.choices[0].message.content
            }
        except Exception as e:
            self.logger.error(f"Code validation error: {e}")
            return {"safe": False, "analysis": str(e)}
