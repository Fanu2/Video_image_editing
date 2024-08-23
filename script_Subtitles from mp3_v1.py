from mutagen.mp3 import MP3
from mutagen.id3 import ID3


def print_all_tags(file_path):
    try:
        # Load the MP3 file
        audio = MP3(file_path, ID3=ID3)

        # Print all tags
        tags = audio.tags

        if tags:
            for tag in tags.values():
                print(f"{tag.FrameID}: {tag.text}")
        else:
            print("No tags found.")

    except Exception as e:
        print(f"An error occurred: {e}")


# Path to the MP3 file
file_path = '/home/jasvir/Music/Movie work/River Flows in You.mp3'

print_all_tags(file_path)
