import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')