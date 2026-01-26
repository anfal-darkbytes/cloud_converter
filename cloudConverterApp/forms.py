from django import forms

class DataForm(forms.Form):
    from_file = forms.CharField(max_length=100)
    to_file = forms.CharField(max_length=100)
    file_picked = forms.FileField()
