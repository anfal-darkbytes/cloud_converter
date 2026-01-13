from django import forms

class UploadForm(forms.Form):
    file = forms.FileField()

class ConvertForm(forms.Form):
    target_format = forms.ChoiceField(choices=[])
