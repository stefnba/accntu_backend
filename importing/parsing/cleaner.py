
import re
from decimal import Decimal
from datetime import datetime

from .settings import IMPORT_FIELDS

class Cleaner(object):

    def __init__(self, cell_value, fieldname, field_map):
        
        self.fieldname = fieldname
        self.field_map = field_map
        
        # caching
        self.cleaned_value = cell_value
        # self.cleaned_value = None
        self.add_info = {}

        # do cleaning
        cell_value = cell_value
        
        field_type = IMPORT_FIELDS[fieldname].get('type', None)

        if field_type:
            getattr(self, 'clean_' + field_type)(cell_value)


    def clean_text(self, cell_value):
        self.cleaned_value = cell_value  
    

    def clean_currency(self, cell_value):
        self.cleaned_value = cell_value 

    def clean_date(self, cell_value):
        
        date_format = self.field_map.get('format', None)

        # timestamp format
        if date_format == 'ts':
            ts = int(cell_value) / 1000
            self.cleaned_value = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        else:
            
            try: 
                self.cleaned_value = str(datetime.strptime(cell_value, date_format).date())
            except ValueError:
                date_format = self.field_map.get('format_sec', None)
                self.cleaned_value = str(datetime.strptime(cell_value, date_format).date())


    def clean_amount(self, cell_value):
        
        # add status
        if '-' in cell_value:
            if self.fieldname is 'account_amount':
                self.add_info['status'] = 'debit'

            self.cleaned_value = cell_value.replace('-', '').strip()

        if '-' not in cell_value:
            if self.fieldname is 'account_amount':
                self.add_info['status'] = 'credit'

        if '+' in cell_value:
            self.cleaned_value = cell_value.replace('+', '').strip()

        # if dec sep is ,
        if re.match(r'^(\d{1,3}.{0,1}){1,5}\,(\d){2}$', self.cleaned_value):
            self.cleaned_value = self.cleaned_value.replace('.', '')
            self.cleaned_value = str(Decimal(self.cleaned_value.replace(',', '.')))
            return True
        
        # if thousand sep is ,
        if re.match(r'^(\d{1,3},{0,1}){1,5}\.(\d){2}$', self.cleaned_value):
            self.cleaned_value = str(Decimal(self.cleaned_value.replace(',', '')))
            return True

        # if thousand sep is '
        if re.match(r'^(\d{1,3}\'{0,1}){1,5}\.(\d){2}$', self.cleaned_value):
            self.cleaned_value = str(Decimal(self.cleaned_value.replace('\'', '')))
            return True

        self.cleaned_value = str(Decimal(self.cleaned_value))

    def get_cleaned_value(self):
        return self.cleaned_value
    

    def get_add_info(self):
        return self.add_info