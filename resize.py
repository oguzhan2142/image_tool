import io
import time
from typing import Tuple

import cv2
import numpy as np
from PIL import Image
import os


def generate_test_image(ratio: Tuple[int, int], file_size: int) -> Image:
    """
        Generate a test image with fixed width height ratio and an approximate size.

        :param ratio: (Tuple[int, int]) screen ratio for the image
        :param file_size: (int) Approximate size of the image, note that this may be off due to image compression.
    """
    height, width = ratio  # Numpy reverse values
    scale = np.int(np.sqrt(file_size // (width * height)))
    img = np.random.randint(0, 255, (width * scale, height * scale, 3), dtype=np.uint8)
    return img


def _change_image_memory(path, file_size: int = 2 ** 20):
    """
        Tries to match the image memory to a specific file size.

        :param path: (str) Path to the image
        :param file_size: (int) Size of the file in bytes
        :return: (np.ndarray) rescaled version of the image
    """
    image = cv2.imread(path)
    height, width = image.shape[:2]

    original_memory = os.stat(path).st_size
    original_bytes_per_pixel = original_memory / np.product(image.shape[:2])

    # perform resizing calculation
    new_bytes_per_pixel = original_bytes_per_pixel * (file_size / original_memory)
    new_bytes_ratio = np.sqrt(new_bytes_per_pixel / original_bytes_per_pixel)
    new_width, new_height = int(new_bytes_ratio * width), int(new_bytes_ratio * height)

    new_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR_EXACT)
    return new_image


def _get_size_of_image(image):
    # Encode into memory and get size
    buffer = io.BytesIO()
    image = Image.fromarray(image)
    image.save(buffer, format="JPEG")
    size = buffer.getbuffer().nbytes
    return size


def limit_image_memory(path, max_file_size: int, delta: float = 0.05, step_limit=10):
    """
        Reduces an image to the required max file size.

        :param path: (str) Path to the original (unchanged) image.
        :param max_file_size: (int) maximum size of the image
        :param delta: (float) maximum allowed variation from the max file size.
            This is a value between 0 and 1, relatively to the max file size.
        :return: an image path to the limited image.
    """
    start_time = time.perf_counter()
    max_file_size = max_file_size * (1 - delta)
    max_deviation_percentage = delta
    new_image = None

    current_memory = new_memory = os.stat(image_location).st_size
    ratio = 1
    steps = 0

    while abs(1 - max_file_size / new_memory) > max_deviation_percentage:
        new_image = _change_image_memory(path, file_size=max_file_size * ratio)
        new_memory = _get_size_of_image(new_image)
        ratio *= max_file_size / new_memory
        steps += 1

        # prevent endless looping
        if steps > step_limit:  break

    print(f"Stats:"
          f"\n\t- Original memory size: {current_memory / 2 ** 20:9.2f} MB"
          f"\n\t- New memory size     : {new_memory / 2 ** 20:9.2f} MB"
          f"\n\t- Number of steps {steps}"
          f"\n\t- Time taken: {time.perf_counter() - start_time:5.3f} seconds")

    if new_image is not None:
        cv2.imwrite(f"resize {path}", new_image)
        return f"resize {path}"
    return path


if __name__ == '__main__':
    image_location = "your nice image.jpg"

    # Uncomment to generate random test images
    # test_image = generate_test_image(ratio=(16, 9), file_size=1567289)
    # cv2.imwrite(image_location, test_image)

    path = limit_image_memory(image_location, max_file_size=2 ** 20, delta=0.01)
