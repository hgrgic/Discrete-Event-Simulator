import uuid


def get_unique_id():
    _id = uuid.uuid1()
    return _id.hex
