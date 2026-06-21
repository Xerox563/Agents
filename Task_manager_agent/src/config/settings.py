import os
from dotenv import load_dotenv

load_dotenv()

# API Settings
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your-openrouter-api-key-here")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here") # Fallback or if needed

# OpenRouter Specific
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = os.getenv("MODEL", "openai/gpt-3.5-turbo") # OpenRouter format

# Today's date for examples
TODAY = "2024-01-15"

# Max iterations (agent can't loop forever)
MAX_ITERATIONS = 5
