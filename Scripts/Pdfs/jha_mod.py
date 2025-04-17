from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter

# Reprocess the file while keeping all original pages intact

# Reload the PDF
reader = PdfReader(r"C:\Users\PrasoonJose\Tribe Technology\11. Commissioning - Documents\General\Completed JSA's\JSA Form - Potting and Racking.pdf")

# Create a PdfWriter object
writer = PdfWriter()

# Add all pages
for i in range(len(reader.pages)):
    writer.add_page(reader.pages[i])  # Add original pages
    if i == 4:  # Page 4 in zero-based index (which is actually page 64 in document)
        writer.add_page(reader.pages[i])  # Duplicate as page 4

# Save the corrected modified PDF
corrected_pdf_path = r"C:\Users\PrasoonJose\Tribe Technology\11. Commissioning - Documents\General\Completed JSA's\JSA Form - Potting and Racking_mod.pdf"
with open(corrected_pdf_path, "wb") as output_pdf:
    writer.write(output_pdf)

corrected_pdf_path
