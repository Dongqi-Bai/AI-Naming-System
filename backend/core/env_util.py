import os
import dotenv

dotenv.load_dotenv(override=True)  # Load environment variables from .env file

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


