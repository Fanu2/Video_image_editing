import subprocess

def resize_image(input_path, output_path, size):
    subprocess.run(['convert', input_path, '-resize', size, output_path])

# Example usage
resize_image('input.jpg', 'output_resized.jpg', '800x600')
