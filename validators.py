import re

def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_valid_naming(name: str) -> bool:
    if name is None or len(name) < 2:
        return False
    return True

def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_phone_number(phone_number: str) -> bool:
    pattern = r'^\+?\d{5,15}$'
    return re.match(pattern, phone_number) is not None

def is_valid_zipcode(zipcode: str) -> bool:
    pattern = r'^\d{4,10}$'
    return re.match(pattern, zipcode) is not None