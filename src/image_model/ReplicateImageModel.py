from datetime import datetime
import os

import replicate


class ReplicateImageModel:
    def __init__(self, client, logger):
        self.client = client
        self.logger = logger.getChild('image')

    def create_imput(self, prompt):
        #input = {"raw": False,
        #         "prompt": prompt,
        #         "aspect_ratio": "3:2",
        #         "output_format": "jpg",
        #         "safety_tolerance": 6,
        #         "image_prompt_strength": 0.1,
        #         "seed": 6969693245266
        #         }

        input = {
            "prompt": prompt,
            "go_fast": True,
            "guidance": 3.5,
            "num_outputs": 1,
            "aspect_ratio": "3:2",
            "output_format": "jpg",
            "output_quality": 80,
            "prompt_strength": 0.8,
            "num_inference_steps": 28,
            "seed": 6969693245266,
            "disable_safety_checker": True
        }
        return input

    async def run(self, prompt):
        input = self.create_imput(prompt)
        self.logger.info(f"generating Image from prompt: {input}")
        output = await self.client.async_run(
            #"black-forest-labs/flux-1.1-pro-ultra",
            "black-forest-labs/flux-dev",
            input=input,
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
        filename = f"{timestamp}.jpg"

        # Define the target directory for saving images
        images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../images")

        # Ensure the directory exists
        os.makedirs(images_dir, exist_ok=True)

        # Construct the full path to save the image
        file_path = os.path.join(images_dir, filename)

        print(output)

        # Write the image to the file
        with open(file_path, "wb") as file:
            file.write(output[0].read())

        self.logger.info(f"Image saved to {file_path}")

        return file_path
