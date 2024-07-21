#!/usr/bin/python3
import os
from PIL import Image
import fitz

def pdf_to_images(pdf_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    pdf_document = fitz.open(pdf_file)
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)

        image = page_to_image(page)
        image_path = os.path.join(output_folder, f"page_{page_number + 1}.png")
        image.save(image_path, 'PNG')
    pdf_document.close()

def page_to_image(page):
    img = page.get_pixmap()
    img_pil = Image.frombytes("RGB", [img.width, img.height], img.samples)
    return img_pil
