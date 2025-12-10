# Option 1: Using python-dotenv (recommended)
from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env file in current directory
api_key = os.getenv("SAIA_API_KEY")

# Option 2: Load from specific path
load_dotenv("/path/to/.env")

# Option 3: Without dotenv (manual parsing)
api_key = os.getenv("SAIA_API_KEY")  # Requires .env in PATH or shell export

