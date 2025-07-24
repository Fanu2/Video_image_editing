import subprocess

def trace_image_to_svg(input_image, output_svg):
    command = [
        'inkscape',
        input_image,
        '--export-type=svg',
        '--export-filename', output_svg,
        '--verb', 'EditSelectAll;SelectionTrace;FileSave;FileQuit'
    ]
    subprocess.run(command, check=True)

# Example usage
# [REMOVED PATH] input_image = '/home/jasvir/Documents/Jass/3.png'
# [REMOVED PATH] output_svg = '/home/jasvir/Documents/Jass/3a.svg'

trace_image_to_svg(input_image, output_svg)
