from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


from .utils.fx_rate import FXRate
from transactions.models import (
    Transaction
)
from users.models import Settings



# from accounts.models import Account

class ImportSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):

        # get user, and user_currency
        user = self.context.get('user', None)

        try:
            user_currency = Settings.objects.get(user_id=user).user_currency
        except ObjectDoesNotExist:
            print(user)
            return False


        # FX conversion
        fx = FXRate(data['date'], data['account_currency'], user_currency)

        # modify data
        modified_data = data
        modified_data['account'] = int(data['account'])
        modified_data['account_user_rate'] = fx.get_rate()
        modified_data['user_amount'] = fx.get_amount(data['account_amount'])
        modified_data['user_currency'] = user_currency

        # correct spending_account_rate
        modified_data['spending_account_rate'] = str(round(Decimal(data['account_amount']) / Decimal(data['spending_amount']), 4))

        return super().to_internal_value(modified_data)

    def create(self, validated_data):
        """ Check if transactions already exists in db before saving """

        if Transaction.objects.filter(hash_duplicate=validated_data['hash_duplicate']).exists():
            return False

        return super().create(validated_data)

    class Meta:
        model = Transaction
        fields = '__all__'


