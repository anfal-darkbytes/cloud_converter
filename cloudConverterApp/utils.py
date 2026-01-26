import magic
import os
from PIL import Image
from pdf2image import convert_from_path

def detect_file_extension(file):
    mime = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)

    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "application/pdf": "pdf",
        "image/gif": "gif",
        "application/zip": "zip",
    }

    return mapping.get(mime, os.path.splitext(file.name)[1].replace('.', ''))


def convert_file(file, to_file):













# def convert_file(file, from_ext, to_ext, file_name):
#     if from_ext == to_ext:
#         return 'file extension can\'nt be same'
#
#     elif (from_ext == 'png' or 'jpg') and (to_ext=='jpg' or 'png'):
#         im = Image.open(os.path.abspath(file))
#         rgb_im = im.convert('RGB')
#         rgb_im.save(file_name+to_ext)
#         return rgb_im
#
#     elif (from_ext == 'png' or 'jpg') and (to_ext=='pdf'):
#         im = Image.open(os.path.abspath(file))
#         im.save(file_name + to_ext, 'PDF',resolution=100.0)
#         return im
#
#     elif (from_ext=='pdf') and (to_ext == 'png' or 'jpg'):
#         pages = convert_from_path(file, 500)
#         for count, page in enumerate(pages):
#             page.save(f'image{count}.{to_ext}', to_ext.upper())
#         return pages
#
#     else:
#         return 'error while converting file'

