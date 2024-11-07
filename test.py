import src.speech_recogniser.Transcriber
from src.speech_recogniser.azure_transcriber import Transcriber
from dotenv import load_dotenv
import os




if __name__ == '__main__':
    load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')
    AZUREKEY = os.getenv('AZURE_KEY')
    REGION = os.getenv('REGION')

    transcriber = Transcriber(key=AZUREKEY, region=REGION)

    print(transcriber.from_file("D:/Digcre_Speech_to_Picture/Digcre_Speech_to_Picture/src/255787146701570050.wav"))