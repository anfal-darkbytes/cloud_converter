import io
from io import BytesIO
import os
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.utils import timezone
from datetime import timedelta
from rembg import remove
from .models import ConvertModel


def execute_conversion(file_bytes, to_ext, params):
    input_io = io.BytesIO(file_bytes)
    content_file = convert_file(input_io, to_ext, **params)
    return content_file.read()


def convert_file(file, to_ext, width=800, height=600, quality=90, strip=True, fit='fit', remove_bg=False):
    target_format = to_ext.upper().replace('JPG', 'JPEG')

    with Image.open(file) as im:
        if target_format == "JPEG" and im.mode in ("RGBA", "P"):
            im = im.convert("RGB")

        if fit == 'fit':
            im = ImageOps.fit(im, (width, height), Image.Resampling.LANCZOS)
        elif fit == 'max':
            im.thumbnail((width, height), Image.Resampling.LANCZOS)
        else:
            im = im.resize((width, height), Image.Resampling.LANCZOS)

        if remove_bg:
            im = remove(im)

        buffer = BytesIO()
        im.save(fp=buffer, format=target_format, quality=quality, optimize=strip)
        buff_val = buffer.getvalue()
    return ContentFile(buff_val)


def get_extension(file):
    filename = file.name if hasattr(file, 'name') else str(file)
    _, file_extension = os.path.splitext(filename)
    return file_extension.replace('.', '')


def get_filename(file):
    return os.path.splitext(file.name)[0].replace('.', '')


def del_old_conversions():
    life_span = timezone.now() - timedelta(hours=10)
    ConvertModel.objects.filter(created_at__lt=life_span).delete()
