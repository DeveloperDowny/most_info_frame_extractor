import os

import cv2
from PIL import Image

from src.video2pdf.utils.directory_manager import DirectoryManager
from src.video2pdf.utils.file_frame import FileFrame as Frame


class PostProcessor:
    @staticmethod
    def add_text_to_frames_and_save(input_dir, list_of_files, output_dir):
        # TODO: remove return
        return
        frames = Frame.get_sorted_frames(list_of_files)

        n = len(frames)
        for i, frame in enumerate(frames):
            frame_path = os.path.join(input_dir, frame.frame_path)
            current_frame = cv2.imread(frame_path)

            text = f"Glimpsify {i + 1}/{n}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size, _ = cv2.getTextSize(text, font, 0.51, 1)
            text_x = 10
            text_y = current_frame.shape[0] - 10

            overlay = current_frame.copy()

            # Draw the filled rectangle on the overlay image
            cv2.rectangle(
                overlay,
                (text_x, text_y - text_size[1] - 10),
                (text_x + text_size[0], text_y),
                (85, 26, 58),
                cv2.FILLED,
            )
            cv2.putText(
                overlay,
                text,
                (text_x, text_y - 5),
                font,
                0.5,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

            # Blend the overlay with the original image using alpha blending
            opacity = 0.6
            cv2.addWeighted(
                overlay, opacity, current_frame, 1 - opacity, 0, current_frame
            )

            output_path = os.path.join(output_dir, frame.frame_path)
            cv2.imwrite(output_path, current_frame)

    @staticmethod
    def convert_images_to_pdf(input_dir, list_of_files, output_pdf_path):
        frames = [Frame(file) for file in list_of_files]
        frames.sort(key=lambda x: x.frame_id)

        images = []
        first_image = None

        for frame in frames:
            image_path = os.path.join(input_dir, frame.frame_path)
            img = Image.open(image_path)

            if img.mode == "RGBA":
                img = img.convert("RGB")

            if first_image is None:
                first_image = img
            else:
                images.append(img)

        if first_image:
            first_image.save(output_pdf_path, save_all=True, append_images=images)
            return True
        return False


if __name__ == "__main__":
    input_dir = "data_archive_1/lrpdqi_profits"
    output_dir = "data_archive_1/lrpdqi_profits_postprocessed"
    pdf_output_path = "data_archive_1/lrpdqi_profits.pdf"

    DirectoryManager.create_directory(output_dir)

    list_of_files = os.listdir(input_dir)

    # Process and save individual frames
    PostProcessor.add_text_to_frames_and_save(input_dir, list_of_files, output_dir)

    # Convert processed images to PDF
    processed_files = os.listdir(output_dir)
    if PostProcessor.convert_images_to_pdf(
            output_dir, processed_files, pdf_output_path
    ):
        print(f"PDF successfully created at {pdf_output_path}")
    else:
        print("Failed to create PDF - no images found")
