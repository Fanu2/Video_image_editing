import subprocess
import os


def convert_image_to_pgm(input_image, output_pgm):
    command = ['convert', input_image, output_pgm]
    subprocess.run(command, check=True)


def trace_image_to_svg(input_pgm, output_svg):
    command = ['potrace', input_pgm, '--svg', '-o', output_svg]
    subprocess.run(command, check=True)


def png_to_svg(input_image, output_svg):
    base_name = os.path.splitext(input_image)[0]
    intermediate_pgm = f"{base_name}.pgm"

    convert_image_to_pgm(input_image, intermediate_pgm)
    trace_image_to_svg(intermediate_pgm, output_svg)

    os.remove(intermediate_pgm)


# Example usage
input_image = '/home/jasvir/Documents/Jass/3.png'
output_svg = '/home/jasvir/Documents/Jass/3.svg'

png_to_svg(input_image, output_svg)
