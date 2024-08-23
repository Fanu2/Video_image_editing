import subprocess
import json


def get_video_duration(video_path):
    """
    Get the duration of a video in seconds using ffprobe.

    :param video_path: Path to the video file.
    :return: Duration of the video in seconds.
    """
    command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=duration',
        '-of', 'json',
        video_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    print(f"ffprobe output: {result.stdout}")  # Debugging line

    try:
        duration_info = json.loads(result.stdout)
        return float(duration_info['streams'][0]['duration'])
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Error decoding JSON or parsing duration: {e}")
        print(f"ffprobe output: {result.stdout}")
        raise


def create_pip_video(background_video, pip_video, output_video, x_offset, y_offset, scale_width, scale_height):
    """
    Create a picture-in-picture (PiP) video and limit its length to the shorter input video.

    :param background_video: Path to the background video file.
    :param pip_video: Path to the picture-in-picture video file.
    :param output_video: Path where the output video will be saved.
    :param x_offset: X position for the PiP video overlay.
    :param y_offset: Y position for the PiP video overlay.
    :param scale_width: Width to scale the PiP video.
    :param scale_height: Height to scale the PiP video.
    """
    # Get the duration of both videos
    background_duration = get_video_duration(background_video)
    pip_duration = get_video_duration(pip_video)

    # Determine the shorter duration
    shortest_duration = min(background_duration, pip_duration)

    # Create the PiP video
    command = [
        'ffmpeg',
        '-i', background_video,
        '-i', pip_video,
        '-filter_complex', (
            f'[1:v]scale={scale_width}:{scale_height}[pip];'
            f'[0:v][pip]overlay={x_offset}:{y_offset}'
        ),
        '-codec:a', 'copy',
        '-t', str(shortest_duration),  # Set duration to the shortest video
        output_video
    ]

    try:
        subprocess.run(command, check=True)
        print(f'PiP video created successfully: {output_video}')
    except subprocess.CalledProcessError as e:
        print(f'Error occurred: {e}')


# Example usage
background_video = '/home/jasvir/Music/Movie work/Pic in pic/5.mp4'
pip_video = '/home/jasvir/Music/Movie work/Pic in pic/2.mp4'
output_video = '/home/jasvir/Music/Movie work/Pic in pic/output_video5.mp4'
x_offset = 10  # X position for PiP video
y_offset = 10  # Y position for PiP video
scale_width = 320  # Width of PiP video
scale_height = 180  # Height of PiP video

create_pip_video(background_video, pip_video, output_video, x_offset, y_offset, scale_width, scale_height)
