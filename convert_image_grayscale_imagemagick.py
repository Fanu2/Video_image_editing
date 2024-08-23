import subprocess

def convert_image_grayscale(input_path, output_path):
    subprocess.run(['convert', input_path, '-colorspace', 'Gray', output_path])

# Example usage
convert_image_grayscale('input.jpg', 'output_grayscale.jpg')
