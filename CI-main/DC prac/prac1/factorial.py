import math

def calculate_factorial(n):
    """Calculates the factorial of a given integer."""
    if not isinstance(n, int):
        return "Error: Input must be an integer."
    if n < 0:
        return "Error: Factorial is not defined for negative numbers."
    try:
        return math.factorial(n)
    except OverflowError:
        return "Error: Integer too large for factorial calculation"