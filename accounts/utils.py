import datetime

def generate_unique_uuid_string():
    now = datetime.datetime.now()
    unique_string = now.strftime("%Y-%m-%d_%H-%M-%S.%f")

    return f'ZIX-CONVERTER {unique_string}'
