from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import os
import zipfile


def model_form_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            for f in request.FILES.getlist('file'):
                filename = f.name

            form.save()
            return HttpResponseRedirect('success/' + filename + '/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {
        'form': form
    })


def get_z_coordinate(request, file_name):
    zip_file = zipfile.ZipFile('media/' + file_name)
    zip_file_name = os.path.splitext(file_name)[0]
    zip_file.extractall('media/' + zip_file_name)
    return render(request, 'upload_result.html')
