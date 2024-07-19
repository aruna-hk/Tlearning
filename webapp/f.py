#!/usr/bin/python3
import os
from PIL import Image
import fitz  # PyMuPDF

def pdf_to_images(pdf_file, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the provided PDF file
    pdf_document = fitz.open(pdf_file)

    # Iterate over each page in the PDF
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_number)

        # Convert page to image
        image = page_to_image(page)

        # Save the image
        image_path = os.path.join(output_folder, f"page_{page_number + 1}.png")
        image.save(image_path, 'PNG')

        print(f"Page {page_number + 1} saved as {image_path}")

    # Close the PDF document
    pdf_document.close()

def page_to_image(page):
    # Convert PDF page to PIL image
    img = page.get_pixmap()
    img_pil = Image.frombytes("RGB", [img.width, img.height], img.samples)
    return img_pil

# Example usage:
pdf_file_path = "/home/hk/inet/unix_netprog_v1.pdf"
output_folder_path = "unix"

pdf_to_images(pdf_file_path, output_folder_path)

