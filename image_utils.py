from django.core.files import File
import os 
from PIL import Image
from io import BytesIO

image_types = {
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".png": "PNG",
}


def image_resize(image):
    # Open the image using Pillow
    img = Image.open(image)
    # check if either the width or height is greater than the max
    if img.width > 300 or img.height > 300:
        output_size = (300, 300)
        # Create a new resized “thumbnail” version of the image with Pillow
        img.thumbnail(output_size)
        # Find the file name of the image
        img_filename, img_extention = os.path.splitext(image.file.name)
        # Use the file extension to determine the file type from the image_types dictionary
        img_format = image_types[img_extention]
        # Save the resized image into the buffer, noting the correct file type
        buffer = BytesIO()
        img.save(buffer, format=img_format)
        # Wrap the buffer in File object
        file_object = File(buffer)
        file_object.content_type = 'image/jpeg'
        # Save the new resized file as usual, which will save to S3 using django-storages
        image.save(img_filename, file_object)