from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


from .utils.fx_rate import FXRate
from transactions.models import (
    Transaction
)
from users.models import Settings



class ImportSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        # Check if transactions already exists in db before saving
        t = Transaction.objects.filter(hash_duplicate=validated_data['hash_duplicate'])
        if t.exists():
            return False

        return super().create(validated_data)

    class Meta:
        model = Transaction
        fields = '__all__'


