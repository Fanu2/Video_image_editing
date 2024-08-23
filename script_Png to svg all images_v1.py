import os
import subprocess
import shlex

def create_svg_folder(svg_folder_path):
    # Create the SVG folder if it doesn't exist
    if not os.path.exists(svg_folder_path):
        os.makedirs(svg_folder_path)
        print(f"Created directory: {svg_folder_path}")

def convert_png_to_svg(png_folder, svg_folder):
    # Get a list of all PNG files in the input folder
    png_files = [f for f in os.listdir(png_folder) if f.endswith('.png')]

    # Convert each PNG file to SVG
    for png_file in png_files:
        input_image_path = os.path.join(png_folder, png_file)
        output_svg_path = os.path.join(svg_folder, os.path.splitext(png_file)[0] + '.svg')

        # Inkscape command to convert PNG to SVG
        command = f'inkscape {shlex.quote(input_image_path)} --export-filename={shlex.quote(output_svg_path)}'
        try:
            subprocess.run(command, shell=True, check=True)
            print(f"Converted {png_file} to SVG")
        except subprocess.CalledProcessError as e:
            print(f"Failed to convert {png_file} to SVG. Error: {e}")

# Define input and output folders
input_folder = '/home/jasvir/Music/Jodha2/'
output_folder = '/home/jasvir/Music/Jodha2/svg/'

# Create the SVG folder
create_svg_folder(output_folder)

# Convert PNG files to SVG
convert_png_to_svg(input_folder, output_folder)

print("Conversion completed.")
























