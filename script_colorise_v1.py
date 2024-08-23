from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import torch
import os


def colorize_image(input_image_path):
    # Load the pre-trained model and feature extractor
    model_name = 'rsortino/ColorizeNet'
    feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)
    model = AutoModelForImageClassification.from_pretrained(model_name)

    # Open and preprocess the image
    image = Image.open(input_image_path).convert('RGB')
    inputs = feature_extractor(images=image, return_tensors="pt")

    # Perform colorization
    with torch.no_grad():
        outputs = model(**inputs)
        colorized_image = feature_extractor.post_process(outputs, target_sizes=[image.size[::-1]])[0]

    # Save the colorized image
    output_image_path = input_image_path  # Same path as input
    colorized_image.save(output_image_path)

    print(f"Colorized image saved to {output_image_path}")


if __name__ == "__main__":
    input_image_path = input("Enter the path to the black and white image: ")
    if os.path.exists(input_image_path):
        colorize_image(input_image_path)
    else:
        print("The provided path does not exist.")
