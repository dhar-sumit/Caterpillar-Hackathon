# voice_recognition.py
import speech_recognition as sr

class VoiceRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def listen_for_command(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio)
                return command
            except sr.UnknownValueError:
                return "Sorry, I did not understand that."
            except sr.RequestError:
                return "Sorry, there was an issue with the speech recognition service."
