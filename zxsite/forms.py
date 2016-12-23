from django import forms

class PortraitForm(forms.Form):
    picfile = forms.FileField(
        label='select a pic',
        help_text= 'max. 42megabytes'
    )