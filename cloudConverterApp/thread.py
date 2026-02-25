import threading
import time
from datetime import timedelta
from django.utils import timezone

class CleanUpFiles(threading.Thread):
    def run(self):
        from .models import ConvertModel
        while True:
            expiry_time = timezone.now() - timedelta(minutes=5)
            objs = ConvertModel.objects.filter(created_at__lt=expiry_time)

            for obj in objs:
                for upload in obj.uploaded_files.all():
                    if upload.file:
                        upload.file.delete(save=False)


                for converted in obj.converted_files.all():
                    if converted.file:
                        converted.file.delete(save=False)

                print(f'Cleaning up files and DB record for: {obj}')
                obj.delete()

            time.sleep(60)
