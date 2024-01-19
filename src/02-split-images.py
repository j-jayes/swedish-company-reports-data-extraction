import cv2
import numpy as np

def split_image_at_spine(image_path, num_bands=100, margin=10):
    """
    Splits an image at the spine by analyzing vertical bands and locating the band with the lowest average intensity.
    
    :param image_path: The file path of the image to be split.
    :param num_bands: The number of vertical bands to divide the image into for analysis.
    :param margin: The number of pixels to exclude from the edge of the detected spine to avoid cutting text.
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

    # Add a margin to avoid cutting text
    left_cut = max(0, left_cut - margin)
    right_cut = min(gray.shape[1], right_cut + margin)

    # Cut the image into two halves using the left and right cut points
    left_half = image[:, :left_cut]
    right_half = image[:, right_cut:]

    # Define the paths for saving the split images
    left_page_path = image_path.replace('.jpeg', '_left_page.jpeg')
    right_page_path = image_path.replace('.jpeg', '_right_page.jpeg')

    # Save the split images
    cv2.imwrite(left_page_path, left_half)
    cv2.imwrite(right_page_path, right_half)

    return left_page_path, right_page_path

# Example usage:
# left_page, right_page = split_image_at_spine('/path/to/your/image.jpeg')
