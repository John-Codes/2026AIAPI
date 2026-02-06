# FastAPI OpenRouter Integration

A FastAPI application that integrates with OpenRouter's LLM API to provide text generation capabilities with optional multimodal support for images.

## Features

- **Text Generation**: Generate text using OpenRouter's LLM models
- **Multimodal Support**: Optional image URL parameter for multimodal inputs
- **Flexible Configuration**: API key and model name can be provided via request or environment variables
- **RESTful API**: Clean, well-documented REST endpoint
- **Docker Support**: Containerized for easy deployment
- **Test Coverage**: Comprehensive test suite with real API integration

## API Endpoints

### GET /heartbeat

Health check endpoint to verify the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

### POST /generate

Generate text using OpenRouter's LLM API.

**Request Body:**
```json
{
  "text": "string (required)",
  "image_url": "string (optional)",
  "api_key": "string (optional)",
  "model_name": "string (optional)"
}
```

**Response:**
```json
{
  "response": "Generated text from the LLM"
}
```

**Parameters:**
- `text` (required): The input text to send to the LLM
- `image_url` (optional): URL of an image to include in multimodal input
- `api_key` (optional): OpenRouter API key (defaults to `Open_Router` environment variable)
- `model_name` (optional): Model name to use (defaults to `Model_Name` environment variable)

## Installation & Local Setup

### Prerequisites

- Python 3.10+
- Docker (optional, for containerized deployment)

### Local Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd 2026AIAPI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file with your OpenRouter credentials
echo 'Open_Router="your-openrouter-api-key"' > .env
echo 'Model_Name="moonshotai/kimi-k2.5"' >> .env
```

4. Run the application:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### Running Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest test_app.py -v

# Run with coverage
pytest test_app.py --cov=app
```

## Docker Deployment

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd 2026AIAPI
```

2. Set up environment variables:
```bash
# Create .env file with your OpenRouter credentials
echo 'Open_Router="your-openrouter-api-key"' > .env
echo 'Model_Name="moonshotai/kimi-k2.5"' >> .env
```

3. Run with Docker Compose:
```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`

### Using Docker Image Directly

#### Pull from Docker Hub

```bash
docker pull efexzium/fastapi-openrouter-app
```

#### Run the Container

```bash
# With environment variables
docker run -d \
  --name fastapi-openrouter \
  -p 8000:8000 \
  -e Open_Router="your-openrouter-api-key" \
  -e Model_Name="moonshotai/kimi-k2.5" \
  efexzium/fastapi-openrouter-app

# With .env file mount
docker run -d \
  --name fastapi-openrouter \
  -p 8000:8000 \
  -v $(pwd)/.env:/app/.env \
  efexzium/fastapi-openrouter-app
```

### Building Custom Docker Image

```bash
# Build the image
docker build -t fastapi-openrouter-app .

# Run the built image
docker run -d \
  --name fastapi-openrouter \
  -p 8000:8000 \
  -v $(pwd)/.env:/app/.env \
  fastapi-openrouter-app
```

## API Usage Examples

### Basic Text Generation

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, tell me about artificial intelligence"
  }'
```

### Heartbeat Check

```bash
# Check API health
curl -X GET "http://localhost:8000/heartbeat"
```

```python
import requests

# Check API health
response = requests.get("http://localhost:8000/heartbeat")
print(response.json())
```

### With Custom API Key and Model

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Describe this image",
    "image_url": "https://example.com/image.jpg",
    "api_key": "your-api-key",
    "model_name": "openai/gpt-4"
  }'
```

### Python Example

```python
import requests

response = requests.post("http://localhost:8000/generate", json={
    "text": "Write a short story about a robot",
    "api_key": "your-api-key",
    "model_name": "anthropic/claude-3"
})

print(response.json())
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `Open_Router` | OpenRouter API key | Required |
| `Model_Name` | Default model name | Required |

## Docker Image Details

- **Image Name**: `efexzium/fastapi-openrouter-app`
- **Tag**: `latest`
- **Architecture**: Multi-platform support
- **Base Image**: Python 3.10-slim
- **Port**: 8000

## API Documentation

When running the application, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## Development

### Project Structure

```
2026AIAPI/
├── app.py                 # FastAPI application
├── test_app.py           # Test suite
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── .env                 # Environment variables
└── README.md            # This documentation
```

### Adding New Features

1. Write tests first (TDD approach)
2. Implement minimal functionality
3. Run tests to ensure they pass
4. Refactor if needed

### Testing

The project follows Test-Driven Development (TDD) principles with real API integration tests:

- **Missing required fields**: Validates input validation
- **Happy path**: Tests successful text generation
- **Optional parameters**: Tests image URL and optional parameters
- **Configuration updates**: Tests API key and model name updates
- **Real API failure**: Tests error handling with invalid credentials

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your OpenRouter API key is valid and has sufficient quota
2. **Model Not Found**: Check if the model name is correct and available in OpenRouter
3. **Port Already in Use**: Change the port in the command or stop the conflicting service
4. **Docker Issues**: Ensure Docker is running and you have proper permissions

### Logs

```bash
# View container logs
docker logs fastapi-openrouter

# Follow logs in real-time
docker logs -f fastapi-openrouter
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Ensure all tests pass
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Questions

### Common Questions

**Q: What models are supported?**
A: Any model available in OpenRouter's API. You can specify the model name in the request or set it as an environment variable.

**Q: How do I get an OpenRouter API key?**
A: Sign up at [OpenRouter.ai](https://openrouter.ai) and generate an API key from your dashboard.

**Q: Can I use this commercially?**
A: Yes, this application can be used for commercial purposes. Ensure you comply with OpenRouter's terms of service.

**Q: How do I add custom models?**
A: Add the model name to your request or update the `Model_Name` environment variable. The model must be available in OpenRouter's catalog.

**Q: What's the performance like?**
A: Performance depends on the model you choose and your network connection. The application uses async HTTP client for optimal performance.

**Q: How do I scale this application?**
A: You can use Docker Swarm, Kubernetes, or any container orchestration platform to scale the application horizontally.

**Q: Can I add authentication?**
A: Yes, you can add authentication middleware to the FastAPI application. Consider using JWT or OAuth2 for production use.

**Q: How do I monitor the application?**
A: You can integrate with monitoring tools like Prometheus, Grafana, or use cloud provider monitoring services.

**Q: What are the security considerations?**
A: 
- Keep your API keys secure
- Use HTTPS in production
- Implement rate limiting
- Validate all inputs
- Use proper error handling
- Monitor for abuse

## Support

For support, please:
1. Check the troubleshooting section
2. Review the API documentation
3. Check OpenRouter's status page
4. Open an issue in the repository

---

**Docker Image**: `efexzium/fastapi-openrouter-app`  
**Registry**: Docker Hub  
**Last Updated**: 2026-02-06