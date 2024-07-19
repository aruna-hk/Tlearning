#!/usr/bin/python3
import PyPDF2

def split_pdf(input_pdf, output_folder):
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        
        for page_num in range(num_pages):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[page_num])
            
            output_pdf = f"{output_folder}/chapter_{page_num + 1}.pdf"
            
            with open(output_pdf, 'wb') as out:
                writer.write(out)
    return num_pages
