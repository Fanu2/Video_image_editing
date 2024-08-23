from google_images_download import google_images_download


def download_images(keywords, limit=10, output_directory="downloads"):
    # Create an instance of google_images_download
    response = google_images_download.googleimagesdownload()

    # Set up the arguments for the download
    arguments = {
        "keywords": keywords,
        "limit": limit,
        "print_urls": True,
        "output_directory": output_directory,
        "format": "jpg"
    }

    # Download the images
    paths = response.download(arguments)
    return paths


if __name__ == "__main__":
    keywords = "beautiful scenery"
    limit = 20
    output_directory = "/home/jasvir/Music/Jacinta2"

    download_images(keywords, limit, output_directory)
