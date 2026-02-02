from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect
from .forms import DataForm
from .models import ConvertModel
from .utils import detect_file_extension, convert_file
import logging
from django.utils import timezone
from django.shortcuts import get_object_or_404

logger = logging.getLogger('cloudConverterApp/views.py')

def home(request):
    if request.method == 'POST':
        data_form = DataForm(request.POST, request.FILES)
        if data_form.is_valid():
            file_picked = data_form.cleaned_data['file_picked']
            from_file = detect_file_extension(file_picked)

            obj = ConvertModel.objects.create(
                uploaded = file_picked,
                from_format = from_file,
                to_format = data_form.cleaned_data['to_file'],
                created_at=timezone.now()
            )

            return redirect('convert', from_format=obj.from_format, to_format=obj.to_format, pk=obj.pk)

    return render(request, 'home/home.html')


def convert(request,from_format, to_format, pk):
    obj = get_object_or_404(ConvertModel, pk=pk)
    if request.method == 'POST':

        uploaded_file=obj.uploaded
        to_format=obj.to_format

        output_file = convert_file(uploaded_file, to_format)

        obj.converted = InMemoryUploadedFile(output_file, None, 'fool.' + to_format,
                                                   'image/' + to_format, output_file.tell, None)
        obj.save()

        return render(request, 'converter/converter.html', {'obj':obj})
    return render(request, 'converter/converter.html', {'obj':obj})

def privacy_policy(request):
    return render(request, 'privacy_policy/privacy_policy.html')

def terms_condition(request):
    return render(request, 'terms_condition/terms_condition.html')