import speech_recognition as sr
import pyttsx3
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def normalize_command(command):
    """Normalize the command by converting to lower case and stripping whitespace."""
    return command.lower().strip() if command else ""

def listen_for_command(timeout=5):
    """Listen for a command with a specified timeout."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout)
            command = recognizer.recognize_google(audio)
            print(f"Command received: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None
        except sr.RequestError as e:
            print(f"Sorry, there was an error with the speech recognition service: {e}")
            return None

# Define the inspection steps
inspection_steps = [
    "Let us check the front tires.",
    "Please check the rear tires.",
    "Inspect the battery.",
    "Examine the exterior.",
    "Check the brakes.",
    "Review the engine."
]

def perform_inspection_step(step):
    """Perform an inspection step, prompting the user to say 'done' when finished."""
    print(step)
    speak(step)

    time.sleep(2)
    
    speak("Say 'done' when you have finished.")
    
    while True:
        command = listen_for_command(timeout=5)
        normalized_command = normalize_command(command)
        
        if "done" in normalized_command:
            result = f"{step} - Completed"
            speak(f"{result}")
            return result
        elif normalized_command:
            speak("Please say 'done' when you have finished.")
        else:
            speak("Sorry, I didn't catch that. Please say 'done' when you have finished.")

def save_results(results):
    """Save the inspection results to a file."""
    with open("inspection_results.txt", "a") as file:
        for result in results:
            file.write(result + "\n")

def main():
    """Main function to run the inspection process."""
    results = []
    for step in inspection_steps:
        result = perform_inspection_step(step)
        results.append(result)
    
    save_results(results)
    speak("Inspection completed. Results have been saved.")
    print("Inspection completed. Results have been saved.")

if __name__ == "__main__":
    main()

