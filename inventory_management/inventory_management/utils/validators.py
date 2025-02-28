import re

def validate_password(password):
    """
    Validate password strength.
    
    Requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    
    Returns a dict with 'valid' (bool) and 'message' (str) keys.
    """
    # Check length
    if len(password) < 8:
        return {
            "valid": False,
            "message": "Password must be at least 8 characters long"
        }
    
    # Check for uppercase letter
    if not re.search(r"[A-Z]", password):
        return {
            "valid": False,
            "message": "Password must contain at least one uppercase letter"
        }
    
    # Check for lowercase letter
    if not re.search(r"[a-z]", password):
        return {
            "valid": False,
            "message": "Password must contain at least one lowercase letter"
        }
    
    # Check for digit
    if not re.search(r"\d", password):
        return {
            "valid": False,
            "message": "Password must contain at least one digit"
        }
    
    # Check for special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return {
            "valid": False,
            "message": "Password must contain at least one special character"
        }
    
    return {
        "valid": True,
        "message": "Password meets requirements"
    }

def validate_sku(sku):
    """
    Validate product SKU format.
    
    Requirements:
    - 5 to 20 characters long
    - Alphanumeric characters and hyphens only
    - Must start with a letter
    - Must not end with a hyphen
    
    Returns a dict with 'valid' (bool) and 'message' (str) keys.
    """
    # Check length
    if len(sku) < 5 or len(sku) > 20:
        return {
            "valid": False,
            "message": "SKU must be between 5 and 20 characters long"
        }
    
    # Check if starts with a letter
    if not sku[0].isalpha():
        return {
            "valid": False,
            "message": "SKU must start with a letter"
        }
    
    # Check if ends with a hyphen
    if sku.endswith("-"):
        return {
            "valid": False,
            "message": "SKU must not end with a hyphen"
        }
    
    # Check for valid characters
    if not re.match(r"^[a-zA-Z0-9-]+$", sku):
        return {
            "valid": False,
            "message": "SKU must contain only letters, numbers, and hyphens"
        }
    
    return {
        "valid": True,
        "message": "SKU format is valid"
    }
