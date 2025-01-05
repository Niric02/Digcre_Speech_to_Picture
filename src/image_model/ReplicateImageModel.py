import logging
import os
from datetime import datetime

import replicate


class ReplicateImageModel:
    def __init__(self, client: replicate.Client, logger: logging.Logger):
        self.client = client
        self.logger = logger.getChild('image')

    def create_input(self, prompt):
        return {
            "prompt": prompt,
            "go_fast": True,
            "guidance": 3.5,
            "num_outputs": 1,
            "aspect_ratio": "3:2",
            "output_format": "jpg",
            "output_quality": 80,
            "prompt_strength": 0.8,
            "num_inference_steps": 28,
            "seed": 2,
            "disable_safety_checker": True
        }

    async def run(self, prompt):
        prompt_input = self.create_input(prompt)
        self.logger.info(f"generating Image from prompt: {prompt_input}")
        output = await self.client.async_run(
            # "black-forest-labs/flux-1.1-pro-ultra", # alternative model, nsfw problems
            "black-forest-labs/flux-dev",
            input=prompt_input,
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
        filename = f"{timestamp}.jpg"

        images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../images")
        os.makedirs(images_dir, exist_ok=True)
        file_path = os.path.join(images_dir, filename)

        print(output)

        with open(file_path, "wb") as file:
            file.write(output[0].read())

        self.logger.info(f"Image saved to {file_path}")

        return file_path
