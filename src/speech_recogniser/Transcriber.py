import speech_recognition as sr


class Transcriber:

    def __init__(self):
        self.r = sr.Recognizer()

    def recognize(self, audio_input):

        print(type(audio_input))
        text = self.r.recognize_google(audio_input)

        return text