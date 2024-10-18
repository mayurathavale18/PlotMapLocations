import pandas as pd
import requests
import os

def download_image_from_drive(image_url):
    # Extract the file ID from the Google Drive URL
    try:
        file_id = image_url.split('id=')[1]
    except IndexError:
        return None
    download_url = f"https://drive.google.com/uc?id={file_id}&export=download"
    
    folder = "save_folder"
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    response = requests.get(download_url)
    if response.status_code == 200:
        image_path = os.path.join(folder, f"{file_id}.jpg")
        with open(image_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {image_path}")
        return image_path
    else:
        print(f"Failed to download image: {image_url}")
        return None

# Step 1: Read the CSV file containing the Google Drive URLs
csv_file_path = 'images.csv'  # Update this path to your CSV file
data = pd.read_csv(csv_file_path)

# Ensure the column containing URLs is named 'Image_URL'
if 'image_url' not in data.columns:
    raise ValueError("The CSV file must contain a column named 'Image_URL'.")

# Step 2: Download all images from the provided URLs
for index, row in data.iterrows():
    image_url = row['image_url']
    download_image_from_drive(image_url)

print("All images have been processed.")
