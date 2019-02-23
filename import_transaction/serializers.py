from rest_framework import serializers

from .models import (
    FileUpload,
)

"""
    Transaction
"""""""""""""""""""""""""""""""""""""""""""""

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ('account', 'upload_file', )