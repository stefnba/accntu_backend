from django.contrib import admin

# Register your models here.
from .models import (
    NewImport,
)

admin.site.register(NewImport)