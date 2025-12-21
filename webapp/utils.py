import re
def is_strong_password(password: str):
    """
    Simple & safe password validator

    Rules:
    - Minimum 5 characters
    - At least 1 digit
    - At least 1 special character

    Returns:
    - (True, None) if valid
    - (False, error_message) if invalid
    """

    if not password or len(password) < 5:
        return False, "Signup error,Password must be at least 5 characters long."

    if not re.search(r"\d", password):
        return False, "Signup error,Password must contain at least one number."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Signup error ,Password must contain at least one special character."

    return True, None
