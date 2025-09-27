from typing import Union, Tuple

import cv2
import imagehash
import numpy as np
from PIL import Image


class ImageUtils:

    @staticmethod
    def are_images_almost_equal(image1: np.ndarray, image2: np.ndarray) -> bool:
        # Convert frames to grayscale
        image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # Compute the absolute difference between the two frames
        diff = cv2.absdiff(image1_gray, image2_gray)

        # Threshold the difference to get a binary image
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Calculate the percentage of different pixels
        non_zero_count = cv2.countNonZero(thresh)
        total_pixels = image1_gray.size
        diff_percentage = (non_zero_count / total_pixels) * 100

        # If the difference is less than a certain threshold, consider the frames almost the same
        return diff_percentage < 0.5

    @staticmethod
    def are_images_similar_phash(
            image1: Union[np.ndarray, str],
            image2: Union[np.ndarray, str],
            threshold: int = 8
    ) -> Tuple[bool, int]:
        """
        Compare two images using perceptual hash (phash) algorithm.

        This method is more robust to scaling, rotation, and minor edits than
        pixel-based comparison. The hash represents the visual signature of an image.
        Lower hash difference means higher similarity.

        Args:
            image1: First image as numpy array (BGR format) or path to image file
            image2: Second image as numpy array (BGR format) or path to image file
            threshold: Maximum hash difference to consider images similar (0-64)
                      Lower values mean stricter comparison

        Returns:
            Tuple[bool, int]: (True if images are similar, hash difference)
        """
        # Convert numpy arrays to PIL images if needed
        pil_image1 = ImageUtils._convert_to_pil(image1)
        pil_image2 = ImageUtils._convert_to_pil(image2)

        # Calculate perceptual hashes
        hash1 = imagehash.phash(pil_image1)
        hash2 = imagehash.phash(pil_image2)

        # Calculate hash difference (0 = identical, higher = more different)
        hash_diff = hash1 - hash2

        # Return similarity result and the hash difference
        return hash_diff <= threshold

    @staticmethod
    def _convert_to_pil(image: Union[np.ndarray, str]) -> Image.Image:
        """
        Convert image from numpy array or file path to PIL Image.

        Args:
            image: Image as numpy array (BGR format) or path to image file

        Returns:
            PIL.Image: Converted PIL image
        """
        if isinstance(image, str):
            # Load from file path
            return Image.open(image)
        elif isinstance(image, np.ndarray):
            # Convert from OpenCV BGR to RGB for PIL
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return Image.fromarray(rgb_image)
        elif isinstance(image, Image.Image):
            # Already a PIL image
            return image
        else:
            raise TypeError(f"Unsupported image type: {type(image)}")
