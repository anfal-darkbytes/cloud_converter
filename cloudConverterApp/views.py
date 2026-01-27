from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect
from .forms import DataForm
from .models import ConvertModel
from .utils import detect_file_extension, convert_file
import logging
import datetime

logger = logging.getLogger('cloudConverterApp/views.py')
converter = ConvertModel()

def home(request):
    if request.method == 'POST':
        print(f'from image: {request.POST['from_file']}')
        print(f'to image: {request.POST['to_file']}')
        print(f'file image: {request.FILES['file_picked']}')
        data_form = DataForm(request.POST, request.FILES)

        print(f'data form is valid: " {data_form.is_valid()}')
        if data_form.is_valid():
            to_file = data_form.cleaned_data['to_file']
            file_picked = data_form.cleaned_data['file_picked']

            from_file = detect_file_extension(file_picked)
            print(f'from file detected extension: {from_file}')

            converter.from_format = from_file
            converter.to_format = to_file
            converter.file_picked = file_picked
            converter.created_at = datetime.datetime.now()


            output_image = convert_file(file_picked, to_file)
            converter.converted = InMemoryUploadedFile(output_image, None, 'fool.'+ to_file,
                                                       'image/'+to_file, output_image.tell, None)

            converter.save()

            res_data = {
                'from': from_file,
                'to': to_file
            }

            print(f'my data: {res_data}')

            return redirect('convert', from_formate=from_file, to_formate=to_file)

    return render(request, 'home/home.html')


def convert(request, from_formate, to_formate):
    return render(request, 'converter/converter.html', {
        'from': from_formate,
        'to': to_formate,
    })
