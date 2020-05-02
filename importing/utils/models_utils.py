import os
from datetime import datetime, date


def get_file_path(instance, filename):
    """
    Set path and filename of imported csv file
    :return: 
    """
    
    account_key = str(instance.account.provider.key)
    dt = datetime.now()
    user = instance.user.id

    extension = os.path.splitext(filename)[1:]
    filename_new = "{}_{}{:02d}{:02d}_{:02d}{:02d}{:02d}_{}.csv".format(
                                            account_key, 
                                            dt.year, 
                                            dt.month, 
                                            dt.day, 
                                            dt.hour, 
                                            dt.minute, 
                                            dt.second, 
                                            filename
                                        )

    return 'imports/{}/{}/{:02d}/{}/{}'.format(user, dt.year, dt.month, account_key, filename_new)



def get_image_path(instance, filename):
    """
    Set impage path and filename of photo TAN image
    :return: 
    """
    
    account_key = str(instance.account.provider.key)
    dt = datetime.now()
    user = instance.user.id

    extension = os.path.splitext(filename)[1:]
    filename_new = "{}_{}{:02d}{:02d}_{:02d}{:02d}{:02d}{}".format(
                                            account_key, 
                                            dt.year, 
                                            dt.month, 
                                            dt.day, 
                                            dt.hour, 
                                            dt.minute, 
                                            dt.second, 
                                            extension
                                        )

    return 'auth/photo_tan/{}/{}/{:02d}/{}'.format(user, dt.year, dt.month, filename_new)


def get_upload_file_path(instance, filename):
    """
    Get path and filename of UPLOADED csv file
    :return: 
    """
    
    account_key = str(instance.account.provider.key)
    dt = datetime.now()
    user = instance.user.id

    extension = os.path.splitext(filename)[1:]
    name = os.path.splitext(filename)[:1]
    filename_new = "{}_{}{:02d}{:02d}_{:02d}{:02d}{:02d}_{}_upload_file{}".format(
                                            account_key, 
                                            dt.year, 
                                            dt.month, 
                                            dt.day, 
                                            dt.hour, 
                                            dt.minute, 
                                            dt.second, 
                                            name,
                                            extension
                                        )

    return 'imports/{}/{}/{:02d}/{}/{}'.format(user, dt.year, dt.month, account_key, filename_new)