import speech_recognition as sr
import pyttsx3
from pydub import AudioSegment
import soundfile as sf


class Transcriber:

    def __init__(self):
        self.r = sr.Recognizer()

    def recognize(self, audio_input):
        print(f"Recognizing audio from: {audio_input}")  # Debug print
        try:
            with sr.AudioFile(audio_input) as source:
                audio_listened = self.r.record(source)
                # Try converting it to text
                try:
                    text = self.r.recognize_azure(audio_listened,key="key",location="switzerlandnorth")
                    print(text)  # Print the recognized text
                except sr.UnknownValueError as e:
                    print(f"Error in recognition: {e}")
                    text = None  # Set text to None if recognition fails
        except Exception as e:
            print(f"Error loading audio file: {e}")
            text = None  # Set text to None if loading fails

        return text