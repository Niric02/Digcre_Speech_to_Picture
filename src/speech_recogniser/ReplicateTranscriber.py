import replicate

class ReplicateTranscriber():
    def __init__(self,replicateToken):
        self.client = replicate.Client(api_token=replicateToken)

    def from_file(self, file_path):

        audio = open(file_path, "rb");

        # Now, pass the URL to Replicate
        input = {
            "audio": audio
        }

        output = self.client.run(
            "openai/whisper:cdd97b257f93cb89dede1c7584e3f3dfc969571b357dbcee08e793740bedd854",
            input=input
        )
        print("Output:", output)
        return output['transcription']
