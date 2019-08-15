
IMPORT_FIELDS = {
    'title': {
        'required': True,
        'type': 'text',
        'multiple': True,
    },
    'counterparty': {
        'required': True,
        'type': 'text',
        'multiple': True,
    },
    'reference_text': {
        'required': True,
        'type': 'text',
        'multiple': True,
    },
    'account_amount': {
        'type': 'amount',
    },
    'spending_amount': {
        'type': 'amount',
    },
    'spending_currency': {
        'required': True,
        'type': 'currency',
    },
    'account_currency': {
        'required': True,
        'type': 'currency',
    },
    'date': {
        'type': 'date',
    },
    'hash_duplicate': {
        'required': True,
    },
    'iban': {
        'required': True,
    },
    'bic': {
        'required': True,
    },
}