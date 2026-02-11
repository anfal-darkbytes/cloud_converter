from io import BytesIO
import os
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from datetime import timedelta
from django.utils import timezone
from .models import ConvertModel
from celery import shared_task
from rembg import remove
import glob
from multiprocessing import Pool

def convert_file(file, to_ext, width=800, height=600, quality=90, strip=True, fit='fit', remove_bg=False):
    with Image.open(file) as im:
        im.resize((width, height), Image.Resampling.LANCZOS)
        if fit == 'fit':
            ImageOps.fit(im, (width, height), Image.Resampling.LANCZOS)
        elif fit == 'max':
            im.thumbnail((width, height), Image.Resampling.LANCZOS)
        else:
            im.resize((width,height), Image.Resampling.LANCZOS)

        if remove_bg:
            im = remove(im)

        buffer = BytesIO()
        im.save(fp=buffer, format=to_ext.upper(), quality=quality, optimize=strip)
        buff_val = buffer.getvalue()
    return ContentFile(buff_val)


def get_filename(file):
    return os.path.splitext(file.name)[0].replace('.', '')

def get_extension(file):
    filename = file.name if hasattr(file, 'name') else str(file)
    _, file_extension = os.path.splitext(filename)
    return file_extension.replace('.', '')

@shared_task
def del_old_conversions():
    life_span = timezone.now() - timedelta(hours=10)
    records = ConvertModel.objects.filter(create_at__lt=life_span)
    for record in records:
        record.delete()

