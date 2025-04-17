import os
import time
import threading
import queue
import fitz  # PyMuPDF
import easyocr
import numpy as np  # Import NumPy
from deep_translator import GoogleTranslator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

# Queue for thread communication
message_queue = queue.Queue()

def select_pdf_file():
    """Opens file dialog to select a PDF file."""
    file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")])
    return file_path

def convert_pdf_to_images(pdf_path):
    """Converts each page of the PDF into an image (PIL Image objects)."""
    print("Converting PDF pages to images...")
    images = []
    try:
        pdf_document = fitz.open(pdf_path)
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
        pdf_document.close()
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
    return images

def extract_text_from_images(images):
    """Extracts text from each image using OCR (easyocr)."""
    extracted_text = []
    reader = easyocr.Reader(['de'])  # German OCR
    for i, img in enumerate(images):
        print(f"Extracting text from page {i + 1}...")
        # Convert PIL Image to NumPy array
        img_np = np.array(img)
        result = reader.readtext(img_np)
        page_text = ""
        for detection in result:
            page_text += detection[1] + " "
        extracted_text.append(page_text.strip())
    return extracted_text

def translate_text(text, target_language="en"):
    """Translates text to the target language."""
    translator = GoogleTranslator(source="auto", target=target_language)
    return translator.translate(text)

def overlay_translated_text_on_images(images, translated_texts, output_pdf):
    """Creates a new PDF with the translated text overlayed on the original images."""
    print("Overlaying translated text onto images...")

    c = canvas.Canvas(output_pdf, pagesize=letter)

    for i, (img, translated_text) in enumerate(zip(images, translated_texts)):
        img_path = f"temp_page_{i}.png"
        img.save(img_path, "PNG")  # Save image to overlay text

        c.drawImage(img_path, 0, 0, width=612, height=792)  # Adjust to fit page
        c.setFont("Helvetica", 12)
        c.setFillColorRGB(1, 0, 0)  # Red for translated text

        # Place translated text on the image
        lines = translated_text.split("\n")
        y_position = 700  # Adjust starting position
        for line in lines:
            c.drawString(50, y_position, line)
            y_position -= 20  # Adjust line spacing

        c.showPage()
        os.remove(img_path)  # Cleanup

    c.save()
    print(f"Translated PDF saved as: {output_pdf}")

def run_translation(pdf_path):
    """Runs the full translation process."""
    images = convert_pdf_to_images(pdf_path)
    extracted_texts = extract_text_from_images(images)

    translated_texts = []
    for i, text in enumerate(extracted_texts):
        print(f"Translating page {i + 1}...")
        translated_texts.append(translate_text(text))
        time.sleep(1)  # Avoid rate limits

    output_pdf = pdf_path.replace(".pdf", "_translated.pdf")
    overlay_translated_text_on_images(images, translated_texts, output_pdf)

    # Put the success message in the queue
    message_queue.put(f"Translated PDF saved at: {output_pdf}")

def main():
    """Main function to handle user interaction."""
    root = tk.Tk()  # Create Tk instance in the main thread
    root.withdraw() #hides the root window.

    pdf_path = select_pdf_file()
    if not pdf_path:
        messagebox.showerror("Error", "No file selected!")
        return

    translation_thread = threading.Thread(target=run_translation, args=(pdf_path,))
    translation_thread.start()

    def check_queue():
        """Checks the queue for messages and updates the GUI."""
        try:
            message = message_queue.get_nowait()
            messagebox.showinfo("Success", message)
            root.destroy() #close the mainloop.
        except queue.Empty:
            root.after(100, check_queue)  # Check again after 100ms

    check_queue()  # Start checking the queue
    root.mainloop() #start the mainloop.

if __name__ == "__main__":
    main()