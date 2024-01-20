
def add_plus(number: str) -> str:
    if number.startswith("+"):
        return number
    return "+" + number
