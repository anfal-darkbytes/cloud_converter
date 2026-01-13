from django import forms

class SelectForm(forms.Form):
    from_file = forms.FileField()
    to_file = forms.FileField()