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
import subprocess
import sys

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

recognizer = sr.Recognizer()

inspection_thread = None
inspection_running = threading.Event()
inspection_cancelled = threading.Event()

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
            update_text(f"Command received: {command}")
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

# def perform_inspection():
#     results = []

#     inspections = [
#         ("Tire", [
#             # ("\n1. Left Front Tire Pressure: ", None),
#             # ("\n2. Right Front Tire Pressure: ", None),
#             # ("\n3. Left Front Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
#             # ("\n4. Right Front Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),        
#             # ("\n5. Left Rear Tire Pressure: ", None),
#             # ("\n6. Right Rear Tire Pressure: ", None),
#             # ("\n7. Left Rear Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
#             # ("\n8. Right Rear Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
#             # ("\n9. Check for single shoulder wear : ", None)
#             ("\n10. Overall Tire Summary (up to 1000 characters): ", None)
#         ]),
#         ("Battery", [
#             # ("\n1. Battery Make: ", None),
#             # ("\n2. Battery Replacement Date: ", None),
#             # ("\n3. Battery Voltage (e.g., 12V, 13V): ", None),
#             # ("\n4. Battery Water Level (Good, Acceptable, Needs Water): ", ["good", "acceptable", "needs water"]),
#             # ("\n5. Rust, Dents or Damage in Battery (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
#             # ("\n6. Is the battery damaged or frayed? ", None),
#             # ("\n7. Will the battery be able to take the load? ", None),
#             # ("\n8. Is the battery internally fine? ", None),
#             # ("\n9. Are the parasitic draws checked? ", None),
#             ("\n10. Battery Overall Summary (up to 1000 characters): ", None)
#         ]),
#         ("Exterior", [
#             ("\n1. Rust, Dent or Damage to Exterior (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
#             ("\n2. Oil Leak in Suspension (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
#             ("\n3. Inspection underneath the machine for any signs of fluid leaks? ", None),
#             ("\n4. Are the lights and reflectors working fine? ", None),
#             ("\n5. Attachments are in working condition? ", None),
#             ("\n6. Overall Summary (up to 1000 characters): ", None)
#         ]),
#         ("Brakes", [
#             # ("\n1. Brake Fluid Level (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
#             # ("\n2. Brake Condition for Front (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
#             # ("\n3. Brake Condition for Rear (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
#             # ("\n4. Emergency Brake (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
#             # ("\n5. Brake disc (rotor) condition: ", None),
#             # ("\n6. Brake noise and vibration: ", None),
#             # ("\n7. Brake calipers are working: ", None),
#             # ("\n8. Brake Overall Summary (up to 1000 characters): ", None)
#         ]),
#         ("Engine", [
#             # ("\n1. Rust, Dents or Damage in Engine (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
#             # ("\n2. Engine Oil Condition (Good/Needs Replacement): ", ["good", "needs replacement"]),
#             # ("\n3. Engine Oil Color (Clean/Brown/Black): ", ["clean", "brown", "black"]),
#             # ("\n4. Brake Fluid Condition (Good/Needs Replacement): ", ["good", "needs replacement"]),
#             # ("\n5. Brake Fluid Color (Clean/Brown/Black): ", ["clean", "brown", "black"]),
#             # ("\n6. Any Oil Leak in Engine (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
#             # ("\n7. Have you checked compression of the engine? ", None),
#             # ("\n8. Is the air filter clean and free of debris? ", None),
#             # ("\n9. Is the cooling system working fine? ", None),
#             # ("\n10. Is there any blockage or leak in the engine oil? ", None),
#             ("\n11. Any abnormal noises such as tapping or knocking? ", None),
#             ("\n12. Overall Summary (up to 1000 characters): ", None)
#         ])
#     ]

def perform_inspection():
    results = []

    inspections = [
        ("Tire", [
            ("\n1. Left Front Tire Pressure: ", None),
            ("\n2. Right Front Tire Pressure: ", None),
            ("\n3. Left Front Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("\n4. Right Front Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),        
            ("\n5. Left Rear Tire Pressure: ", None),
            ("\n6. Right Rear Tire Pressure: ", None),
            ("\n7. Left Rear Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("\n8. Right Rear Tire Condition (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("\n9. Check for single shoulder wear : ", None),
            ("\n10. Overall Tire Summary (up to 1000 characters): ", None)
        ]),
        ("Battery", [
            ("\n1. Battery Make: ", None),
            ("\n2. Battery Replacement Date: ", None),
            ("\n3. Battery Voltage (e.g., 12V, 13V): ", None),
            ("\n4. Battery Water Level (Good, Acceptable, Needs Water): ", ["good", "acceptable", "needs water"]),
            ("\n5. Rust, Dents or Damage in Battery (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
            ("\n6. Is the battery damaged or frayed? ", None),
            ("\n7. Will the battery be able to take the load? ", None),
            ("\n8. Is the battery internally fine? ", None),
            ("\n9. Are the parasitic draws checked? ", None),
            ("\n10. Battery Overall Summary (up to 1000 characters): ", None)
        ]),
        ("Exterior", [
            ("\n1. Rust, Dent or Damage to Exterior (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
            ("\n2. Oil Leak in Suspension (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
            ("\n3. Inspection underneath the machine for any signs of fluid leaks? ", None),
            ("\n4. Are the lights and reflectors working fine? ", None),
            ("\n5. Attachments are in working condition? ", None),
            ("\n6. Overall Summary (up to 1000 characters): ", None)
        ]),
        ("Brakes", [
            ("\n1. Brake Fluid Level (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("\n2. Brake Condition for Front (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("\n3. Brake Condition for Rear (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("\n4. Emergency Brake (Good, Acceptable, Needs Replacement): ", ["good", "acceptable", "needs replacement"]),
            ("\n5. Brake disc (rotor) condition: ", None),
            ("\n6. Brake noise and vibration: ", None),
            ("\n7. Brake calipers are working: ", None),
            ("\n8. Brake Overall Summary (up to 1000 characters): ", None)
        ]),
        ("Engine", [
            ("\n1. Rust, Dents or Damage in Engine (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
            ("\n2. Engine Oil Condition (Good/Needs Replacement): ", ["good", "needs replacement"]),
            ("\n3. Engine Oil Color (Clean/Brown/Black): ", ["clean", "brown", "black"]),
            ("\n4. Brake Fluid Condition (Good/Needs Replacement): ", ["good", "needs replacement"]),
            ("\n5. Brake Fluid Color (Clean/Brown/Black): ", ["clean", "brown", "black"]),
            ("\n6. Any Oil Leak in Engine (Heavy, Moderate, Acceptable): ", ["heavy", "moderate", "acceptable"]),
            ("\n7. Have you checked compression of the engine? ", None),
            ("\n8. Is the air filter clean and free of debris? ", None),
            ("\n9. Is the cooling system working fine? ", None),
            ("\n10. Is there any blockage or leak in the engine oil? ", None),
            ("\n11. Any abnormal noises such as tapping or knocking? ", None),
            ("\n12. Overall Summary (up to 1000 characters): ", None)
        ])
    ]

    for part_name, questions in inspections:
        if inspection_cancelled.is_set():
            update_text("Inspection cancelled.", 'alert')
            return []

        update_text(f"\n- : Starting the {part_name} Inspection : -\n", 'heading')
        speak(f"Starting the {part_name} inspection.")
        results.append(f"{part_name} Inspection")

        # Proceed with questions for the part
        parts_questions(part_name, questions, results)

        while True:
            confirm = ask_question(f"\nHave you completed the {part_name} inspection? (Completed/Not Completed)", ["completed", "not completed"])
            if confirm == "completed":
                # Ask for the summary after confirmation of completion
                overall_summary_question = next((q for q, _ in questions if "Overall Summary" in q), None)
                if overall_summary_question:
                    summary = ask_question(overall_summary_question, retries=1)  # Ask once for summary
                    if summary:
                        results.append(f"{part_name} - {overall_summary_question} {summary}")
                break  # Proceed to the next part after receiving the summary
            else:
                speak(f"Please complete the {part_name} inspection before proceeding.")
                update_text(f"\nPlease complete the {part_name} inspection before proceeding.", 'alert')
                time.sleep(10)  # Wait before asking again

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
    """Handle the window close event."""
    print("Exit button pressed or window closed.")
    if inspection_running.is_set():
        inspection_cancelled.set()
    root.destroy()

def start_inspection():
    """Start the inspection process in a separate thread to avoid blocking the GUI."""
    global inspection_thread
    update_text("-: Inspection system starting :-", 'heading')
    speak("Inspection system starting.")
    
    if inspection_running.is_set():
        update_text("-: Inspection already running :-", 'alert')
        return
    
    inspection_running.set()
    inspection_cancelled.clear()
    inspection_thread = threading.Thread(target=run_inspection, daemon=True)
    inspection_thread.start()

def run_inspection():
    """Run the inspection process."""
    results = perform_inspection()
    if not inspection_cancelled.is_set():
        if results:
            save_results_to_pdf(results)
        else:
            update_text("-: Inspection was not completed :-", 'alert')
            speak("Inspection was not completed.")
    inspection_running.clear()

def restart_app():
    """Restart the application."""
    print("Restart button pressed.")
    root.destroy()
    # Explicitly provide the path to the script
    subprocess.Popen([sys.executable, "D:\\Hackathon\\level 8\\main.py"])

def on_hover(event):
    """Change button color and cursor on hover."""
    event.widget.config(bg=event.widget.hover_color, cursor="hand2")

def on_leave(event):
    """Reset button color and cursor on leave."""
    event.widget.config(bg=event.widget.original_color, cursor="arrow")

def create_button(text, command, bg_color="#4CAF50", hover_color="#45a049"):
    """Create a styled button with hover effects."""
    button = tk.Button(buttons_frame, text=text, command=command, font=("Arial", 14, "bold"), bg=bg_color, fg="#ffffff", relief="flat", bd=0, padx=20, pady=10)
    button.original_color = bg_color
    button.hover_color = hover_color
    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", on_leave)
    return button

def open_fill_details_window():
    """Open the fill details window with dark mode styling."""
    fill_details_window = tk.Toplevel(root)
    fill_details_window.title("Fill Details")
    fill_details_window.geometry("600x500")  # Increased height for larger form
    fill_details_window.configure(bg="#2C2C2C")  # Dark background color

    def submit_details():
        global header_info
        # Collect details from the placeholders
        details = {
            "Name": name_entry.get(),
            "Vehicle Make": make_entry.get(),
            "Model": model_entry.get(),
            "Year": year_entry.get(),
            "VIN": vin_entry.get()
        }
        # Ensure no field is empty or contains placeholder text
        if any(value == entry.placeholder or not value for key, value, entry in zip(details.keys(), details.values(), [name_entry, make_entry, model_entry, year_entry, vin_entry])):
            update_text("Please fill all fields before submitting.", 'alert')
            speak("Please fill all fields before submitting.")
            return

        header_info = details
        update_text("Details submitted. Click 'Start Inspection' to begin.", 'info')
        speak("Details submitted. Click 'Start Inspection' to begin.")
        start_button.config(state=tk.NORMAL)  # Enable Start Inspection button
        fill_details_window.destroy()

    def validate_fields(*args):
        # Check if any field is empty or contains only placeholder text
        if (name_var.get() == "" or name_var.get() == name_entry.placeholder or
            make_var.get() == "" or make_var.get() == make_entry.placeholder or
            model_var.get() == "" or model_var.get() == model_entry.placeholder or
            year_var.get() == "" or year_var.get() == year_entry.placeholder or
            vin_var.get() == "" or vin_var.get() == vin_entry.placeholder):
            submit_button.config(state=tk.DISABLED)
        else:
            submit_button.config(state=tk.NORMAL)

    def on_hover(event):
        """Change button color and cursor on hover."""
        event.widget.config(bg="#45a049", cursor="hand2")

    def on_leave(event):
        """Reset button color and cursor on leave."""
        event.widget.config(bg="#4CAF50", cursor="arrow")

    tk.Label(fill_details_window, text="Please fill in the details:", font=("Arial", 16), bg="#2C2C2C", fg="#FFFFFF").pack(pady=15)

    # Create StringVar for validation
    name_var = tk.StringVar()
    make_var = tk.StringVar()
    model_var = tk.StringVar()
    year_var = tk.StringVar()
    vin_var = tk.StringVar()

    # Attach validation to the StringVar
    for var in [name_var, make_var, model_var, year_var, vin_var]:
        var.trace_add("write", validate_fields)

    # Create Entry widgets with placeholders
    name_entry = PlaceholderEntry(fill_details_window, placeholder="Enter your name", textvariable=name_var, bg="#1E1E1E", fg="#FFFFFF", insertbackground='white', font=("Arial", 14))
    name_entry.pack(fill=tk.X, padx=20, pady=10)
    
    make_entry = PlaceholderEntry(fill_details_window, placeholder="Enter vehicle make", textvariable=make_var, bg="#1E1E1E", fg="#FFFFFF", insertbackground='white', font=("Arial", 14))
    make_entry.pack(fill=tk.X, padx=20, pady=10)
    
    model_entry = PlaceholderEntry(fill_details_window, placeholder="Enter vehicle model", textvariable=model_var, bg="#1E1E1E", fg="#FFFFFF", insertbackground='white', font=("Arial", 14))
    model_entry.pack(fill=tk.X, padx=20, pady=10)
    
    year_entry = PlaceholderEntry(fill_details_window, placeholder="Enter vehicle year", textvariable=year_var, bg="#1E1E1E", fg="#FFFFFF", insertbackground='white', font=("Arial", 14))
    year_entry.pack(fill=tk.X, padx=20, pady=10)
    
    vin_entry = PlaceholderEntry(fill_details_window, placeholder="Enter VIN", textvariable=vin_var, bg="#1E1E1E", fg="#FFFFFF", insertbackground='white', font=("Arial", 14))
    vin_entry.pack(fill=tk.X, padx=20, pady=10)

    submit_button = tk.Button(fill_details_window, text="Submit", command=submit_details, font=("Arial", 16, "bold"), bg="#4CAF50", fg="#FFFFFF", relief="flat", bd=0, padx=20, pady=15)
    submit_button.pack(pady=15)

    # Bind hover events to the submit button
    submit_button.bind("<Enter>", on_hover)
    submit_button.bind("<Leave>", on_leave)

    # Initialize submit button state
    validate_fields()


class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self._has_placeholder = True
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        self._set_placeholder()

    def _set_placeholder(self):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg="grey")
            self._has_placeholder = True

    def _on_focus_in(self, *args):
        if self._has_placeholder:
            self.delete(0, tk.END)
            self.config(fg="white")
            self._has_placeholder = False

    def _on_focus_out(self, *args):
        if not self.get():
            self._set_placeholder()

# Setup tkinter GUI
root = tk.Tk()
root.title("Inspection System")
root.geometry("900x700")
root.configure(bg="#2C2C2C")

# Define custom styles for text tags
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30, font=("Arial", 12), bg="#1E1E1E", fg="#FFFFFF", borderwidth=2, relief="flat")
text_area.tag_configure('heading', font=("Arial", 16, "bold"), foreground="#FFD700")  # Gold color for headings
text_area.tag_configure('question', font=("Arial", 14, "italic"), foreground="#00BFFF")  # Deep Sky Blue for questions
text_area.tag_configure('command', font=("Arial", 12), foreground="#FFFFFF")  # White for regular commands
text_area.tag_configure('alert', font=("Arial", 12), foreground="#FF6347")  # Tomato color for alerts
text_area.tag_configure('info', font=("Arial", 12, "italic"), foreground="#32CD32")  # Lime Green for information

text_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Buttons Frame
buttons_frame = tk.Frame(root, bg="#2C2C2C")
buttons_frame.pack(fill=tk.X, pady=20)

# Create Buttons
fill_details_button = create_button("Fill Details", open_fill_details_window)
fill_details_button.pack(side=tk.LEFT, padx=20)

start_button = create_button("Start Inspection", start_inspection, bg_color="#9E9E9E", hover_color="#757575")
start_button.config(state=tk.DISABLED)  # Initially disable the Start Inspection button
start_button.pack(side=tk.LEFT, padx=20)

restart_button = create_button("Restart", restart_app)
restart_button.pack(side=tk.LEFT, padx=20)

exit_button = create_button("Exit", on_close, bg_color="#f44336", hover_color="#d32f2f")
exit_button.pack(side=tk.RIGHT, padx=20)

root.protocol("WM_DELETE_WINDOW", on_close)

# Initialize header_info as None
header_info = None

# Start the GUI main loop
root.mainloop()
