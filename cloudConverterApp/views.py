from django.shortcuts import render
from .forms import DataForm
from .models import ConvertModel
from .utils import detect_file_extension, convert_file
import logging
from django.http import JsonResponse
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

            file_name = file_picked.replace(from_file, '')

            convert_file(file_picked, from_file, to_file, file_name)

            converter.converted =
            converter.save()
            print(f"from file ext in db: {converter.from_format}")
            print(f"to file ext in db: {converter.to_format}")
            print(f"file in db: {converter.file_picked}")
            print(f"created_at file ext in db: {converter.created_at}")

            res_data = {
                'from': from_file,
                'to': to_file
            }

            print(f'my data: {res_data}')

            return JsonResponse(
                data={
                    'status': 200,
                    'message': "Detected file",
                    'data': res_data,
                },
                safe=False,
                status=200
            )

    return render(request, 'home/home.html')


def convert(request):
    if request.GET:
        pass

    return render(request, 'converter/converter.html')
