from django.contrib import admin

# Register your models here.
from .models import (
    Bucket,
    Label,
    Icon,
)

admin.site.register(Bucket)
admin.site.register(Label)
admin.site.register(Icon)