import azure.cognitiveservices.speech as speechsdk


class Transcriber:

    def __init__(self,key,region):
        self.speech_config = speechsdk.SpeechConfig(subscription=key, region=region)

    def from_file(self, filename):

        audio_config = speechsdk.AudioConfig(filename=filename)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        speech_recognition_result = speech_recognizer.recognize_once_async().get()
        return speech_recognition_result.text
