from rest_framework import serializers

from transactions.models import (
    Transaction
)

from .models import NewImport

class ImportListSerializer(serializers.ModelSerializer):
    """
    List all imports
    """
    
    class Meta:
        model = NewImport
        fields = ('imported_at','nmbr_transactions', 'import_success')



class ImportSerializer(serializers.ModelSerializer):
    """
    Bulk creation of transactions following import/upload
    """

    def create(self, validated_data):

        # Check if transactions already exists in db before saving
        t = Transaction.objects.filter(hash_duplicate=validated_data['hash_duplicate'])
        if t.exists():
            return False

        return super().create(validated_data)

    class Meta:
        model = Transaction
        fields = '__all__'


