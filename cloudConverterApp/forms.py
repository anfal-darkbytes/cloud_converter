from django import forms

class DataForm(forms.Form):
    from_file = forms.CharField()
    to_file = forms.CharField()
    file_picked = forms.FileField()
