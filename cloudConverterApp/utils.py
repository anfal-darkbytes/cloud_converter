import io
from io import BytesIO

import magic
import os
from PIL import Image, ImageOps
from django.core.files.base import ContentFile


def detect_file_extension(file):
    mime = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)

    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "application/pdf": "pdf",
        "image/gif": "gif",
    }

    return mapping.get(mime, os.path.splitext(file.name)[1].replace('.', ''))

def convert_file(file, to_ext):
    with Image.open(file) as im:
        img_border = (0, 0, 0, 10)
        im_with_border = ImageOps.expand(im, border=img_border, fill='white')

        buffer = BytesIO()
        im_with_border.save(fp=buffer, format=to_ext.upper())
        buff_val = buffer.getvalue()
    return ContentFile(buff_val)

def get_filename(file):
    return os.path.splitext(file.name)[0].replace('.', '')
