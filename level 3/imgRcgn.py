import cv2
import numpy as np
import tensorflow as tf
import pyttsx3
import speech_recognition as sr
import time
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

recognizer = sr.Recognizer()

# Load pre-trained MobileNet model
model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=True)

# Load class labels for MobileNet
def load_labels():
    return tf.keras.applications.mobilenet_v2.decode_predictions(np.zeros((1, 1000)))[0]

labels = load_labels()

def speak(text):
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)

def listen_for_command(timeout=5):
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

def ask_question(question, options=None, retries=3):
    for attempt in range(retries):
        print(question)
        speak(question)
        
        response = listen_for_command(timeout=10)
        
        if response is not None:
            normalized_response = response.lower().strip()
            if options and normalized_response not in options:
                speak(f"Invalid response. Please choose from: {', '.join(options)}")
                print(f"Invalid response. Please choose from: {', '.join(options)}")
            else:
                return normalized_response
        
        speak("Sorry, I didn't catch that. Please try again.")
    
    speak("Unable to understand response after multiple attempts.")
    return None

def capture_image(section, part):
    """Simulate image capture."""
    print(f"Please capture an image for {section} - {part}.")
    speak(f"Capture an image for {section} - {part}.")
    # Placeholder for actual image capture code
    image_filename = f"{section}_{part}.jpg"
    # Simulate image capture error
    if not os.path.exists(image_filename):
        print(f"Error: Image file {image_filename} does not exist.")
        speak(f"Error: Image capture failed for {section} - {part}.")
        return None
    else:
        speak(f"Image captured: {image_filename}")
        return image_filename

def detect_object(frame):
    """Detect objects in the frame using MobileNet."""
    resized_frame = cv2.resize(frame, (224, 224))
    preprocessed_frame = tf.keras.applications.mobilenet_v2.preprocess_input(resized_frame)
    preprocessed_frame = np.expand_dims(preprocessed_frame, axis=0)

    predictions = model.predict(preprocessed_frame)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)[0]

    return decoded_predictions

def is_correct_part(frame, expected_part):
    """Check if the detected object matches the expected part."""
    predictions = detect_object(frame)
    for _, label, _ in predictions:
        if expected_part.lower() in label.lower():
            return True
    return False

def parts_questions(part_name, parts_ques, results):
    for question, options in parts_ques:
        answer = ask_question(question, options)
        if answer is not None:
            results.append(f"{part_name} - {question} {answer}")
            if "image" in question.lower():
                image = capture_image(part_name, question)
                if image:
                    results.append(f"Image captured: {image}")

def perform_inspection():
    results = []
    
    inspections = [
        ("Tire", [
            ("1. Left Front Tire Pressure: ", None),
            ("2. Right Front Tire Pressure: ", None),
            ("3. Left Front Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("4. Right Front Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("5. Left Rear Tire Pressure: ", None),
            ("6. Right Rear Tire Pressure: ", None),
            ("7. Left Rear Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("8. Right Rear Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("9. Overall Tire Summary (up to 1000 characters): ", None)
        ]),
        ("Battery", [
            ("1. Battery Make: ", None),
            ("2. Battery Replacement Date: ", None),
            ("3. Battery Voltage (e.g., 12V, 13V): ", None),
            ("4. Battery Water Level (Good, Acceptable, Needs Water): ", ["good", "acceptable", "needs water"]),
            ("5. Rust, Dents or Damage in Battery (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
            ("6. Battery Overall Summary (up to 1000 characters): ", None)
        ]),
        ("Exterior", [
            ("1. Rust, Dent or Damage to Exterior (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
            ("2. Oil Leak in Suspension (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
            ("3. Overall Summary (up to 1000 characters): ", None)
        ]),
        ("Brakes", [
            ("1. Brake Fluid Level (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("2. Brake Condition for Front (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("3. Brake Condition for Rear (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("4. Emergency Brake (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("5. Brake Overall Summary (up to 1000 characters): ", None)
        ]),
        ("Engine", [
            ("1. Rust, Dents or Damage in Engine (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
            ("2. Engine Oil Condition (Good/Needs Replacement): ", ["good", "needs replacement"]),
            ("3. Engine Oil Color (Clean/Brown/Black): ", ["clean", "brown", "black"]),
            ("4. Brake Fluid Condition (Good/Needs Replacement): ", ["good", "needs replacement"]),
            ("5. Brake Fluid Color (Clean/Brown/Black): ", ["clean", "brown", "black"]),
            ("6. Any Oil Leak in Engine (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
            ("7. Overall Summary (up to 1000 characters): ", None)
        ])
    ]

    for part_name, questions in inspections:
        print(f"\n- : Starting the {part_name} Inspection : -\n")
        speak(f"Starting the {part_name} inspection.")
        results.append(f"{part_name} Inspection")

        # Check if technician is in front of the part
        capture_device = cv2.VideoCapture(0)  # Use the pocket camera
        while True:
            ret, frame = capture_device.read()
            if not ret:
                print("Failed to capture image.")
                continue

            if is_correct_part(frame, part_name):
                speak(f"You are in front of the {part_name}.")
                results.append(f"Technician confirmed they are in front of the {part_name}.")
                break
            else:
                speak(f"Please move to the {part_name}.")
                print(f"Please move to the {part_name}.")

        capture_device.release()
        cv2.destroyAllWindows()

        # Proceed with questions for the part
        parts_questions(part_name, questions, results)

        confirm = ask_question(f"Have you completed the {part_name} inspection? (Yes/No)", ["yes", "no"])
        if confirm == "no":
            speak(f"Please complete the {part_name} inspection before proceeding.")
            print(f"Please complete the {part_name} inspection before proceeding.")
            return []

    return results

def save_results_to_pdf(results):
    """Save the inspection results to a PDF file."""
    pdf_filename = "inspection_results.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, "Inspection Results")
    y_position = height - 120

    for result in results:
        if y_position < 100:
            c.showPage()
            y_position = height - 100
        c.drawString(100, y_position, result)
        y_position -= 20

    c.save()
    print(f"Results saved to {pdf_filename}")

if __name__ == "__main__":
    print("Inspection system starting...")
    speak("Inspection system starting.")
    results = perform_inspection()
    if results:
        save_results_to_pdf(results)
    else:
        print("Inspection was not completed.")
        speak("Inspection was not completed.")
