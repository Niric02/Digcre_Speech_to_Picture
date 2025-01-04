import logging
from dataclasses import dataclass

import replicate


@dataclass
class TimestampedTranscription:
    start: int
    end: int
    text: str
    identifier: any


class ReplicateTranscriber:
    def __init__(self, client: replicate.Client, logger: logging.Logger, language=None):
        if language is None:
            language = "auto"
        self.client = client
        self.language = language
        self.logger = logger.getChild('transcriber')

    async def from_file(self, file_path, identifier=None) -> list[TimestampedTranscription]:
        audio = open(file_path, "rb")
        replicate_input = {
            "audio": audio,
            "language": self.language,  # auto | de | en
        }
        output = await self.client.async_run(
            "openai/whisper:cdd97b257f93cb89dede1c7584e3f3dfc969571b357dbcee08e793740bedd854",
            input=replicate_input
        )
        self.logger.info(f"Output: {output}")
        return [TimestampedTranscription(text=segment['text'],
                                         start=segment['start'],
                                         end=segment['end'],
                                         identifier=identifier)
                for segment in output['segments']]
