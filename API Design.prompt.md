You are a strict adherent to Test-Driven Development (TDD). Follow TDD exactly: Write a failing test first, then the minimal code to make it pass, refactor if needed, and repeat. Only write end-to-end real tests—no mocks, stubs, fakes, or any BS isolation. Tests must use real dependencies (e.g., real HTTP calls to OpenRouter's API) and run against a live setup. Keep everything super minimalistic, clean, and adhering to the Single Responsibility Principle (SRP)—each function/class does one thing only.

Task: Build a FastAPI application with a single endpoint "/generate" that accepts POST requests with JSON body containing "text" (required string) and "image_url" (optional string) and a Open router API key optional string and a model name optional string. The endpoint calls OpenRouter's LLM API (use their actual endpoint, e.g., https://openrouter.ai/api/v1/chat/completions, and assume an API key is provided via environment variable update the env var if the end point recieves the new API key or model name. Pass the text as a user message, and if image_url is provided, include it as an image in the multimodal input if the model supports it if it doesnt work for any reason wrong API key or model return error message. Return the LLM's response text in the API response.

Constraints:
- Use Python 3.10+ and FastAPI only—no extra frameworks or libs except pydantic for models and httpx for real HTTP calls in the implementation (but tests use real endpoints).
- No logging, error handling beyond basics, or extras—keep it minimal.
- Structure: One file for app code (app.py), one for tests (test_app.py). Use pytest for tests.
- TDD steps: Document each cycle (failing test -> minimal code -> passing test -> refactor). Cover happy path, missing text, optional image, and real LLM failure scenarios in E2E tests.
- Run tests assuming a real OpenRouter API key in env; tests must make actual API calls.
- Output the final code only after all TDD cycles, in two sections: app.py and test_app.py.

Start with the first failing test.I wrote the API key and model name in the .env remember to add a git ignore.