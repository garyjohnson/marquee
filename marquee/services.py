_shared_data = {}

def get(key):
    if key not in _shared_data:
        _shared_data[key] = key()

    return _shared_data[key]
