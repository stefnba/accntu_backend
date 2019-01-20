from rest_framework import serializers

from .models import (
    FileImport,
    Transaction,
)


"""
    Import
"""""""""""""""""""""""""""""""""""""""""""""

class FileImportSerializer(serializers.ModelSerializer):
    docfile = serializers.FileField(max_length=None, allow_empty_file=False, use_url=True)
    
    class Meta():
        model = FileImport
        fields = ('docfile', 'hash_string')


"""
    Transaction
"""""""""""""""""""""""""""""""""""""""""""""

class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'