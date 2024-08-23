import subprocess

def create_pip_video(background_video, pip_video, output_video, x_offset, y_offset, scale_width, scale_height):
    """
    Create a picture-in-picture (PiP) video.

    :param background_video: Path to the background video file.
    :param pip_video: Path to the picture-in-picture video file.
    :param output_video: Path where the output video will be saved.
    :param x_offset: X position for the PiP video overlay.
    :param y_offset: Y position for the PiP video overlay.
    :param scale_width: Width to scale the PiP video.
    :param scale_height: Height to scale the PiP video.
    """
    command = [
        'ffmpeg',
        '-i', background_video,                   # Input background video
        '-i', pip_video,                          # Input PiP video
        '-filter_complex', (
            f'[1:v]scale={scale_width}:{scale_height}[pip];'  # Scale the PiP video
            f'[0:v][pip]overlay={x_offset}:{y_offset}'        # Overlay the PiP video on the background
        ),
        '-codec:a', 'copy',                       # Copy audio from the background video
        output_video                             # Output file
    ]

    try:
        subprocess.run(command, check=True)
        print(f'PiP video created successfully: {output_video}')
    except subprocess.CalledProcessError as e:
        print(f'Error occurred: {e}')

# Example usage
background_video = '/home/jasvir/Music/Movie work/Pic in pic/1.mp4'
pip_video = '/home/jasvir/Music/Movie work/Pic in pic/2.mp4'
output_video = '/home/jasvir/Music/Movie work/Pic in pic/output_video.mp4'
x_offset = 10          # X position for PiP video
y_offset = 10          # Y position for PiP video
scale_width = 320      # Width of PiP video
scale_height = 180     # Height of PiP video

create_pip_video(background_video, pip_video, output_video, x_offset, y_offset, scale_width, scale_height)
