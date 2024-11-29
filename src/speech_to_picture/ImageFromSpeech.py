from datetime import datetime

from image_model.ReplicateImageModel import ReplicateImageModel
from llm.ReplicatePrompter import ReplicatePrompter
from speech_recogniser.ReplicateTranscriber import ReplicateTranscriber
import os


class ImageFromSpeech:
    def __init__(self, replicate_client, logger):
        self.logger = logger.getChild("image-from-speech")
        self.replicate_client = replicate_client
        self.llm = ReplicatePrompter(self.replicate_client, logger)
        self.imager = ReplicateImageModel(self.replicate_client, logger)
        self.prompt_history = []

    async def generate_image_from_transcription(self, transcript: str):
        context = self.generate_prompt_template()
        self.append_transcription_to_file(transcript)
        self.prompt_history.append({"role": "user", "content": transcript})
        self.logger.info(transcript)
        prompt = await self.llm.run(transcript,context)
        self.append_prompt_to_file(prompt)
        self.prompt_history.append({"role": "prompter", "content": prompt})
        image_path = await self.imager.run(prompt)
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

    def generate_prompt_template(self):
        context = os.getenv('CONTEXT')

        prompt_template = f"<|start_header_id|>system<|end_header_id|>\n\n{context}"

        for history in self.prompt_history:
            prompt_template += f"<|eot_id|><|start_header_id|>{history['role']}<|end_header_id|>\n\n{history['content']}"

        prompt_template += f" <|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{{prompt}}<|eot_id|><|start_header_id|>prompter<|end_header_id|>\n\n"  # End of context

        return prompt_template
