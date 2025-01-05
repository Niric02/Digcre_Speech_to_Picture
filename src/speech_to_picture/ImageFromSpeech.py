import logging
import os
from datetime import datetime

import replicate

from image_model.ReplicateImageModel import ReplicateImageModel
from llm.ReplicatePrompter import ReplicatePrompter


class ImageFromSpeech:
    def __init__(self, replicate_client: replicate.Client, logger: logging.Logger):
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
        prompt = await self.llm.run(transcript, context)
        self.append_prompt_to_file(prompt)
        self.prompt_history.append({"role": "prompter", "content": prompt})
        image_path = await self.imager.run(prompt)
        return image_path

    def append_transcription_to_file(self, transcription):
        timestamp = datetime.now().strftime("%Y%m%d")  # Format: YYYYMMDD_HHMMSS
        filename = f"{timestamp}.txt"

        transcriptions_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../transcription")
        os.makedirs(transcriptions_dir, exist_ok=True)
        file_path = os.path.join(transcriptions_dir, filename)

        with open(file_path, "a") as file:
            file.write(f"{transcription}\n")

    def append_prompt_to_file(self, prompt):
        timestamp = datetime.now().strftime("%Y%m%d")  # Format: YYYYMMDD_HHMMSS
        filename = f"{timestamp}.txt"

        prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../prompts")
        os.makedirs(prompts_dir, exist_ok=True)
        file_path = os.path.join(prompts_dir, filename)

        with open(file_path, "a") as file:
            file.write(f"prompt: [{prompt}]\n\n")

    def generate_prompt_template(self):
        context = os.getenv('CONTEXT')

        prompt_template = f"<|start_header_id|>system<|end_header_id|>\n\n{context}"

        for history in self.prompt_history:
            prompt_template += f"<|eot_id|><|start_header_id|>{history['role'][-5:]}<|end_header_id|>\n\n{history['content'][-5:]}"

        prompt_template += f" <|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{{prompt}}<|eot_id|><|start_header_id|>prompter<|end_header_id|>\n\n"  # End of context

        return prompt_template
