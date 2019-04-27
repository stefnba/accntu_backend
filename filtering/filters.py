from django.db.models import Q

from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES

from transactions.models import (
    Transaction
)


FILTER_FIELDS = (
    'account',
    'account_currency', 
    'counterparty',
    'country',
    'date', 
    'spending_currency', 
    'status',
    'category',
    'label',
)



class ListFilter(filters.Filter):

    def filter(self, qs, value):

        if value in EMPTY_VALUES:
                return qs
        if self.distinct:
            qs = qs.distinct()

        multiple_values = value.split(u',')

        lookup = '%s__%s' % (self.field_name, self.lookup_expr)
        return self.get_method(qs)(Q(**{lookup: multiple_values}))

        # if len(multiple_values) > 1:
        #     # override filter with Q filter if multiple values
        #     return self.get_method(qs)(Q(**{lookup: multiple_values}))

        # else:
        #     return self.get_method(qs)(**{lookup: value})


class TransactionFilterSet(filters.FilterSet):
    # account = filters.NumberFilter(field_name='account', lookup_expr = 'in')
    account = ListFilter(field_name='account', lookup_expr = 'in')
    date = ListFilter(field_name='date', lookup_expr = 'in')
    spending_currency = ListFilter(field_name='spending_currency', lookup_expr = 'in')
    category = ListFilter(field_name='category', lookup_expr = 'in')
    status = ListFilter(field_name='status', lookup_expr = 'in')
    label = ListFilter(field_name='label', lookup_expr = 'in')
    

    class Meta:
        model = Transaction
        fields = FILTER_FIELDS