from django import forms


from django import forms
from .models import UploadFileModel


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFileModel
        fields = ('title', 'file')
        widgets = {
          'title': forms.Textarea(attrs={'rows': 1, 'cols': 45}),
        }
