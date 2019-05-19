import csv

from io import StringIO

from .import_errors import ERORRS


""" 
    Handles all the extraction of the csv file and return content of csv file
    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class ReadCSV(object):
    def __init__(self, csv_file):
        self.file = csv_file
        self.errors = []



    def get_content(self):
        csv_file = self.file
        
        csv_file.seek(0)

        # check if first row is header or other strings like sep=
        first_row = csv_file.readline()
        if 'sep=' not in str(first_row):
            csv_file.seek(0)

        content = StringIO(csv_file.read().decode('utf-8', errors='ignore'))
        # print(content)
        return csv.DictReader(content, delimiter=';')
    


    def is_valid(self):
        # set criteria
        max_size = 10 # in MB
        allowed_endings = ('.csv', '.CSV')
        allowed_content_type = 'text/csv'

        csv_file = self.file
        name = csv_file.name
        content_type = csv_file.content_type
        size = csv_file.size

        # check for errors
        if size > max_size * 1000000:
            return self.throw_error('FILE_SIZE')

        if not name.endswith(allowed_endings) or not content_type == allowed_content_type:
            return self.throw_error('FILE_TYPE')
        
        # if no error
        return True



    def throw_error(self, err):
        try:
            error = ERORRS[err]
            self.errors.append(error)
        except:
            print('no error code found')
        
        # if error was report, always return False
        return False



    def get_errors(self):
            return self.errors[0]