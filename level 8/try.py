import tkinter as tk
from tkinter import messagebox

def open_fill_details_window():
    """Open the fill details window with a form."""
    fill_details_window = tk.Toplevel(root)
    fill_details_window.title("Fill Details")
    fill_details_window.geometry("600x400")
    fill_details_window.configure(bg="#2C2C2C")
    
    # Create a form frame
    form_frame = tk.Frame(fill_details_window, bg="#2C2C2C")
    form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    tk.Label(form_frame, text="Enter your details:", font=("Arial", 14), bg="#2C2C2C", fg="#FFFFFF").pack(pady=10)
    
    # Form fields
    labels = ["Inspection ID", "Inspector Name", "Inspection Date", "Comments"]
    entries = {}
    
    for label in labels:
        tk.Label(form_frame, text=label + ":", font=("Arial", 12), bg="#2C2C2C", fg="#FFFFFF").pack(anchor="w", padx=5)
        entry = tk.Entry(form_frame, font=("Arial", 12))
        entry.pack(fill=tk.X, padx=5, pady=5)
        entries[label] = entry

    def submit_details():
        details = {label: entry.get() for label, entry in entries.items()}
        print("Submitted Details:", details)  # Debugging print statement
        fill_details_window.destroy()

    tk.Button(form_frame, text="Submit", command=submit_details, font=("Arial", 14), bg="#4CAF50", fg="#FFFFFF").pack(pady=10)

# Setup tkinter GUI
root = tk.Tk()
root.title("Inspection System")
root.geometry("900x700")
root.configure(bg="#2C2C2C")

# Test button to open form
test_button = tk.Button(root, text="Open Form", command=open_fill_details_window, font=("Arial", 14))
test_button.pack(pady=20)

root.mainloop()
