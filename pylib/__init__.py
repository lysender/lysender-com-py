# DC Lab Cluster helpers

import uuid

def generate_uuid():
    """Returns a uuid version 4 in string format"""
    return uuid.uuid4().hex