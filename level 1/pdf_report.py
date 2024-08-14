# pdf_report.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class PDFReport:
    def __init__(self, file_name):
        self.file_name = file_name
    
    def generate_pdf(self, content):
        c = canvas.Canvas(self.file_name, pagesize=letter)
        c.drawString(100, 750, "Inspection Report")
        text_object = c.beginText(100, 730)
        text_object.setFont("Helvetica", 12)
        text_object.setTextOrigin(100, 730)
        for line in content:
            text_object.textLine(line)
        c.drawText(text_object)
        c.save()
        print(f"PDF report generated: {self.file_name}")
