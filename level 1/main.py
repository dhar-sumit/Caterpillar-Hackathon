# main.py
from voice_recognition import VoiceRecognition
from image_capture import ImageCapture
from data_storage import DataStorage
from pdf_report import PDFReport

def main():
    voice_recognition = VoiceRecognition()
    image_capture = ImageCapture()
    data_storage = DataStorage(base_file_name="inspection_report")
    
    inspection_steps = [
        "Tires",
        "Battery",
        "Exterior",
        "Brakes",
        "Engine"
    ]
    
    for step in inspection_steps:
        print(f"Starting inspection for: {step}")
        command = voice_recognition.listen_for_command()
        print(f"Command received: {command}")
        data_storage.record_finding(f"Checked {step}", step)
        image_capture.capture_image(step)
        
        if "next" in command.lower():
            continue
        elif "finish" in command.lower():
            break
    
    report_content = [
        "Inspection Summary",
        "Tires: Checked",
        "Battery: Checked",
        "Exterior: Checked",
        "Brakes: Checked",
        "Engine: Checked"
    ]
    pdf_report = PDFReport(file_name="inspection_report.pdf")
    pdf_report.generate_pdf(report_content)

if __name__ == "__main__":
    main()
