import hashlib
import json
import pandas as pd
from io import StringIO


class BaseExtractor(object):

    def __init__(self, data, sep, skiprows, cutrows):
        self.data = data
        self.sep = sep
        self.skiprows = skiprows
        self.cutrows = cutrows


        # key caching
        self.key_cache = {}


    def return_extracted_transactions(self):

        csv = StringIO(self.data)

        try:

            df = pd.read_csv(csv, sep=self.sep, skiprows=self.skiprows, na_filter=False, error_bad_lines=False)
            trans_dict = df.to_dict('records')

            # cut last rows in csv dict (e.g. Deutsche Bank)
            if self.cutrows is not None and self.cutrows > 0:
                trans_dict = trans_dict[:-self.cutrows]

            # add key to every transaction
            return [self.add_key(transaction) for transaction in trans_dict]

        except:
            print('failed to extract transactions from csv')
            return False


    def add_key(self, transaction):
        values = list(transaction.values())
        
        # create single key
        key = hashlib.md5(json.dumps(values, sort_keys=True).encode('utf-8')).hexdigest()
        
        # get key occurences
        occs = self.key_cache.get(key, 0)
        
        # create key with occs and assign to transaction
        transaction['key'] = hashlib.md5((key + str(occs)).encode('utf-8')).hexdigest()
        
        self.key_cache[key] = occs + 1
        return transaction