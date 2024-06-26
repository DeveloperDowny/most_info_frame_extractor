import os
import random
import string
from yt_down import *
from u1 import *
import shutil

def generate_random_word(length):
    """Generates a random word of given length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def create_directory(directory_name):
    """Creates a directory with the given name."""
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")

def random_10_frames(dir):
    # Get the list of all files in directory tree at given path
    list_of_files = list()
    for (dirpath, dirnames, filenames) in os.walk(dir):
        list_of_files += [os.path.join(dirpath, file) for file in filenames]

    # Get 10 random files
    random_files = random.sample(list_of_files, 10)
    # return random_files
    new_dir = dir + "_10_" + generate_random_word(3)
    print(f"New directory: {new_dir}")
    create_directory(new_dir)
    # copy to new directory
    for file in random_files:
        shutil.copy(file, new_dir)

def main():
    # Generate a random 6-digit word
    random_word = generate_random_word(6)
    random_word = "data/" + random_word
    print(f"Random word: {random_word}")

    # Create a directory using the random word as the name
    create_directory(random_word)

    output_directory = os.path.join(os.getcwd(), random_word)  # Change this to your desired output directory
    video_url = input("Enter the URL of the YouTube video: ")  # Replace with your desired video URL
    download_youtube_video(video_url, output_directory)

    # get frames
    frame_dir_1 = random_word + "_frames"
    frame_dir = frame_dir_1  
    create_directory(frame_dir_1)
    # video_path = "data/v1_t5.mp4"
    # rename the file in the random_word directory to v1.mp4
    os.rename(output_directory + "/" + os.listdir(output_directory)[0], output_directory + "/v1.mp4")
    video_path = output_directory + "/v1.mp4"

    # Path to the Tesseract OCR executable
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Windows
    # tesseract_path = r"/usr/bin/tesseract"  # Linux/macOS

    # Path to save the improved frame
    # output_path = "frames3/frame.jpg" 
    output_path = frame_dir

    # Extract text with a difference threshold of 0.05 (5%)
    extract_text_from_video(video_path, tesseract_path, output_path, diff_threshold=0.05, interval=1.0)
    random_10_frames(frame_dir)




if __name__ == "__main__":
    main()
    # random_10_frames("data/vdcakt_frames")