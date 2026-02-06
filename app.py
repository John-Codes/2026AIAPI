from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import httpx
import json

app = FastAPI()

class GenerateRequest(BaseModel):
    text: str
    image_url: str = None
    api_key: str = None
    model_name: str = None

def get_api_key(request_api_key: str = None):
    """Get API key from request or environment"""
    if request_api_key:
        os.environ['Open_Router'] = request_api_key
        return request_api_key
    return os.getenv('Open_Router')

def get_model_name(request_model_name: str = None):
    """Get model name from request or environment"""
    if request_model_name:
        os.environ['Model_Name'] = request_model_name
        return request_model_name
    return os.getenv('Model_Name')

async def call_openrouter_api(messages, api_key: str, model: str):
    """Call OpenRouter API with the given messages"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "FastAPI OpenRouter Client"
    }
    
    data = {
        "model": model,
        "messages": messages
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except httpx.HTTPError as e:
            error_msg = f"API Error: {str(e)}"
            if e.response:
                error_msg = f"API Error: {e.response.status_code} - {e.response.text}"
            return error_msg
        except Exception as e:
            return f"Unexpected Error: {str(e)}"

@app.post("/generate")
async def generate(request: GenerateRequest):
    # Get API key and model name
    api_key = get_api_key(request.api_key)
    model_name = get_model_name(request.model_name)
    
    if not api_key:
        raise HTTPException(status_code=400, detail="API key is required")
    
    if not model_name:
        raise HTTPException(status_code=400, detail="Model name is required")
    
    # Build messages
    messages = [{"role": "user", "content": request.text}]
    
    # Add image if provided (basic multimodal support)
    if request.image_url:
        # Note: Full multimodal support would require more complex handling
        # For now, we'll just append the image URL to the text
        messages[0]["content"] = f"{request.text}\n\nImage: {request.image_url}"
    
    # Call OpenRouter API
    response_text = await call_openrouter_api(messages, api_key, model_name)
    
    return {"response": response_text}