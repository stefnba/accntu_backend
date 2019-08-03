from rest_framework import serializers

from .models import (
    Account,
    Provider
)

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('key', 'provider', 'parser_map', 'access_type')


class AccountListSerializer(serializers.ModelSerializer):
    " List all Accounts for user "

    provider = ProviderSerializer()
    
    class Meta:
        model = Account
        fields = ('title','id', 'provider')


class AccountFullListSerializer(serializers.ModelSerializer):
    " List all Accounts for user with all fields "

    provider = ProviderSerializer()
    
    class Meta:
        model = Account
        fields = '__all__'