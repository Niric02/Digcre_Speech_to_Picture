import speech_recognition as sr


class Transcriber:

    def __init__(self):
        self.r = sr.Recognizer()

    def recognize(self, audio):
        text = self.r.recognize_google(audio)

        return text