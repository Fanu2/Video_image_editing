import subprocess

def trace_image_to_svg(input_image, output_svg):
    command = f'inkscape --file="{input_image}" --export-type="svg" --export-filename="{output_svg}"'
    subprocess.run(command, shell=True)

# Example usage
input_image = '/home/jasvir/Documents/Jass/3.png'
output_svg = '/home/jasvir/Music/Jacinta2/image2.svg'

trace_image_to_svg(input_image, output_svg)
