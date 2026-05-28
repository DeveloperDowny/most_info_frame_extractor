from pathlib import Path

from ytvideo2pdf.utils.helper import Helper

BASE_DIR = Path("/content")
DATA_DIR = BASE_DIR / "output"
# PYTHON_OBJECT = DATA_DIR / "ydeawv_python_object"
PYTHON_OBJECT = DATA_DIR / "kjvbci_python_object"  # old with 720p
METADATA_JSON = PYTHON_OBJECT / "metadata.json"


def main() -> None:
    processed_frames = Helper.load_python_object(
        PYTHON_OBJECT / "processed_frames.pkl"
    )
    metadata = Helper.load_json(str(METADATA_JSON))
    extracted_frame_numbers = metadata["extracted_frame_numbers"]

    all_frame_numbers, all_frame_char_counts = Helper.get_frame_char_counts(
        processed_frames
    )
    extracted_char_counts = Helper.get_extracted_char_counts(
        processed_frames, extracted_frame_numbers
    )

    fig = Helper.build_char_count_figure(
        all_frame_numbers,
        all_frame_char_counts,
        extracted_frame_numbers,
        extracted_char_counts,
    )
    fig.show()


if __name__ == "__main__":
    main()
