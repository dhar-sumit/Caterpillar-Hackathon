import pyttsx3
import speech_recognition as sr
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech rate
engine.setProperty('volume', 1)  # Adjust volume level

# def preprocess_text(text):
#     replacements = {
#         'bad': 'b-a-d',  # Break down words if necessary
#         'yes': 'y-e-s',
#         'less': 'l-e-s-s',
#     }
#     for word, replacement in replacements.items():
#         text = text.replace(word, replacement)
#     return text

def speak(text):
    # print(f"Speaking: {text}")  # Debugging statement
    # processed_text = preprocess_text(text)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)  # Ensure proper playback

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
            # print("Sorry, I did not understand that.")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None
        except sr.RequestError as e:
            print(f"Sorry, there was an error with the speech recognition service: {e}")
            return None

def ask_question(question, options=None, retries=3):
    """Ask a question and listen for a response, retrying if necessary."""
    for attempt in range(retries):
        print(question)
        speak(question)
        
        response = listen_for_command(timeout=10)
        
        if response is not None:
            normalized_response = normalize_command(response)
            if options and normalized_response not in options:
                speak("Invalid response. Please choose from: " + ", ".join(options))
                print("Invalid response. Please choose from: " + ", ".join(options))
            else:
                return normalized_response
        
        print("Sorry, I didn't catch that. Please try again.")
        speak("Sorry, I didn't catch that. Please try again.")
    
    # If all attempts fail, you might want to handle this case explicitly
    print("Unable to understand response after multiple attempts.")
    speak("I am unable to understand your response. Please check your input.")
    return None

def capture_image(section, part):
    """Simulate image capture and save the image with a specific name."""
    print(f"Please capture an image for {section} - {part}.")
    speak(f"Capture an image for {section} - {part}.")
    # This is where you would integrate your image capture code
    # For now, just simulating it with a placeholder
    return f"{section}_{part}.jpg"


def parts_questions(part_name,parts_ques,results):
    for question, options in parts_ques:
        answer = ask_question(question, options)
        if answer is not None:
            results.append(f"{question} {answer}")
            if "image" in question.lower():
                image = capture_image(f"{part_name}", question)
                results.append(f"Image captured: {image}")

def perform_inspection():
    """Perform the complete inspection process."""
    results = []
    
    # Tires Inspection
    print("\n- : Starting the Tire Inspection : -\n")
    speak("Starting the tire inspection.")
    results.append("Tires Inspection")
    tires_questions = [
        ("1. Left Front Tire Pressure: ", None),
        ("2. Right Front Tire Pressure: ", None),
        ("3. Left Front Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
        ("4. Right Front Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
        ("5. Left Rear Tire Pressure: ", None),
        ("6. Right Rear Tire Pressure: ", None),
        ("7. Left Rear Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
        ("8. Right Rear Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
        ("9. Overall Tire Summary (up to 1000 characters): ", None)
    ]
    parts_questions("Tire",tires_questions,results)
    # for question, options in tires_questions:
    #     answer = ask_question(question, options)
    #     if answer is not None:
    #         results.append(f"Tire - {question} {answer}")
    #         print("Hi",question.lower())
    #         if "image" in question.lower():
    #             image = capture_image("Tire", question)
    #             results.append(f"Image captured: {image}")

    # Battery Inspection
    print("\n- : Starting the Battery Inspection : -\n")
    speak("Starting the battery inspection.")
    results.append("Battery Inspection")
    battery_questions = [
        ("1. Battery Make: ", None),
        ("2. Battery Replacement Date: ", None),
        ("3. Battery Voltage (e.g., 12V, 13V): ", None),
        ("4. Battery Water Level (Good, Acceptable, Needs Water): ", ["good", "acceptable", "needs water"]),
        ("5. Rust, Dents or Damage in Battery (Heavy, Moderate, Acceptable): ", ["heavy", "moderate","acceptable"]),
        ("6. Battery Overall Summary (up to 1000 characters): ", None)
    ] 
    parts_questions("Battery",battery_questions,results)
    # for question, options in battery_questions:
    #     answer = ask_question(question, options)
    #     if answer is not None:
    #         results.append(f"Battery - {question} {answer}")
    #         if "image" in question.lower():
    #             image = capture_image("Battery", question)
    #             results.append(f"Image captured: {image}")

    # Exterior Inspection
    print("\n- : Starting the Exterior Inspection : -\n")
    speak("Starting the exterior inspection.")
    results.append("Exterior Inspection")
    exterior_questions = [
        ("1. Rust, Dent or Damage to Exterior (Heavy, Moderate, Acceptable): ", ["heavy", "moderate","acceptable"]),
        ("2. Oil Leak in Suspension (Heavy, Moderate, Acceptable): ", ["heavy", "moderate","acceptable"]),
        ("3. Overall Summary (up to 1000 characters): ", None)
    ]
    # parts_questions("Exterior",exterior_questions,results)
    # for question, options in exterior_questions:
    #     answer = ask_question(question, options)
    #     if answer is not None:
    #         results.append(f"Exterior - {question} {answer}")
    #         if "image" in question.lower():
    #             image = capture_image("Exterior", question)
    #             results.append(f"Image captured: {image}")

    # Brakes Inspection
    print("\n- : Starting the Brakes Inspection : -\n")
    speak("Starting the brakes inspection.")
    results.append("Brakes Inspection")
    brakes_questions = [
        ("1. Brake Fluid Level (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
        ("2. Brake Condition for Front (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
        ("3. Brake Condition for Rear (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
        ("4. Emergency Brake (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
        ("5. Brake Overall Summary (up to 1000 characters): ", None)
    ]
    # parts_questions("Brakes",brakes_questions,results)
    # for question, options in brakes_questions:
    #     answer = ask_question(question, options)
    #     if answer is not None:
    #         results.append(f"Brakes - {question} {answer}")
    #         if "image" in question.lower():
    #             image = capture_image("Brakes", question)
    #             results.append(f"Image captured: {image}")

    # Engine Inspection
    print("\n- : Starting the Engine Inspection : -\n")
    speak("Starting the engine inspection.")
    results.append("Engine Inspection")
    engine_questions = [
        ("1. Rust, Dents or Damage in Engine (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
        ("2. Engine Oil Condition (Good/Needs Replacement): ", ["good", "needs replacement"]),
        ("3. Engine Oil Color (Clean/Brown/Black): ", ["clean", "brown", "black"]),
        ("4. Brake Fluid Condition (Good/Needs Replacement): ", ["good", "needs replacement"]),
        ("5. Brake Fluid Color (Clean/Brown/Black): ", ["clean", "brown", "black"]),
        ("6. Any Oil Leak in Engine (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
        ("7. Overall Summary (up to 1000 characters): ", None)
    ]
    # parts_questions("Engine",engine_questions,results)
    # for question, options in engine_questions:
    #     answer = ask_question(question, options)
    #     if answer is not None:
    #         results.append(f"Engine - {question} {answer}")
    #         if "image" in question.lower():
    #             image = capture_image("Engine", question)
    #             results.append(f"Image captured: {image}")

    return results

def save_results(results):
    """Save the inspection results to a file."""
    with open("inspection_results.txt", "a") as file:
        for result in results:
            file.write(result + "\n")

def main():
    """Main function to run the inspection process."""
    results = perform_inspection()
    save_results(results)
    speak("Inspection completed. Results have been saved.")
    print("Inspection completed. Results have been saved.")

if __name__ == "__main__":
    main()




# import speech_recognition as sr
# import pyttsx3
# import time

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# def speak(text):
#     time.sleep(1)
#     engine.say(text)
#     engine.runAndWait()

# # Initialize the speech recognizer
# recognizer = sr.Recognizer()

# def normalize_command(command):
#     """Normalize the command by converting to lower case and stripping whitespace."""
#     return command.lower().strip() if command else ""

# def listen_for_command(timeout=5):
#     """Listen for a command with a specified timeout."""
#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source, duration=1)
#         print("Listening...")
#         try:
#             audio = recognizer.listen(source, timeout=timeout)
#             command = recognizer.recognize_google(audio)
#             print(f"Command received: {command}")
#             return command
#         except sr.UnknownValueError:
#             print("Sorry, I did not understand that.")
#             return None
#         except sr.WaitTimeoutError:
#             print("Listening timed out.")
#             return None
#         except sr.RequestError as e:
#             print(f"Sorry, there was an error with the speech recognition service: {e}")
#             return None
# def ask_question(question, options=None, retries=3):
#     """Ask a question and listen for a response, retrying if necessary."""
#     for attempt in range(retries):
#         speak(question)
#         print(question)
#         if options:
#             speak("Possible answers are: " + ", ".join(options))
        
#         response = listen_for_command(timeout=10)
        
#         if response is not None:
#             normalized_response = normalize_command(response)
#             if options and normalized_response not in options:
#                 speak("Invalid response. Please choose from: " + ", ".join(options))
#                 print("Invalid response. Please choose from: " + ", ".join(options))
#             else:
#                 return normalized_response
        
#         speak("Sorry, I didn't catch that. Please try again.")
#         print("Sorry, I didn't catch that. Please try again.")
    
#     # If all attempts fail, you might want to handle this case explicitly
#     speak("I am unable to understand your response. Please check your input.")
#     print("Unable to understand response after multiple attempts.")
#     return None

# # def ask_question(question, options=None):
# #     """Ask a question and listen for a response."""
# #     speak(question)
# #     print(question)
# #     if options:
# #         speak("Possible answers are: " + ", ".join(options))
# #     response = listen_for_command(timeout=10)
# #     return normalize_command(response)

# def capture_image(section, part):
#     """Simulate image capture and save the image with a specific name."""
#     print(f"Please capture an image for {section} - {part}.")
#     speak(f"Capture an image for {section} - {part}.")
#     # This is where you would integrate your image capture code
#     # For now, just simulating it with a placeholder
#     return f"{section}_{part}.jpg"

# def perform_inspection():
#     """Perform the complete inspection process."""
#     results = []
    
#     # Tires Inspection
#     speak("Starting the tire inspection.")
#     print("\n- : Starting the tire Inspection : -\n")
#     results.append("Tires Inspection")
#     tires_questions = [
#         ("Left Front Tire Pressure: ", None),
#         ("Right Front Tire Pressure: ", None),
#         ("Left Front Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
#         ("Right Front Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
#         ("Left Rear Tire Pressure: ", None),
#         ("Right Rear Tire Pressure: ", None),
#         ("Left Rear Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
#         ("Right Rear Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
#         ("Overall Tire Summary (up to 1000 characters): ", None)
#     ]
#     for question, options in tires_questions:
#         answer = ask_question(question, options)
#         results.append(f"Tire - {question} {answer}")
#         if "image" in question.lower():
#             image = capture_image("Tire", question)
#             results.append(f"Image captured: {image}")

#     # Battery Inspection
#     speak("Starting the battery inspection.")
#     print("\n- : Starting the battery Inspection : -\n")
#     results.append("Battery Inspection")
#     battery_questions = [
#         ("Battery Make: ", None),
#         ("Battery Replacement Date: ", None),
#         ("Battery Voltage (e.g., 12V, 13V): ", None),
#         ("Battery Water Level (Good, acceptable, Less): ", ["good", "acceptable", "low"]),
#         ("Condition of Battery (Any damage? Y/N): ", ["yes", "no"]),
#         ("Any Leak/Rust in Battery (Heavy, Moderate, Acceptable): ", ["yes", "no"]),
#         ("Battery Overall Summary (up to 1000 characters): ", None)
#     ]
#     for question, options in battery_questions:
#         answer = ask_question(question, options)
#         results.append(f"Battery - {question} {answer}")
#         if "image" in question.lower():
#             image = capture_image("Battery", question)
#             results.append(f"Image captured: {image}")

#     # Exterior Inspection
#     speak("Starting the exterior inspection.")
#     print("\n- : Starting the exterior Inspection : -\n")
#     results.append("Exterior Inspection")
#     exterior_questions = [
#         ("Rust, Dent or Damage to Exterior (Heavy, Moderate, Acceptable): ", ["yes", "no"]),
#         ("Oil Leak in Suspension (Heavy, Moderate, Acceptable): ", ["yes", "no"]),
#         ("Overall Summary (up to 1000 characters): ", None)
#     ]
#     for question, options in exterior_questions:
#         answer = ask_question(question, options)
#         results.append(f"Exterior - {question} {answer}")
#         if "image" in question.lower():
#             image = capture_image("Exterior", question)
#             results.append(f"Image captured: {image}")

#     # Brakes Inspection
#     speak("Starting the brakes inspection.")
#     print("\n- : Starting the brakes Inspection : -\n")
#     results.append("Brakes Inspection")
#     brakes_questions = [
#         ("Brake Fluid Level (Good, acceptable, Less): ", ["good", "acceptable", "low"]),
#         ("Brake Condition for Front (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
#         ("Brake Condition for Rear (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
#         ("Emergency Brake (Good, acceptable, Less): ", ["good", "acceptable", "low"]),
#         ("Brake Overall Summary (up to 1000 characters): ", None)
#     ]
#     for question, options in brakes_questions:
#         answer = ask_question(question, options)
#         results.append(f"Brakes - {question} {answer}")
#         if "image" in question.lower():
#             image = capture_image("Brakes", question)
#             results.append(f"Image captured: {image}")

#     # Engine Inspection
#     speak("Starting the engine inspection.")
#     print("\n- : Starting the engine Inspection : -\n")
#     results.append("Engine Inspection")
#     engine_questions = [
#         ("Rust, Dents or Damage in Engine (Heavy, Moderate, Acceptable): ", ["yes", "no"]),
#         ("Engine Oil Condition (Good/Bad): ", ["good", "bad"]),
#         ("Engine Oil Color (Clean/Brown/Black): ", ["clean", "brown", "black"]),
#         ("Brake Fluid Condition (Good/Bad): ", ["good", "bad"]),
#         ("Brake Fluid Color (Clean/Brown/Black): ", ["clean", "brown", "black"]),
#         ("Any Oil Leak in Engine (Heavy, Moderate, Acceptable): ", ["yes", "no"]),
#         ("Overall Summary (up to 1000 characters): ", None)
#     ]
#     for question, options in engine_questions:
#         answer = ask_question(question, options)
#         results.append(f"Engine - {question} {answer}")
#         if "image" in question.lower():
#             image = capture_image("Engine", question)
#             results.append(f"Image captured: {image}")

#     return results

# def save_results(results):
#     """Save the inspection results to a file."""
#     with open("inspection_results.txt", "a") as file:
#         for result in results:
#             file.write(result + "\n")

# def main():
#     """Main function to run the inspection process."""
#     results = perform_inspection()
#     save_results(results)
#     speak("Inspection completed. Results have been saved.")
#     print("Inspection completed. Results have been saved.")

# if __name__ == "__main__":
#     main()
