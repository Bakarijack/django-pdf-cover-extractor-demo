from .models import Pdffile
from django import forms

class PdffileForm(forms.ModelForm):
    class Meta:
        model = Pdffile
        fields = (
            'pdf',
            'filename',
            'pagenumforcover',
        )