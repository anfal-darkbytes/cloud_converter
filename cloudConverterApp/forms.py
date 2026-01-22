from django import forms

class OptionForm(forms.Form):
    from_file = forms.CharField()
    to_file = forms.CharField()

class PickFileForm(forms.Form):
    file_picked = forms.FileField()

class DataForm(forms.Form):
    from_file = forms.CharField()
    to_file = forms.CharField()
    file_picked = forms.FileField()
