from fpdf import FPDF
import os
import datetime

class ForensicReport(FPDF):
    def header(self):
        # Official Header
        self.set_font("helvetica", "B", 16)
        self.set_text_color(18, 25, 38) # Dark Slate
        self.cell(0, 10, "EVO-FORENSIC INTELLIGENCE SUITE", align="C", ln=True)
        self.set_font("helvetica", "I", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "CONFIDENTIAL / LAW ENFORCEMENT SENSITIVE", align="C", ln=True)
        self.ln(10)

    def footer(self):
        # Footer with page numbers and timestamp
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cell(0, 10, f"Generated: {timestamp} | Page {self.page_no()}", align="C")

def generate_suspect_pdf(meta, match_score, image_path):
    """Generates a formatted PDF report and returns the file path."""
    pdf = ForensicReport()
    pdf.add_page()
    
    # 1. Subject Photo (Placed on the left)
    if os.path.exists(image_path):
        pdf.image(image_path, x=15, y=35, w=50)
    
    # 2. Basic Information (Placed next to the photo)
    pdf.set_xy(70, 35)
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"SUBJECT: {meta.get('full_name', 'UNKNOWN').upper()}", ln=True)
    
    pdf.set_x(70)
    pdf.set_font("helvetica", "", 11)
    pdf.cell(0, 8, f"Status: {meta.get('status', 'Unknown')}", ln=True)
    
    pdf.set_x(70)
    aliases = ", ".join(meta.get('aliases', []))
    pdf.cell(0, 8, f"Known Aliases: {aliases}", ln=True)
    
    pdf.set_x(70)
    pdf.cell(0, 8, f"Biometric Match Score: {match_score:.4f} (Cosine Dist)", ln=True)

    # 3. Move cursor below the image for the dossier
    pdf.set_y(95)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "INTELLIGENCE DOSSIER", ln=True)
    pdf.line(15, 105, 195, 105) # Draw a divider line
    pdf.ln(5)
    
    # 4. Inject the RAG text
    pdf.set_font("helvetica", "", 11)
    dossier_text = meta.get('intelligence_dossier', 'No records available.')
    # Multi_cell handles text wrapping automatically
    pdf.multi_cell(0, 7, dossier_text) 
    
    # 5. Save the PDF to a temporary path
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_dir = os.path.join(base_dir, "data", "temp_reports")
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{meta.get('full_name', 'Suspect').replace(' ', '_')}_Report.pdf"
    output_path = os.path.join(output_dir, filename)
    
    pdf.output(output_path)
    return output_path