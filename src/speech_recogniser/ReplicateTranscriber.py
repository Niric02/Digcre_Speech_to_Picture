from dataclasses import dataclass

import replicate


@dataclass
class TimestampedTranscription:
    start: int
    end: int
    text: str
    identifier: any


class ReplicateTranscriber:
    def __init__(self, replicate_token, language=None):
        if language is None:
            language = "auto"
        self.client = replicate.Client(api_token=replicate_token)
        self.language = language

    def from_file(self, file_path, identifier=None) -> list[TimestampedTranscription]:
        audio = open(file_path, "rb")
        replicate_input = {
            "audio": audio,
            "language": self.language,  # auto | de | en
        }
        output = self.client.run(
            "openai/whisper:cdd97b257f93cb89dede1c7584e3f3dfc969571b357dbcee08e793740bedd854",
            input=replicate_input
        )

        print("Output:", output)
        return [TimestampedTranscription(text=segment['text'],
                                         start=segment['start'],
                                         end=segment['end'],
                                         identifier=identifier)
                for segment in output['segments']]
