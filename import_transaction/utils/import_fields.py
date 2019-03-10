
FIELDS = {
    'spending_amount': {
        'required': True,
        'multiple': False,
    },
    'spending_currency': {
        'required': True,
        'multiple': False,
    },
}

DB_FIELDS = {
    'account_amount': {
        'type': 'amount_field',
        'options': [
            'column', 'column_secondary', 'column_debit',
            'column_credit', 'default', 'regex', 
            'negative_for_debit', 'decimal_sep', 'thousand_sep'
        ]
    },
    'spending_amount': {
        'type': 'amount_field',
        'options': [
            'column', 'column_secondary', 'column_debit',
            'column_credit', 'default', 'regex', 
            'negative_for_debit', 'decimal_sep', 'thousand_sep'
        ]
    },
}


# 
    # 'date': 'date_field',