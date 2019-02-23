from rest_framework import serializers

from .models import (
    Account,
)


class AccountListSerializer(serializers.ModelSerializer):
    " List all Accounts for user "
    
    class Meta:
        model = Account
        fields = ('title','id',)


class AccountFullListSerializer(serializers.ModelSerializer):
    " List all Accounts for user "
    
    class Meta:
        model = Account
        fields = '__all__'