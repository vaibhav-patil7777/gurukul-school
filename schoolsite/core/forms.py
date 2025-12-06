from django import forms

class MultiUploadForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    event = forms.CharField(required=False)
    description = forms.CharField(required=False, widget=forms.Textarea)
    date = forms.DateField(required=False)
