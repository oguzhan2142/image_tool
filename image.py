from cgi import print_arguments
import numpy as np

import os
import cv2


class Image:
    def __init__(self,  path: str):
        self.img = cv2.imread(path)
        self.path = path

    def save(self, path):
        cv2.imwrite(path, self.img)

    # calculate image size kb
    def get_size_kb(self):
        return self.img.nbytes / 1024

    # def getSize(self):
    #     row, column, depth = self.img.shape
    #     return row * column * depth // 1024

    def delete_bg(self):
        # load image
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gray = 255*(gray < 128).astype(np.uint8)  # To invert the text to white
        coords = cv2.findNonZero(gray)  # Find all non-zero points (text)
        # Find minimum spanning bounding box
        x, y, w, h = cv2.boundingRect(coords)
        # Crop the image - note we do this on the original image
        self.img = self.img[y:y+h, x:x+w]

    def scale_size(self, scale: float):
        self.img = cv2.resize(self.img, (0, 0), fx=scale, fy=scale)

    def make_size(self, size: float):
        kb = self.get_size_kb()
        x = size / kb

        self.scale_size(x)

    def reduce_image_memory(self, max_file_size: int = 2 ** 20):
        """
            Reduce the image memory by downscaling the image.

            :param path: (str) Path to the image
            :param max_file_size: (int) Maximum size of the file in bytes
            :return: (np.ndarray) downscaled version of the image
        """

        height, width = self.img.shape[:2]

        original_memory = os.stat(self.path).st_size
        print(original_memory)
        original_bytes_per_pixel = original_memory / \
            np.product(self.img.shape[:2])

        # perform resizing calculation
        new_bytes_per_pixel = original_bytes_per_pixel * \
            (max_file_size / original_memory)
        new_bytes_ratio = np.sqrt(
            new_bytes_per_pixel / original_bytes_per_pixel)
        new_width, new_height = int(
            new_bytes_ratio * width), int(new_bytes_ratio * height)

        self.img = cv2.resize(self.img, (new_width, new_height),
                              interpolation=cv2.INTER_LINEAR_EXACT)
