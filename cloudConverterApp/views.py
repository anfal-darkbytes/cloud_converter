from django.shortcuts import render
from .forms import OptionForm, PickFileForm, DataForm
from .models import ConvertModel
from .utils import detect_file_extension
import logging
from django.http import JsonResponse
import datetime
logger = logging.getLogger('cloudConverterApp/views.py')
converter = ConvertModel()

def home(request):
    if request.method == 'POST':
        data_form = DataForm(request.POST, request.FILES)

        if data_form.is_valid():
            to_file = data_form.cleaned_data['to_file']
            file_picked = data_form.cleaned_data['file_picked']

            from_file = detect_file_extension(file_picked)

            converter.from_format = from_file
            converter.to_format = to_file
            converter.file_picked = file_picked
            converter.created_at = datetime.datetime.now()

            converter.save()

            info = {
                'from': from_file,
                'to': to_file,
                'file': file_picked
            }

            return JsonResponse(info)

    return render(request, 'home/home.html')


def convert(request):
    return render(request, 'converter/converter.html')
