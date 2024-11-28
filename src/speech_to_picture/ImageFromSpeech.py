from src.image_model.ReplicateImageModel import ReplicateImageModel
from src.llm.ReplicatePrompter import ReplicatePrompter
from src.speech_recogniser.ReplicateTranscriber import ReplicateTranscriber
import os


class ImageFromSpeech:
    def __init__(self, replicate_client, logger):
        self.logger = logger
        self.replicate_client = replicate_client
        self.llm = ReplicatePrompter(self.replicate_client,logger)
        self.llm.set_context(os.getenv('CONTEXT'))

        self.imager = ReplicateImageModel(self.replicate_client,logger)

    def generate_image_from_transcription(self, transcript: str):
        self.logger.info(transcript)
        prompt = self.llm.run(transcript)
        image_path = self.imager.run(prompt)
        return image_path
