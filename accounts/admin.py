from django.contrib import admin

# Register your models here.
from .models import (Account, Provider)


admin.site.register(Account)
admin.site.register(Provider)