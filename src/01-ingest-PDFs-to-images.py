import pandas as pd
import os
import PyPDF2

company_name = "Electrolux"

# create a function that looks inside "data/companies/{company_name}" and returns a list of the PDFs inside
def get_pdfs(company_name):
    input_directory = f"./data/companies/{company_name}"
    # grab the files that end in .pdf
    pdfs_paths = [
        os.path.join(input_directory, file)
        for file in os.listdir(input_directory)
        if file.endswith(".pdf")
    ]
    return pdfs_paths

# create a function that extracts the year from the PDF file name
def extract_year_from_filename(file_path):
    # extract the file name without extension
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    # extract the year from the file name
    year = file_name[-4:]
    # validate the year is within the range 1900-2030
    if year.isdigit() and 1900 <= int(year) <= 2030:
        return year
    else:
        raise ValueError("Invalid year in file name")
    
# create a folder inside "data/companies/{company_name}" for each year
def create_year_folders(company_name):
    # get the list of PDFs
    pdfs = get_pdfs(company_name)
    # loop through the PDFs
    for pdf in pdfs:
        # extract the year from the PDF file name
        year = extract_year_from_filename(pdf)
        # create the output directory based on the year
        output_directory = f"./data/companies/{company_name}/{year}"
        os.makedirs(output_directory, exist_ok=True)


# Function to get the number of pages of the PDF documents.
def get_num_pages(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    return len(reader.pages)


def split_pdf_pages(company_name):
    # utility function
    # This function takes the pdfs from "data/companies/{company_name}" and splits them to one page per pdf and puts them in data/companies/{company_name}/{year}-split
    input_directory = f"./data/companies/{company_name}"
    # grab the files that end in .pdf
    pdfs_paths = [
        os.path.join(input_directory, file)
        for file in os.listdir(input_directory)
        if file.endswith(".pdf")
    ]

    for pdf_path in pdfs_paths:
        # extract the year from the PDF file name
        year = extract_year_from_filename(pdf_path)

        # create the output directory based on the year
        output_directory = f"./data/companies/{company_name}/{year}/single_page_pdfs"
        os.makedirs(output_directory, exist_ok=True)

        # set pages to save as all except the cover page by getting the number of pages in the pdf
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        pages = get_num_pages(pdf_path)
        pages_to_save = list(range(2, pages + 1))

        # split the pdf into pages
        for page_number in pages_to_save:
            output_pdf = PyPDF2.PdfWriter()
            output_pdf.add_page(pdf_reader.pages[page_number - 1])
            output_file_path = os.path.join(
                output_directory, f"{company_name}_{year}_page_{page_number}.pdf"
            )
            with open(output_file_path, "wb") as output_file:
                output_pdf.write(output_file)




import fitz  # PyMuPDF
from PIL import Image

def convert_pdf_to_jpeg(pdf_path, jpeg_path, dpi=300):
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Select the page you want to convert (0 is the first page)
    page = doc.load_page(0)

    # Set the DPI for higher quality output
    zoom = dpi / 72  # PDFs are normally 72 DPI
    mat = fitz.Matrix(zoom, zoom)

    # Render the page to an image (pixmap)
    pix = page.get_pixmap(matrix=mat)

    # Save the pixmap as a PNG
    pix.save("temp.png")

    # Open the PNG with Pillow and convert to JPEG
    image = Image.open("temp.png")
    image = image.convert('RGB')  # Convert to RGB
    image.save(jpeg_path, "JPEG", quality=100)  # Save as JPEG with high quality

    # Clean up
    doc.close()
    image.close()

