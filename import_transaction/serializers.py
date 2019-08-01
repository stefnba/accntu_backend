from decimal import Decimal
from rest_framework import serializers
from .models import (
    FileUpload,
)
from .utils.fx_rate import FXRate
from transactions.models import (
    Transaction
)
from users.models import Settings



# from accounts.models import Account

class ImportSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):

        # print(data)

        # get user, and user_currency
        request = self.context.get('request', None)
        user_currency = Settings.objects.get(user_id=request.user.id).user_currency
        
        # fx conversion
        fx = FXRate(data['date'], data['account_currency'], user_currency)

        # modify serializer
        modified_data = data
        
        modified_data['account'] = int(3)
        # modified_data['account'] = int(data['account'])
        
        modified_data['account_user_rate'] = fx.get_rate()
        modified_data['user_amount'] = fx.get_amount(data['account_amount'])
        modified_data['user_currency'] = user_currency

        # correct spending_account_rate
        modified_data['spending_account_rate'] = str(round(Decimal(data['account_amount']) / Decimal(data['spending_amount']), 4))

        return super().to_internal_value(modified_data)

    class Meta:
        model = Transaction
        fields = '__all__'


    

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ('account', 'upload_file',)