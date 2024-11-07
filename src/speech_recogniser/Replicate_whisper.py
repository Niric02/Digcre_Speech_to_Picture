import os
import requests
import replicate
from dotenv import load_dotenv

# Load API token from .env file
load_dotenv()
client = replicate.Client(api_token=os.getenv('REPLICATE_API_TOKEN'))

# Path to your local .wav file
file_path = "./255787146701570050.wav"

audio = open(file_path, "rb");

# Now, pass the URL to Replicate
input = {
    "audio": audio
}

output = client.run(
    "openai/whisper:cdd97b257f93cb89dede1c7584e3f3dfc969571b357dbcee08e793740bedd854",
    input=input
)
print("Output:", output)
