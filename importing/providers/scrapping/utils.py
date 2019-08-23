from django.core.cache import cache

import hashlib
import json
import time

def wait_for_tan(user, account, task, timeout=30, period=0.25, *args, **kwargs):
    
    key = '{}_{}_{}'.format(user, account, task)
    mustend = time.time() + timeout
    
    while time.time() < mustend:
        tan = cache.get(key)
        if tan:
            print('cache set')
            return tan
        
        print('waiting')
        time.sleep(period)

    print('timeout')
    return False



def hash_url(*argv):
    """ Hash url with given parameters for db retrival via hash """


    params = [param for param in argv]

    return hashlib.md5(json.dumps(params, sort_keys=True).encode('utf-8')).hexdigest()