from rest_framework import serializers

from .models import (
    Account,
    Provider
)

class ProviderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = (
            'id',
            'key',
            'provider',
            'access_type',
            'logo',
            'provider_type',
            'currency',
            'country',
            'login_required',
        )


class AccountListSerializer(serializers.ModelSerializer):
    " List all Accounts for user "

    provider = ProviderListSerializer()
    
    class Meta:
        model = Account
        fields = ('title','id', 'provider')


class AccountCreateRetrieveUpdateSerializer(serializers.ModelSerializer):
    """
    Retrieve and update single account
    """

    # provider = ProviderListSerializer()
    # provider = ProviderListSerializer(read_only=True)

    class Meta:
        model = Account
        fields = (
            'id',
            'title',
            'last_import',
            'first_import_success',
            'login',
            'login_sec',
            'pin',
            'provider',
            'provider_id',
        )

        read_only_fields = (
            'last_import',
            'first_import_success',
        )


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