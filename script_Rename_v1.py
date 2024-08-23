import os


def rename_files(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    # Sort files to maintain order
    files.sort()

    # Initialize a counter
    counter = 1

    # Iterate over the files and rename them
    for filename in files:
        # Form the new filename with counter and original extension
        new_filename = f"{counter}{os.path.splitext(filename)[1]}"
        # Form full file paths
        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, new_filename)

        # Rename the file
        os.rename(src, dst)
        print(f"Renamed: {src} to {dst}")

        # Increment the counter
        counter += 1


# Define the folder path
folder_path = "/home/jasvir/Music/Movie work/"

# Call the function
rename_files(folder_path)
