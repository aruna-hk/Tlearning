#!/usr/bin/python3
import fitz  # PyMuPDF

def pdf_to_images(pdf_file, output_folder):
    # Open the provided PDF file
    pdf_document = fitz.open(pdf_file)
    
    # Iterate over each page in the PDF
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_number)
        
        # Convert page to image
        pix = page.get_pixmap()
        
        # Save the image with a proper name
        image_path = f"{output_folder}/page_{page_number + 1}.png"
        pix.writePNG(image_path)
        
        print(f"Page {page_number + 1} saved as {image_path}")
    
    # Close the PDF document
    pdf_document.close()

# Example usage:
pdf_file_path = "/home/hk/inet/unix_netprog_v1.pdf"
output_folder_path = "unix"

pdf_to_images(pdf_file_path, output_folder_path)

