import os
from .image import convert_image

def dispatch_conversion(input_path, output_path, src, target):
    if src in ["png", "jpg", "jpeg", "gif"]:
        convert_image(input_path, output_path, target)
    else:
        raise ValueError("Unsupported conversion")
