from django.shortcuts import render, redirect
from . import forms
from .forms import OptionForm, PickFileForm
from .models import ConvertModel
from .utils import detect_file_extension


def home(request):
    if request.method == 'POST':
        converter = ConvertModel.objects.get(pk=id)
        # Options
        if 'from_file' and 'to_file' in request.POST:
            option_form = OptionForm(request.POST)
            print(f'{request.POST}')
            if option_form.is_valid():
                from_file = option_form.cleaned_data['from_file']
                to_file = option_form.cleaned_data['to_file']

                converter.from_format = from_file
                converter.to_format = to_file
                converter.save(update_fields=['from_format', 'to_format'])

                return redirect('/')

        # Select File
        if 'file_picked' in request.FILES:
            select_form = PickFileForm(request.POST, request.FILES)
            if select_form.is_valid():
                selected_file = select_form.cleaned_data['file_picked']

                converter.uploaded = selected_file

                from_ext = detect_file_extension(selected_file)

                converter.save(update_fields=['uploaded', 'from_format'])

                to_ext = converter.objects.values_list('to_format')

                context = {
                    'from': from_ext,
                    'to': to_ext,
                    'file': selected_file
                }

                return render(request, 'converter/converter.html', context)


    return render(request, 'home/home.html')


def convert(request):
    return render(request, 'converter/converter.html')
