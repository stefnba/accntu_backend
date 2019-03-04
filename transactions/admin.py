from django.contrib import admin

# Register your models here.
from .models import (FX, Transaction)


admin.site.register(FX)
admin.site.register(Transaction)