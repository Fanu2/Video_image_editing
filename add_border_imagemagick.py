import subprocess

def add_border(input_path, output_path, border_size):
    subprocess.run(['convert', input_path, '-border', border_size, '-bordercolor', 'black', output_path])

# Example usage
add_border('input.jpg', 'output_border.jpg', '10x10')
