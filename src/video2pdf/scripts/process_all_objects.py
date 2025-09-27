import re
import subprocess
from pathlib import Path

from src.video2pdf.utils.constants import BASE_DIR


def main(dir):
    dir = Path(dir)
    folders = list(dir.iterdir())

    for folder in folders:
        try:
            input = folder.name
            pattern = r"\w{6}_\w{3}_python_object"
            if not re.fullmatch(pattern, input):
                continue
            subprocess.run(
                [
                    "python", "/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/main.py",
                    "--input=pickle",
                    f"--dir={input}", "--ocr=tesseract", "--extraction=prominent_peaks"
                ]
            )
        except:
            print("Exception occurred for: ", folder)


if __name__ == "__main__":
    dir = BASE_DIR
    main(dir)
