from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx
import json
import base64
import io
from dotenv import load_dotenv
from PIL import Image

app = FastAPI()

# Load .env file
load_dotenv()

# Add CORS middleware to allow requests from Flutter web app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    text: str
    image_url: str = None
    image_data: str = None  # Base64 encoded image
    api_key: str = None
    model_name: str = None

def get_api_key(request_api_key: str = None):
    """Get API key from request or environment, use default if none provided"""
    if request_api_key:
        os.environ['Open_Router'] = request_api_key
        return request_api_key
    env_key = os.getenv('Open_Router')
    if env_key:
        return env_key
    # Default API key for testing (user should replace this with their own)
    return "sk-or-xxxx"  # This will need to be replaced with actual API key

def get_model_name(request_model_name: str = None):
    """Get model name from request or environment, use default if none provided"""
    if request_model_name:
        os.environ['Model_Name'] = request_model_name
        return request_model_name
    env_model = os.getenv('Model_Name')
    if env_model:
        return env_model
    # Default model for testing
    return "z-ai/glm-4.5-air:free"

def validate_image_file(file: UploadFile):
    """Validate uploaded image file"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only JPEG and PNG images are supported")
    
    # Check file size (max 5MB)
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size and file.size > max_size:
        raise HTTPException(status_code=400, detail="File size must be less than 5MB")

def process_image_to_base64(file: UploadFile):
    """Process uploaded image and return base64 encoded string"""
    validate_image_file(file)
    
    # Read image file
    image_data = file.file.read()
    
    # Open image with PIL to validate and potentially resize
    image = Image.open(io.BytesIO(image_data))
    
    # Convert to RGB if necessary (for PNG with transparency)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize image if too large (max 1024x1024)
    max_size = (1024, 1024)
    if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG', quality=85)
    img_byte_arr = img_byte_arr.getvalue()
    
    # Encode to base64
    base64_image = base64.b64encode(img_byte_arr).decode('utf-8')
    
    return base64_image

def create_multimodal_message(text: str, image_url: str = None, image_data: str = None):
    """Create message in multimodal format for OpenRouter API"""
    if image_url:
        # URL-based image (legacy support)
        return [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
    elif image_data:
        # Base64 encoded image
        return [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]
            }
        ]
    else:
        # Text only
        return [{"role": "user", "content": text}]

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
    
    # Debug logging
    print(f"Sending request to OpenRouter with model: {model}")
    print(f"Messages: {messages}")
    
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
                if e.response.status_code == 401:
                    error_msg = "Authentication failed. Please check your API key or configure a valid API key in the settings."
                else:
                    error_msg = f"API Error: {e.response.status_code} - {e.response.text}"
            return error_msg
        except Exception as e:
            return f"Unexpected Error: {str(e)}"

@app.post("/generate")
async def generate(request: GenerateRequest):
    # Get API key and model name (with defaults if not provided)
    api_key = get_api_key(request.api_key)
    model_name = get_model_name(request.model_name)
    
    # Create multimodal message
    messages = create_multimodal_message(
        text=request.text,
        image_url=request.image_url,
        image_data=request.image_data
    )
    
    # Call OpenRouter API
    response_text = await call_openrouter_api(messages, api_key, model_name)
    
    return {"response": response_text}

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """Upload and process image file, return base64 encoded data"""
    try:
        # Process image to base64
        base64_image = process_image_to_base64(file)
        
        return {
            "success": True,
            "image_data": base64_image,
            "filename": file.filename,
            "content_type": file.content_type
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/heartbeat")
async def heartbeat():
    """Health check endpoint to verify the API is running"""
    return {"status": "healthy", "message": "API is running"}