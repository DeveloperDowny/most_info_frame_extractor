import io
from pathlib import Path
from typing import List

import fitz
import imagehash
import pandas as pd
from PIL import Image


def clean_df(pdf_files_df: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicate rows"""
    return pdf_files_df.drop_duplicates(subset=["internal_id"], keep="last")


def build_pdf_files_df(files: List[Path]):
    """Build PDF files dataframe having columns `internal_id` and `pdf_path`"""
    pdfs_files_df = pd.DataFrame(columns=["internal_id", "pdf_path"])
    for file in files:
        new_row = {"internal_id": file.stem.split("_")[0], "pdf_path": str(file)}
        pdfs_files_df = pd.concat([pdfs_files_df, pd.DataFrame([new_row])])
    return pdfs_files_df


def get_pdf_files(folder_path: str | Path):
    """Get PDF files in the folder"""
    folder_path = Path(folder_path)
    return folder_path.glob("*.pdf")


def extract_image_hashes_from_pdf(pdf_path: str) -> list:
    """
    Extracts images from each page of a PDF and computes their perceptual hashes (pHash).
    pHash is used because it identifies images that are visually similar,
    which is suitable for lecture slides where content might have minor variations
    but should be considered the same if visually identical.
    Assumes one image per page.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        list: A list of imagehash.ImageHash objects.
    """
    hashes = []
    try:
        pdf_document = fitz.open(pdf_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            # Render page to a pixmap (an image representation)
            pix = page.get_pixmap()
            # Convert pixmap to PNG image bytes
            img_bytes = pix.tobytes("png")
            # Open image bytes with Pillow
            pil_image = Image.open(io.BytesIO(img_bytes))

            # Convert to RGB if it's RGBA, P (palette), or LA (Luminance Alpha)
            # to ensure consistency for hashing, as pHash works best on RGB.
            if pil_image.mode in ('RGBA', 'P', 'LA'):
                pil_image = pil_image.convert('RGB')

            # Compute perceptual hash (pHash)
            img_hash = imagehash.phash(pil_image)
            hashes.append(img_hash)
        pdf_document.close()
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}")
        # Return empty list if a PDF is corrupt, unreadable, or contains no valid images
    return hashes


def evaluate(evaluation_data_df: pd.DataFrame) -> pd.DataFrame:
    # ----- Init evaluation report df
    # Define the columns for the evaluation report DataFrame
    evaluation_report_cols = ['internal_id',
                              'num_of_duplicates',
                              'num_of_missing_key_frames',
                              'num_of_non_key_frames',
                              'generated_pdf_key_frame_count',
                              'reference_pdf_key_frame_count',
                              'accuracy',
                              'precision',
                              'similarity_score']
    # Initialize an empty DataFrame to store evaluation results
    evaluation_report_df = pd.DataFrame(columns=evaluation_report_cols)

    # ---- Build evaluation report
    # List to store data for new rows, to be concatenated later for efficiency
    new_rows_list = []

    for index, row_data in evaluation_data_df.iterrows():
        internal_id = row_data['internal_id']
        generated_pdf_path = row_data['pdf_path_generated']
        reference_pdf_path = row_data['pdf_path_reference']

        print(f"Processing evaluation for: {internal_id}")

        # Extract perceptual hashes from generated and reference PDFs
        # These hashes represent the visual content of each slide.
        gen_hashes_list = extract_image_hashes_from_pdf(generated_pdf_path)
        ref_hashes_list = extract_image_hashes_from_pdf(reference_pdf_path)

        # Total number of frames (images/pages) in the generated PDF
        generated_pdf_key_frame_count = len(gen_hashes_list)

        # Create sets of hashes for efficient comparison.
        # For reference, assume it's already curated (no duplicates), but set ensures uniqueness.
        ref_hashes_set = set(ref_hashes_list)
        reference_pdf_key_frame_count = len(ref_hashes_set)  # Number of unique reference frames

        # Unique hashes from the generated PDF
        unique_gen_hashes_set = set(gen_hashes_list)
        num_unique_generated_frames = len(unique_gen_hashes_set)

        # METRIC 1: Number of duplicates in the generated PDF
        # Duplicates are extra occurrences of the same visual slide.
        num_of_duplicates = generated_pdf_key_frame_count - num_unique_generated_frames

        # Identify True Positives: Unique generated frames that are also in reference frames.
        # These are the correctly identified keyframes.
        true_positives_hashes_set = unique_gen_hashes_set.intersection(ref_hashes_set)
        num_true_positives = len(true_positives_hashes_set)

        # METRIC 2: Number of missing keyframes
        # These are frames present in the reference set but not found in the unique generated set (False Negatives).
        missed_hashes_set = ref_hashes_set.difference(unique_gen_hashes_set)
        num_of_missing_key_frames = len(missed_hashes_set)

        # METRIC 3: Number of non-key frames (False Positives)
        # These are frames present in the unique generated set but not found in the reference set.
        # These are incorrectly identified as keyframes.
        non_key_frame_hashes_set = unique_gen_hashes_set.difference(ref_hashes_set)
        num_of_non_key_frames = len(non_key_frame_hashes_set)

        # METRIC 4: Accuracy
        # Defined as: (number of correctly identified unique keyframes) / (total number of actual keyframes)
        # The numerator (generated_pdf_key_frame_count - num_of_duplicates - num_of_non_key_frames)
        # simplifies to num_true_positives.
        if reference_pdf_key_frame_count > 0:
            accuracy = num_true_positives / reference_pdf_key_frame_count
        else:
            # If there are no reference keyframes:
            # Accuracy is 1.0 if no frames were generated (correctly identified nothing).
            # Accuracy is 0.0 if any frames were generated (all would be non-keyframes).
            accuracy = 1.0 if num_unique_generated_frames == 0 else 0.0

        # METRIC 5: Similarity Score (Jaccard Index)
        # J(A,B) = |A ∩ B| / |A ∪ B|
        # A = unique_gen_hashes_set, B = ref_hashes_set
        # Intersection = num_true_positives
        # Union = total unique items in either set
        union_hashes_set = unique_gen_hashes_set.union(ref_hashes_set)
        num_union_hashes = len(union_hashes_set)

        if num_union_hashes > 0:
            similarity_score = num_true_positives / num_union_hashes
        else:
            # If both sets are empty (no generated frames and no reference frames),
            # their Jaccard index is 1.0 (perfectly similar in their emptiness).
            similarity_score = 1.0

        # Store the calculated results for the current item
        current_eval_results = {
            'internal_id': internal_id,
            'num_of_duplicates': num_of_duplicates,
            'num_of_missing_key_frames': num_of_missing_key_frames,
            'num_of_non_key_frames': num_of_non_key_frames,
            'generated_pdf_key_frame_count': generated_pdf_key_frame_count,
            'reference_pdf_key_frame_count': reference_pdf_key_frame_count,
            'accuracy': accuracy,
            'precision': num_true_positives / generated_pdf_key_frame_count,
            'similarity_score': similarity_score
        }
        new_rows_list.append(current_eval_results)

    # Concatenate all new rows to the main DataFrame at once for better performance
    if new_rows_list:
        evaluation_report_df = pd.concat([evaluation_report_df, pd.DataFrame(new_rows_list)], ignore_index=True)

    return evaluation_report_df
