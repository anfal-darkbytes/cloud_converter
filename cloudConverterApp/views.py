from django.shortcuts import render
from .forms import OptionForm, PickFileForm, DataForm
from .models import ConvertModel
from .utils import detect_file_extension
import logging

logger = logging.getLogger('cloudConverterApp/views.py')
converter = ConvertModel()

def home(request):
    return render(request, 'home/home.html')

def data(request):
    if request.method == 'POST':
        data_form = DataForm(request.POST, request.FILES)
        if data_form.is_valid():
            to_file = data_form.cleaned_data['to_file']
            file_picked = data_form.cleaned_data['file_picked']

            from_file = detect_file_extension(file_picked)
            converter.from_format = from_file
            converter.to_format = to_file
            converter.file_picked = file_picked
            converter.save()

            context = {
                'from': from_file,
                'to': to_file,
                'file': file_picked
            }

            return context
    return None

def convert(request):
    return render(request, 'converter/converter.html')
