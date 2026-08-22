from dotenv import load_dotenv
import os 

load_dotenv(".env")

api_key = os.getenv("ANTHROPIC_API_KEY")
assert api_key is not None