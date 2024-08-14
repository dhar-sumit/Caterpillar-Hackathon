import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import messagebox
import pyttsx3
import speech_recognition as sr
import time
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import threading

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)

def listen_for_command(timeout=5):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        update_text("Listening...", 'alert')
        try:
            audio = recognizer.listen(source, timeout=timeout)
            command = recognizer.recognize_google(audio)
            update_text(f"Command received: {command}", 'command')
            return command
        except sr.UnknownValueError:
            update_text("Sorry, I did not understand that.", 'alert')
            return None
        except sr.WaitTimeoutError:
            update_text("Listening timed out.", 'alert')
            return None
        except sr.RequestError as e:
            update_text(f"Sorry, there was an error with the speech recognition service: {e}", 'alert')
            return None

def ask_question(question, options=None, retries=3):
    for attempt in range(retries):
        update_text(question, 'question')
        speak(question)
        
        response = listen_for_command(timeout=10)
        
        if response is not None:
            normalized_response = response.lower().strip()
            if options and normalized_response not in options:
                update_text(f"Invalid response. Please choose from: {', '.join(options)}", 'alert')
                speak(f"Invalid response. Please choose from: {', '.join(options)}")
            else:
                return normalized_response
        
        speak("Sorry, I didn't catch that. Please try again.")
    
    speak("Unable to understand response after multiple attempts.")
    return None

def capture_image(section, part):
    """Simulate image capture."""
    update_text(f"Please capture an image for {section} - {part}.", 'command')
    speak(f"Capture an image for {section} - {part}.")
    # Placeholder for actual image capture code
    image_filename = f"{section}_{part}.jpg"
    # Simulate image capture error
    if not os.path.exists(image_filename):
        update_text(f"Error: Image file {image_filename} does not exist.", 'alert')
        speak(f"Error: Image capture failed for {section} - {part}.")
        return None
    else:
        speak(f"Image captured: {image_filename}")
        return image_filename

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
        update_text(f"\n- : Starting the {part_name} Inspection : -\n", 'heading')
        speak(f"Starting the {part_name} inspection.")
        results.append(f"{part_name} Inspection")

        # Proceed with questions for the part
        parts_questions(part_name, questions, results)

        confirm = ask_question(f"Have you completed the {part_name} inspection? (Yes/No)", ["yes", "no"])
        if confirm == "no":
            speak(f"Please complete the {part_name} inspection before proceeding.")
            update_text(f"Please complete the {part_name} inspection before proceeding.", 'alert')
            return []

    return results

def save_results_to_pdf(results):
    """Save the inspection results to a PDF file."""
    pdf_filename = "inspection_results.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "Inspection Results")
    c.setFont("Helvetica", 12)
    y_position = height - 140

    for result in results:
        if y_position < 100:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 100
        c.drawString(100, y_position, result)
        y_position -= 20

    c.save()
    update_text(f"Results saved to {pdf_filename}", 'info')

def update_text(message, message_type='command'):
    """Update the text area with the message."""
    if message_type == 'heading':
        text_area.insert(tk.END, f"{message}\n", 'heading')
    elif message_type == 'question':
        text_area.insert(tk.END, f"{message}\n", 'question')
    elif message_type == 'alert':
        text_area.insert(tk.END, f"{message}\n", 'alert')
    else:
        text_area.insert(tk.END, f"{message}\n", 'command')

    text_area.yview(tk.END)
    root.update_idletasks()  # Ensure the GUI updates immediately

def on_close():
    root.destroy()

def start_inspection():
    """Start the inspection process in a separate thread to avoid blocking the GUI."""
    update_text("Inspection system starting...", 'info')
    speak("Inspection system starting.")
    results = perform_inspection()
    if results:
        save_results_to_pdf(results)
    else:
        update_text("Inspection was not completed.", 'alert')
        speak("Inspection was not completed.")

# Setup tkinter GUI
root = tk.Tk()
root.title("Inspection System")
root.geometry("900x700")
root.configure(bg="#2C2C2C")

# Define custom styles for text tags
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30, font=("Helvetica", 12), bg="#1E1E1E", fg="#FFFFFF", borderwidth=2, relief="sunken")
text_area.tag_configure('heading', font=("Helvetica", 16, "bold"), foreground="#FFD700")  # Gold color for headings
text_area.tag_configure('question', font=("Helvetica", 14, "italic"), foreground="#00BFFF")  # Deep Sky Blue for questions
text_area.tag_configure('command', font=("Helvetica", 12), foreground="#FFFFFF")  # White for regular commands
text_area.tag_configure('alert', font=("Helvetica", 12), foreground="#FF6347")  # Tomato color for alerts
text_area.tag_configure('info', font=("Helvetica", 12, "italic"), foreground="#32CD32")  # Lime Green for information

text_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Buttons Frame
buttons_frame = tk.Frame(root, bg="#2C2C2C")
buttons_frame.pack(fill=tk.X, pady=20)

# Start Inspection Button
start_button = tk.Button(buttons_frame, text="Start Inspection", command=lambda: threading.Thread(target=start_inspection, daemon=True).start(), font=("Helvetica", 16, "bold"), bg="#4CAF50", fg="#ffffff", relief="raised", bd=2, padx=20, pady=10)
start_button.pack(side=tk.LEFT, padx=20)

# Exit Button
exit_button = tk.Button(buttons_frame, text="Exit", command=on_close, font=("Helvetica", 16, "bold"), bg="#f44336", fg="#ffffff", relief="raised", bd=2, padx=20, pady=10)
exit_button.pack(side=tk.RIGHT, padx=20)

root.protocol("WM_DELETE_WINDOW", on_close)

# Start the GUI main loop
root.mainloop()

