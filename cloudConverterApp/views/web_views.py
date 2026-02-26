from django.shortcuts import render, redirect, get_object_or_404
from cloudConverterApp.forms import DataForm
from django.db import transaction
from cloudConverterApp.models import UploadMultiFileModel, ConvertModel, ConvertedMultiFileModel, ContactUsModel
from cloudConverterApp.utils import get_extension, execute_conversion
import logging
from concurrent.futures import ProcessPoolExecutor
from django.core.files.base import ContentFile


logger = logging.getLogger(__name__)

def home(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')).split(',')[0]

    if request.method == 'POST':
        data_form = DataForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_picked')

        if data_form.is_valid() and files:
            to_file = data_form.cleaned_data['to_file'].upper()
            convert_session = ConvertModel.objects.create(
                ipaddr=ip_address,
                to_format=to_file
            )

            from_formats = set()
            with transaction.atomic():
                for f in files:
                    UploadMultiFileModel.objects.create(
                        file=f,
                        convert=convert_session
                    )
                    from_formats.add(get_extension(f).upper())

            convert_session.from_format = "-".join(sorted(from_formats))
            convert_session.save()

            return redirect('convert',
                            from_format=convert_session.from_format,
                            to_format=to_file,
                            pk=convert_session.pk)

    return render(request, 'home/home.html', {'form': DataForm()})


def convert(request, from_format, to_format, pk):
    obj = get_object_or_404(ConvertModel, pk=pk)

    if request.method == 'POST':
        params = {
            'width': int(request.POST.get('width') or 800),
            'height': int(request.POST.get('height') or 600),
            'fit': request.POST.get('fit', 'fit'),
            'strip': request.POST.get('strip') == 'yes',
            'remove_bg': request.POST.get('remove_bg') == 'yes',
            'quality': int(request.POST.get('quality') or 90),
        }

        uploaded_items = obj.uploaded_files.all()

        with ProcessPoolExecutor() as executor:
            futures = {
                executor.submit(execute_conversion, item.file.read(), to_format, params): item
                for item in uploaded_items
            }

            for future in futures:
                try:
                    result_bytes = future.result()
                    original_item = futures[future]

                    file_name = f"conv_{original_item.id}.{to_format.lower()}"
                    converted_instance = ConvertedMultiFileModel(convert=obj)
                    converted_instance.file.save(file_name, ContentFile(result_bytes))
                except Exception as e:
                    logger.error(f"Conversion Error: {e}")

        return render(request, 'converter/converter.html', {'obj': obj, 'done': True})

    return render(request, 'converter/converter.html', {
        'from_format': from_format,
        'to_format': to_format,
        'pk': pk,
        'obj': obj
    })

def privacy_policy(request):
    return render(request, 'privacy_policy/privacy_policy.html')

def terms_condition(request):
    return render(request, 'terms_condition/terms_condition.html')

def apis(request):
    return render(request, 'apis/apis.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', ''),
        subject = request.POST.get('subject', '')
        comment = request.POST.get('comment')

        error = ''
        done = False
        try:
            ContactUsModel.objects.create(
                name=name,
                email=email,
                subject=subject,
                content=comment
            )
            done = True
        except Exception as e:
            print(f'error: {str(e)}')
            error = str(e)

        return render(request, 'contact_us/contact_us.html', {'done': done, 'error': error})

    return render(request, 'contact_us/contact_us.html')