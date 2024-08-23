import os
import requests
from bs4 import BeautifulSoup

# Define the URL and the output directory
url = "https://huggingface.co/spaces/jbilcke-hf/ai-comic-factory"
output_dir = "/home/jasvir/Music/Jacinta1/"

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Send a request to the webpage
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to load page {url}")

# Parse the webpage content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all image tags
image_tags = soup.find_all('img')

# Download and save each image
for idx, img_tag in enumerate(image_tags):
    img_url = img_tag.get('src')
    if not img_url:
        continue

    # If the image URL is relative, make it absolute
    if img_url.startswith('/'):
        img_url = f"https://huggingface.co{img_url}"

    # Get the image content
    img_response = requests.get(img_url)
    if img_response.status_code == 200:
        img_data = img_response.content
        img_extension = img_url.split('.')[-1]
        img_path = os.path.join(output_dir, f"image_{idx}.{img_extension}")

        # Save the image
        with open(img_path, 'wb') as img_file:
            img_file.write(img_data)

        print(f"Saved image to {img_path}")

print("Download complete.")
