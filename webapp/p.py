#!/usr/bin/python3
import os
from PyPDF2 import PdfReader
from PIL import Image

def pdf_to_images(pdf_file, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the provided PDF file
    with open(pdf_file, 'rb') as f:
        pdf = PdfReader(f)
        
        # Iterate over each page in the PDF
        for page_number in range(len(pdf.pages)):
            # Get the page
            page = pdf.pages[page_number]
            
            # Convert page to image
            image = page_to_image(page)
            
            # Save the image
            image_path = os.path.join(output_folder, f"page_{page_number + 1}.png")
            image.save(image_path, 'PNG')
            
            print(f"Page {page_number + 1} saved as {image_path}")

#def page_to_image(page):
    # Convert PDF page to PIL image
 #   bbox = page.mediabox  # Get the page bounding box
  #  img = Image.new('RGB', (int(bbox.width), int(bbox.height)), 'white')
   # img_pil = page.merge_page(img)
    #return img_pil

def page_to_image(page):
  """Converts a PDF page to a PIL image."""
  # Get the page size
  bbox = page.mediabox
  width = int(bbox.width)
  height = int(bbox.height)

  # Create a new RGB image
  img = Image.new('RGB', (width, height), 'white')

  # Get content stream and resources
  content = page.extract_text()
  resources = page['/Resources']

  return img

# Example usage:
pdf_file_path = "/home/hk/inet/unix_netprog_v1.pdf"
output_folder_path = "unix"

pdf_to_images(pdf_file_path, output_folder_path)
