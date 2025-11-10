import asyncio
import httpx
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Get BASE_URL from environment or use default
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
# Remove /v1 from BASE_URL if present, we'll add it in the code
if BASE_URL.endswith("/v1"):
    BASE_URL = BASE_URL[:-3]
BASE_URL = f"{BASE_URL}/v1"
