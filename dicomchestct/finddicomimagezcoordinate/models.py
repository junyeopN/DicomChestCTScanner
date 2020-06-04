from django.db import models


class UploadFileModel(models.Model):
    title = models.TextField(default='', max_length=10)
    file = models.FileField(null=True)