from PIL import Image
import img2pdf
import os

def convert_image(input_path, output_path, target):
    img = Image.open(input_path)

    if target == "pdf":
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(input_path))
    else:
        img.save(output_path, target.upper())
