import pandas as pd
import pytesseract
import os
from PIL import Image
import re

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


# Update the Tesseract executable path if necessary
# pytesseract.pytesseract.tesseract_cmd = r'path_to_tesseract.exe'  # Uncomment and update this line if needed

def extract_coordinates_from_image(image_path):
    """
    Extracts the latitude and longitude from an image using Tesseract OCR.
    Assumes coordinates are in the format 'Lat: <value> Long: <value>' or similar.
    """
    try:
        # Open the image using PIL
        img = Image.open(image_path)

        # Perform OCR to extract text
        ocr_text = pytesseract.image_to_string(img)

        # Search for latitude and longitude in the OCR text
        lat, lng = None, None
        lat_pattern = re.compile(r'(?:Lat|Latitude)[:\s]*([+-]?\d+\.?\d*)')
        long_pattern = re.compile(r'(?:Long|Longitude)[:\s]*([+-]?\d+\.?\d*)')

        # Find matches for latitude and longitude
        lat_match = lat_pattern.search(ocr_text)
        long_match = long_pattern.search(ocr_text)

        # Extract the values if matches are found
        lat = float(lat_match.group(1)) if lat_match else None
        lng = float(long_match.group(1)) if long_match else None

        return lat, lng
    
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None, None

def update_csv_with_coordinates(csv_file_path, save_folder="save_folder"):
    print("update_csv_with_coordinates Function started running")
    # Read the original CSV file
    data = pd.read_csv(csv_file_path)

    # Ensure the column containing URLs is named 'image_url'
    if 'image_url' not in data.columns:
        raise ValueError("The CSV file must contain a column named 'image_url'.")

    # Add new columns for latitude and longitude
    data['Latitude'] = None
    data['Longitude'] = None

    # Iterate over all files in the save_folder
    for image_filename in os.listdir(save_folder):
        print(f"Loop started with {image_filename}")
        if image_filename.endswith(".jpg"):
            file_id = extract_file_id(image_filename)
            image_path = os.path.join(save_folder, image_filename)
            print(image_path)

            # Find the corresponding row in the DataFrame using the file_id
            row_index = data[data['image_url'].str.contains(file_id, na=False)].index

            if len(row_index) > 0:
                lat, lng = extract_coordinates_from_image(image_path)
                print(lat, lng)
                data.at[row_index[0], 'Latitude'] = lat
                data.at[row_index[0], 'Longitude'] = lng
            else:
                print(f"No matching URL found for file ID: {file_id}")

    # Save the updated DataFrame to the original CSV file
    data.to_csv(csv_file_path, index=False)
    print(f"Updated {csv_file_path} with latitude and longitude values.")

# Utility function to extract file ID from Google Drive URL
def extract_file_id(image_filename):
    try:
        # Remove the '.jpg' extension to get the file_id
        file_id = image_filename.split('.jpg')[0]
        return file_id
    except IndexError:
        return None

# Specify the path to your CSV file and the folder containing downloaded images
csv_file_path = 'images.csv'  # Update this to your actual CSV file path
update_csv_with_coordinates(csv_file_path)
