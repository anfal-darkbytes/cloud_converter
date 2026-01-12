from django.shortcuts import render


def home(request):
    return render(request, 'home/home.html')

def convert(request):
    return render(request, 'converter/converter.html')
