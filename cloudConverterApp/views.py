from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect
from .forms import DataForm
from django.db import transaction
from .models import UploadMultiFileModel, ConvertModel
from .utils import convert_file, get_extension
import logging
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import ConvertedMultiFileModel

logger = logging.getLogger('cloudConverterApp/web_views.py')

def home(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')

    if ip_address:
        ip_address = ip_address.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    if request.method == 'POST':
        data_form = DataForm(request.POST, request.FILES)
        if data_form.is_valid():
            files = request.FILES.getlist('file_picked')
            to_file = data_form.cleaned_data['to_file'].upper()
            from_formats = []
            last_obj = None

            with transaction.atomic():
                for f in files:
                    uploaded_instance = UploadMultiFileModel.objects.create(file=f)

                    file_extension = get_extension(f).upper()
                    from_formats.append(file_extension)

                    last_obj = ConvertModel.objects.create(
                        ipaddr= ip_address,
                        uploaded=uploaded_instance,
                        from_format=file_extension,
                        to_format=to_file,
                        created_at=timezone.now()
                    )

            from_file_ext_slug = "-".join(sorted(set(from_formats)))

            return redirect('convert', from_format=from_file_ext_slug,
                            to_format=to_file, pk=last_obj.pk)

    return render(request, 'home/home.html', {'form': DataForm()})

def convert(request, from_format, to_format, pk):
    obj = get_object_or_404(ConvertModel, pk=pk)

    if request.method == 'POST':
        uploaded_file = obj.uploaded.file
        to_format = obj.to_format

        output_file = convert_file(uploaded_file, to_format)

        converted_instance = ConvertedMultiFileModel()

        file_name = f"converted_{obj.pk}.{to_format.lower()}"
        converted_file = InMemoryUploadedFile(
            output_file,
            None,
            file_name,
            f'image/{to_format.lower()}',
            output_file.tell(),
            None
        )

        converted_instance.file.save(file_name, converted_file)
        converted_instance.save()

        obj.converted = converted_instance
        obj.save()

        return render(request, 'converter/converter.html', {'obj': obj})

    return render(request, 'converter/converter.html', {'from_format': from_format, 'to_format': to_format, 'pk': pk})


def privacy_policy(request):
    return render(request, 'privacy_policy/privacy_policy.html')

def terms_condition(request):
    return render(request, 'terms_condition/terms_condition.html')