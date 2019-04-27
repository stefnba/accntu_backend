from django.contrib import admin

# Register your models here.
from .models import (Bucket, Label)

admin.site.register(Bucket)
admin.site.register(Label)