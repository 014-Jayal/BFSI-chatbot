from fpdf import FPDF
import os

def generate_sanction_letter(customer):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Sanction Letter", ln=True, align="C")
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Dear {customer['name']},\n\nYour personal loan request has been approved. Pre-approved amount: Rs.{customer['pre_approved_limit']:.0f}.\n\nThank you for choosing our services.\n\nBest regards,\nBFSI NBFC Team")
    os.makedirs("outputs", exist_ok=True)
    filename = f"outputs/sanction_{customer['name'].replace(' ','_')}.pdf"
    pdf.output(filename, 'F')
    return filename
