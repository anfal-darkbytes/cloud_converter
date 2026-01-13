from django.shortcuts import render
from . import utils
from . import forms

def home(request):
    if request.method == 'POST':
        form = forms.SelectForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data['from_file']
            to_file = form.cleaned_data['to_file']
            detected_formate = utils.detect_file_extension(file)
            if detected_formate:
                context = {
                    'from_format': detected_formate,
                    'file': file,
                    'to_file': to_file
                }

                return render(request, 'converter/converter.html', context)
            else:
                form.add_error(None, "Could not detect file format.")
        else:
            return render(request, 'home/home.html')

    return render(request, 'home/home.html')


def convert(request):
    return render(request, 'converter/converter.html')
