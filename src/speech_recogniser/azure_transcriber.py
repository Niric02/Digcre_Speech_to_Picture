import azure.cognitiveservices.speech as speechsdk


class Transcriber:
    def __init__(self, key, region):
        self.speech_config = speechsdk.SpeechConfig(subscription=key, region=region)

    def from_file(self, filename):
        print(f"transcribing{filename}")
        audio_config = speechsdk.AudioConfig(filename=filename)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        # Connect to events
        speech_recognizer.recognized.connect(self.recognize_speech)
        speech_recognizer.session_stopped.connect(self.speech_end_detected)
        speech_recognizer.canceled.connect(self.speech_end_detected)

        # Start continuous recognition
        result = speech_recognizer.start_continuous_recognition_async()

        speech_recognizer.session_stopped.connect(lambda evt: result.set_result(None))
        # Wait for recognition to finish
        return result.get()

    def recognize_speech(self, evt):
        print(f"Recognizing: {evt.result.text}")

    def speech_end_detected(self, evt):
        print("Speech recognition ended.")
        evt.result.get_async().stop_continuous_recognition_async()
