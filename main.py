

from image import Image

if __name__ == "__main__":

    max_allowed = 2000


    image = Image("sample.jpeg")
    image.reduce_image_memory(max_allowed)
    # image.delete_bg()
    # image.make_size(max_allowed)

    image.save("output.png")
