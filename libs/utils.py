""" Utils """
import functools
import time

def timer(func):
    """Record elapsed time in a function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        t = time.time()
        func(*args, **kwargs)
        print("[%s] Elapsed %.6f second" % (func.__name__, time.time()-t))
        return func(*args, **kwargs)
    return wrapper_timer

def modInverse(x, p) : 
    """
    Compute an inverse for x modulo p, assuming that x
    is not divisible by p.
    """
    if x % p == 0:
        print("X: {}, P:{}".format(x, p))
        raise ZeroDivisionError("Impossible inverse")
    return pow(x, p-2, p)

def y_square(p, a, b, x):
    """Compute y^2 in form x^3+ax+b mod p
    """
    return (x**3+a*x+b) % p


def is_y_exist(p, a, b, x):
    """Check whether any y exists for given x in ECC
    Returns:
        -1 is not exists, a number otherwise
    """
    y_sqr = y_square(p, a, b, x)
    for i in range(p):
        if ((i*i) % p == y_sqr):
            return i
    return -1


def encode_char(character):
    """Encoding character to an integer"""
    return 10 + ord(character.lower())-ord('a')


def decode_code(code):
    """Decoding integer to a character"""
    return chr(ord('a') + code-10)

def encode_byte(b):
    """Encoding byte to integer repr"""
    return int(b)

def decode_int(code):
    """Decoding int to byte repr"""
    # print("Code: ",code)
    return bytes([code])

def generate_x(m, k, offset):
    """Yielding x by a function"""
    return m*k+offset
