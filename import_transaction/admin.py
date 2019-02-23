from django.contrib import admin

# Register your models here.
from .models import (FileUpload, ImportUpload)


admin.site.register(FileUpload)
admin.site.register(ImportUpload)