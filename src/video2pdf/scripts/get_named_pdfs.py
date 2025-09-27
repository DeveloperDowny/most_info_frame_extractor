import shutil

from src.video2pdf.utils.directory_manager import DirectoryManager
from src.video2pdf.utils.random_generator import RandomGenerator
from src.video2pdf.utils.file_util import FileUtil
from src.video2pdf.utils.text_util import TextUtil


def get_named_pdfs(index, input, new_directory):
    directory, video_name = TextUtil.get_directory_and_video_name(input)

    pdf_path = f"data/{directory}.pdf"

    output_path = f"{new_directory}/{index + 1} {video_name}.pdf"

    shutil.copy(pdf_path, output_path)


if __name__ == "__main__":
    new_directory = RandomGenerator.generate_random_word(3)
    new_directory = f"scripts/data/{new_directory}"
    DirectoryManager.create_directory(new_directory)

    inputs = FileUtil.get_inputs("scripts/data/results.txt")

    print(inputs)

    for index, input in enumerate(inputs):
        try:
            get_named_pdfs(index, input, new_directory)
        except Exception as e:
            print(input)
            print(e)
