import os
from django.conf import settings
from .utils import detect_file_extension
from .converters.dispatcher import dispatch_conversion

SUPPORTED_FORMATS = {
    "png": ["jpg", "pdf", "gif"],
    "jpg": ["png", "pdf"],
    "pdf": ["png", "jpg"],
    "gif": ["png"]
}

def handle_upload(file):
    ext = detect_file_extension(file)
    return ext, SUPPORTED_FORMATS.get(ext, [])

def convert_file(file, target):
    input_path = os.path.join(settings.MEDIA_ROOT, file.name)
    output_name = f"converted.{target}"
    output_path = os.path.join(settings.MEDIA_ROOT, output_name)

    with open(input_path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)

    src_ext = input_path.split('.')[-1]
    dispatch_conversion(input_path, output_path, src_ext, target)

    return output_name
