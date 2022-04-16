

import os
from image import Image

if __name__ == "__main__":

    max_allowed = 2000
    cwd = os.getcwd()
    input_path = f'{cwd}/samples'
    output_path = f'{cwd}/outputs'

    isOutputExist = os.path.exists(output_path)

    if not isOutputExist:
        os.mkdir(output_path)

    for file in os.listdir(input_path):
        image = Image(os.path.join(input_path, file))
        image.delete_bg()
        output_file_path = os.path.join(output_path, file)
        print(output_file_path)
        image.save(output_file_path)
