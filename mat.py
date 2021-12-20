"""
provides math functions for the calulator
"""

def factorial (n):
    f = 1
    for i in range(2, n+1):
        f *= i
    return f