import subprocess
from pathlib import Path


def main(dir):
    dir = Path(dir)
    already_processed_video_names = set()

    for folder in dir.iterdir():
        try:
            video_file_path: Path = list(folder.glob("*.mp4"))[0]
            if video_file_path.stem in already_processed_video_names:
                print(f"Skipping {folder}")
                continue

            already_processed_video_names.add(video_file_path.stem)

            input = folder.name
            if len(input) != 6:
                continue
            subprocess.run(
                [
                    "python", "/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/main.py",
                    "--input=local",
                    f"--dir={input}", "--ocr=tesseract", "--extraction=prominent_peaks"
                ]
            )
            # break
        except:
            print("Exception occurred for: ", folder)


if __name__ == "__main__":
    dir = "/src/video2pdf/data"
    main(dir)
