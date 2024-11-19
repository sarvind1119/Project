from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the variables
speech_key = os.getenv("SPEECH_KEY")
speech_region = os.getenv("SPEECH_REGION")

print(f"Speech Key: {speech_key}")
print(f"Speech Region: {speech_region}")
