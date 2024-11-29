import src.speech_recogniser.Transcriber
from src.speech_recogniser.azure_transcriber import Transcriber
from dotenv import load_dotenv
import os
import replicate
from src.llm.ReplicatePrompter import ReplicatePrompter as Prompter




if __name__ == '__main__':
    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')
    AZUREKEY = os.getenv('AZURE_KEY')
    REGION = os.getenv('REGION')
    replicateToken = os.getenv('REPLICATE_TOKEN')

    client = replicate.Client(api_token=replicateToken)

    prompter = Prompter(client)

    prompter.run("I have a week of item positions exercise, but in portfolio I don't put in number nine, but I put everything from one to eight. Does it count or not? Yes, I mean you need to, you can skip one of those. And if you don't include it, that would be one solution. Thank you")

