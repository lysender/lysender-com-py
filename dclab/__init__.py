# DC Lab Cluster helpers

import os
import uuid
import yaml
import datetime

def generate_uuid():
    """Returns a uuid version 4 in string format"""
    return uuid.uuid4().hex

def get_valid_date(str_date, format='%Y-%m-%d'):
    """Returns the datetime object from the string date format"""
    ret = None
    if isinstance(str_date, str) or isinstance(str_date, unicode):
        try:
            ret = datetime.datetime.strptime(str(str_date), format)
        except ValueError:
            ret = None
            
    return ret

def get_yaml_config(filename):
    """Returns a config object from a yaml document"""
    config = {}
    filename = os.path.join('dclab', 'config', filename)
    try:
        stream = file(filename, 'r')
        config = yaml.load(stream)
        stream.close()
    except IOError:
        config = {}

    return config
