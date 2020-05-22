from rest_framework import serializers

from .models import (
    Account,
    Provider
)

class ProviderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('key', 'provider', 'access_type', 'logo')


class AccountListSerializer(serializers.ModelSerializer):
    " List all Accounts for user "

    provider = ProviderListSerializer()
    
    class Meta:
        model = Account
        fields = ('title','id', 'provider')


class AccountFullListSerializer(serializers.ModelSerializer):
    " List all Accounts for user with all fields "

    provider = ProviderListSerializer()
    
    class Meta:
        model = Account
        fields = '__all__'



class AccountForTransactionSerializer(serializers.ModelSerializer):
    " Provide account info for Transaction "
    
    class Meta:
        model = Account
        fields = ('title','id')