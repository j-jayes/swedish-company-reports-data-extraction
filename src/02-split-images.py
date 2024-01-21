import cv2
import numpy as np
import os


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

import cv2
import numpy as np

def split_image_at_spine_with_buffer(image_path, num_bands=100, margin=10, buffer=10):
    """
    Splits an image at the spine by analyzing vertical bands and locating the band with the lowest average intensity.
    Adds a buffer to avoid cutting too close to the text.
    
    :param image_path: The file path of the image to be split.
    :param num_bands: The number of vertical bands to divide the image into for analysis.
    :param margin: The number of pixels to exclude from the edge of the detected spine to avoid cutting text.
    :param buffer: The number of pixels to add back as a buffer to prevent text clipping.
    :return: Paths to the saved images of the left and right pages.
    """
    
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Define the width of the bands
    band_width = gray.shape[1] // num_bands

    # Calculate the average pixel intensity for each band
    average_intensity = np.array([np.mean(gray[:, i*band_width:(i+1)*band_width]) for i in range(num_bands)])

    # Locate the band with the lowest average intensity, which should correspond to the spine
    spine_band_index = np.argmin(average_intensity)

    # Calculate the left and right cut points based on the spine band index
    left_cut = spine_band_index * band_width
    right_cut = (spine_band_index + 1) * band_width

    # Add a margin to avoid cutting text and add the buffer
    left_cut = max(0, left_cut - margin + buffer)
    right_cut = min(gray.shape[1], right_cut + margin - buffer)

    # Cut the image into two halves using the left and right cut points
    left_half = image[:, :left_cut]
    right_half = image[:, right_cut:]

    # Define the paths for saving the split images
    left_page_path = image_path.replace('.jpeg', '_left_page_with_buffer.jpeg')
    right_page_path = image_path.replace('.jpeg', '_right_page_with_buffer.jpeg')

    try:
        # Save the split images
        cv2.imwrite(left_page_path, left_half)
        cv2.imwrite(right_page_path, right_half)
    except cv2.error as e:
        print(f"Error occurred while saving the split images: {e}, {left_page_path}")

    return left_page_path, right_page_path


def split_images(company_name):
    input_directory = f"./data/companies/{company_name}"
    pdfs_paths = get_pdfs(company_name)

    for pdf_path in pdfs_paths:
        year = extract_year_from_filename(pdf_path)
        input_directory = f"./data/companies/{company_name}/{year}/single_pages"
        images_paths = [os.path.join(input_directory, file) for file in os.listdir(input_directory) if file.endswith(".jpeg")]

        for image_path in images_paths:
            split_image_at_spine_with_buffer(image_path)

# use the function
company_name = "Electrolux"
split_images(company_name)
