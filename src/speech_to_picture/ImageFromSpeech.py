from datetime import datetime

from src.image_model.ReplicateImageModel import ReplicateImageModel
from src.llm.ReplicatePrompter import ReplicatePrompter
from src.speech_recogniser.ReplicateTranscriber import ReplicateTranscriber
import os


class ImageFromSpeech:
    def __init__(self, replicate_client, logger):
        self.logger = logger
        self.replicate_client = replicate_client
        self.llm = ReplicatePrompter(self.replicate_client, logger)
        self.llm.set_context(os.getenv('CONTEXT'))

        self.imager = ReplicateImageModel(self.replicate_client, logger)

    def generate_image_from_transcription(self, transcript: str):
        self.append_transcription_to_file(transcript)
        self.logger.info(transcript)
        prompt = self.llm.run(transcript)
        self.append_prompt_to_file(prompt)
        image_path = self.imager.run(prompt)
        return image_path

    def append_transcription_to_file(self,transcription):
        timestamp = datetime.now().strftime("%Y%m%d")  # Format: YYYYMMDD_HHMMSS
        filename = f"{timestamp}.txt"

        # Define the target directory for saving images
        images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../transcription")

        # Ensure the directory exists
        os.makedirs(images_dir, exist_ok=True)

        # Construct the full path to save the image
        file_path = os.path.join(images_dir, filename)

        # Open the file in append mode
        with open(file_path, "a") as file:
            # Write the transcription to the file followed by a newline
            file.write(f"{transcription}\n")

    def append_prompt_to_file(self,prompt):
        timestamp = datetime.now().strftime("%Y%m%d")  # Format: YYYYMMDD_HHMMSS
        filename = f"{timestamp}.txt"

        # Define the target directory for saving images
        images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../prompts")

        # Ensure the directory exists
        os.makedirs(images_dir, exist_ok=True)

        # Construct the full path to save the image
        file_path = os.path.join(images_dir, filename)

        # Open the file in append mode
        with open(file_path, "a") as file:
            # Write the transcription to the file followed by a newline
            file.write(f"prompt: [{prompt}]\n\n")
