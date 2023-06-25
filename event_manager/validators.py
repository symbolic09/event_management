from datetime import datetime

def validate_text(data: str):
    return isinstance(data, str) and data

def validate_datetime(data: str):
    try:
        x = datetime.strptime(data, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except:
        return False

def validate_int(data: int):
    return isinstance(data, int)