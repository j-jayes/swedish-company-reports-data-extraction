import pandas as pd
import os
import PyPDF2
import fitz  # PyMuPDF
from PIL import Image

company_name = "Electrolux"

# Function to get the list of PDFs in the specified directory
def get_pdfs(company_name):
    input_directory = f"./data/companies/{company_name}"
    pdfs_paths = [os.path.join(input_directory, file) for file in os.listdir(input_directory) if file.endswith(".pdf")]
    return pdfs_paths


# Function to extract the year from a file name
def extract_year_from_filename(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    year = file_name[-4:]
    if year.isdigit() and 1900 <= int(year) <= 2030:
        return year
    else:
        raise ValueError("Invalid year in file name")

# # Function to count the number of pages in each PDF file for each year
# def count_pdf_pages(company_name):
#     pdfs = get_pdfs(company_name)
#     pdfs_dict = {}
#     for pdf in pdfs:
#         year = extract_year_from_filename(pdf)
#         year = int(year)
#         pdf_reader = PyPDF2.PdfReader(pdf)
#         # use pdf_reader.pages to get the number of pages
#         pdfs_dict[year] = len(pdf_reader.pages)

#     return pdfs_dict

# # use function to count pages
# dict = count_pdf_pages(company_name)

# # arrange the dictionary into a dataframe
# df = pd.DataFrame.from_dict(dict, orient='index', columns=['pages'])

# # arrange the dataframe by year
# df = df.sort_index()

# df.to_csv(f"./data/companies/{company_name}/pages.csv")

# Function to create folders for each year
def create_year_folders(company_name):
    pdfs = get_pdfs(company_name)
    for pdf in pdfs:
        year = extract_year_from_filename(pdf)
        output_directory = f"./data/companies/{company_name}/{year}"
        os.makedirs(output_directory, exist_ok=True)

# Function to split a PDF into single-page PDFs
def split_pdf_pages(company_name):
    input_directory = f"./data/companies/{company_name}"
    pdfs_paths = get_pdfs(company_name)

    for pdf_path in pdfs_paths:
        year = extract_year_from_filename(pdf_path)
        output_directory = f"./data/companies/{company_name}/{year}/single_pages"
        os.makedirs(output_directory, exist_ok=True)

        pdf_reader = PyPDF2.PdfReader(pdf_path)
        for page_number, page in enumerate(pdf_reader.pages, start=1):
            output_pdf = PyPDF2.PdfWriter()
            output_pdf.add_page(page)
            output_file_path = os.path.join(output_directory, f"{company_name}_{year}_page_{page_number}.pdf")
            with open(output_file_path, "wb") as output_file:
                output_pdf.write(output_file)



# Function to convert a single-page PDF to JPEG
def convert_pdf_to_jpeg(pdf_path, jpeg_path, dpi=300):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)

    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    image.save(jpeg_path, "JPEG", quality=100)

    doc.close()
    image.close()

    temp_png = "temp.png"
    if os.path.exists(temp_png):
        os.remove(temp_png)


# Function to convert a PDF page into an image
def single_pdf_to_image(company_name):
    input_directory = f"./data/companies/{company_name}"
    pdfs_paths = get_pdfs(company_name)

    for pdf_path in pdfs_paths:
        year = extract_year_from_filename(pdf_path)
        # path to loop through to convert single page PDFs to images
        path_to_loop = f"./data/companies/{company_name}/{year}/single_pages"
        for root, dirs, files in os.walk(path_to_loop):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_path = os.path.join(root, file)
                    jpeg_path = pdf_path.replace('.pdf', '.jpeg')
                    convert_pdf_to_jpeg(pdf_path, jpeg_path)

# Main function to process all PDFs for a company
def process_company_pdfs(company_name):
    create_year_folders(company_name)
    split_pdf_pages(company_name)
    single_pdf_to_image(company_name)

# Run the process
process_company_pdfs(company_name)
