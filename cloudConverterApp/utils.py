import magic
import os

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


# def convert_file(file,)