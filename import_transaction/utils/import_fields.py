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
    'date': {
        'type': 'date_field',
        'options': [
            'column', 'column_secondary', 'default', 
            'regex', 'format'
        ]
    },
    'title': {
        'type': 'text_field',
        'multiple': True,
        'options': [
            'column', 'column_secondary', 'default', 
            'regex', 'sep', 'stopwords'
        ]
    },
    'iban': {
        'type': 'text_field',
        'mandatory': False,
        'options': [
            'column', 'column_secondary', 'default', 
            'regex'
        ]
    },
    'bic': {
        'type': 'text_field',
        'mandatory': False,
        'options': [
            'column', 'column_secondary', 'default', 
            'regex'
        ]
    },
    'counterparty': {
        'type': 'text_field',
        'mandatory': False,
        'options': [
            'column', 'column_secondary', 'default', 
            'regex'
        ]
    },
    'spending_currency': {
        'type': 'text_field',
        'mandatory': False,
        'options': [
            'column', 'column_secondary', 'default', 
            'regex'
        ]
    },
    'account_currency': {
        'type': 'text_field',
        'mandatory': False,
        'options': [
            'column', 'column_secondary', 'default', 
            'regex'
        ]
    }
}


# 
    # 'date': 'date_field',