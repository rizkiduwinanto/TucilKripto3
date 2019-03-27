
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import math
import time
import random
import functools


def timer(func):
    """Record elapsed time in a function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        t = time.time()
        func(*args, **kwargs)
        print("[%s] Elapsed %.6f second" % (func.__name__, time.time()-t))
        return func(*args, **kwargs)
    return wrapper_timer

def modInverse(a, m) : 
    """Return a^-1 mod m"""
    a = a % m; 
    for x in range(1, m) : 
        if ((a * x) % m == 1) : 
            return x 
    return 1


# In[2]:


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
    """Encoding integer to a character"""
    return chr(ord('a') + code-10)


def generate_x(m, k, offset):
    """Yielding x by a function"""
    return m*k+offset


def encode(k, n, p, a, b, message_char):
    """Return encoded point"""
    m = encode_char(message_char)

    # Find solveable y
    for i in range(1, k):
        x = generate_x(m, k, i)
        y = is_y_exist(p, a, b, x)
        if (y != -1):
            break
    return Point(x, y)


def decode(k, x):
    """Return message char"""
    code = math.floor((x-1)/k)
    return decode_code(code)


# In[3]:


@timer
def do_encoding(k, n, p, a, b, messages):
    """Do the encoding things"""
    enc_messages = [encode(k, n, p, a, b, m) for m in messages]
    return enc_messages


@timer
def do_decoding(k, message_point):
    """Do the decoding things"""
    dec_messages = [decode(k, point.x) for point in message_point]
    return dec_messages


# ## ECC Class

# In[4]:


class classproperty(object):
    def __init__(self, f):
        self.f = classmethod(f)
    def __get__(self, *a):
        return self.f.__get__(*a)()
    
class Point(object):
    """ Point class
    Attributes
        x: axis position
        y: ordinat position
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    @classproperty
    def INFINITY(self):
        return Point(-1, -1)
    
    def is_infinity(self):
        return (self.x == -1 and self.y == -1)
    
    def __str__(self):
        return "Point({}, {})".format(self.x, self.y)
    
    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)
        
               
class ECC(object):
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
    
    def get_y_square(self, x):
        """Return y_square of x"""
        return (x**3 + self.a*x + self.b)  % self.p
    
    def is_on_curve(self, point):
        """Check whether a point is on curve"""
        return (point.y**2 % self.p) == self.get_y_square(point.x)
    
    def subtract(self, point_p, point_q):
        """Subtract two points in ECC (P - Q)
        Return
            point as a subtraction result
        """
        if (point_p.is_infinity()):
            return point_q
        if (point_q.is_infinity()):
            return point_p
        if (point_p.x == point_q.x and point_p.y == point_q.y):
            return Point.INFINITY
        
        p_q_new= Point(point_q.x, (-point_q.y) % self.p)
        return self.add(point_p, p_q_new)
    
    def add(self, point_p, point_q):
        """Sum two points in ECC (P + Q)
        Return
            point as an addition result
        """
        if (point_p.is_infinity()):
            return point_q
        if (point_q.is_infinity()):
            return point_p
        
        if (point_p.x == point_q.x and point_p.y == point_q.y):
            if (point_p.y == 0):
                return Point.INFINITY
            grad = (3*(point_p.x**2) + self.a) * modInverse(2*point_p.y, self.p)
            grad = int(grad) % self.p
            x_r = (grad**2 - 2*point_p.x) % self.p
            y_r = (grad*(point_p.x - x_r) - point_p.y) % self.p
            return Point(x_r, y_r)
        else:
            grad = (point_p.y - point_q.y)*modInverse(point_p.x - point_q.x, self.p)
            grad = grad% self.p
            x_r = (grad**2 - point_p.x - point_q.x) % self.p
            y_r = (grad*(point_p.x - x_r) - point_p.y ) % self.p
            return Point(x_r, y_r)
        
    def iteration(self, point_p, k):
        if k >= 2:
            p = self.add(point_p, point_p)
            for i in range(k-2):
                p = self.add(p, point_p)
            return p 
        elif k == 1:
            return point_p
        else:
            print("Unhandled k = ",k)
        


# ## ECC Diffie Hellman

# In[5]:


ecc_dh = ECC(2, 1, 5) 
basis = Point(0,1)
points = [
    Point(0,1),
    Point(1,3),
    Point(3,3),
    Point(3,2),
    Point(1,2),
    Point(0,4)
]
a = 2 # Alice's
b = 3 # Bobs'

point_a = ecc_dh.iteration(basis,a)
print(point_a, "is on curve: ", ecc_dh.is_on_curve(point_a))
point_b = ecc_dh.iteration(basis,b)
print(point_b, "is on curve: ", ecc_dh.is_on_curve(point_b))

# Alice compute shared key for given point_b from bob
shared_key_a = ecc_dh.iteration(point_b,a)
print("Shared key Alice's:",shared_key_a, "is on curve: ", ecc_dh.is_on_curve(shared_key_a))

# Bob compute shared key for given point_a from alice
shared_key_b = ecc_dh.iteration(point_a, b)
print("Shared key Bob's:",shared_key_b, "is on curve: ", ecc_dh.is_on_curve(shared_key_b))


# ## ECC El Gamal

# In[6]:


ecc_el_gamal = ECC(2, 1, 5) 
basis = Point(0,1)
points = [
    Point(0,1),
    Point(1,3),
    Point(3,3),
    Point(3,2),
    Point(1,2),
    Point(0,4)
]
# Alice's
private_a = 2
public_a = ecc_el_gamal.iteration(basis, private_a)
print("Alice's public key", public_a, "is on curve: ", ecc_el_gamal.is_on_curve(public_a))

# Bob's
private_b = 3
public_b = ecc_el_gamal.iteration(basis, private_b)
print("Alice's public key", public_b, "is on curve: ", ecc_el_gamal.is_on_curve(public_b))

# Encoded message
point_m = Point(3, 2)
print("Point message:", point_m, "is on curve: ", ecc_el_gamal.is_on_curve(point_m))


# Other random number 
k = 3

# Alice encrypting message
# Cipherteks (pair of points)
p1 = ecc_el_gamal.iteration(basis, k)
print("Point Cipher 1:", p1, "is on curve: ", ecc_el_gamal.is_on_curve(p1))

p2 = ecc_el_gamal.add(point_m, ecc_el_gamal.iteration(public_b, k))
print("Point Cipher 2:", p2, "is on curve: ", ecc_el_gamal.is_on_curve(p2))

pc = [
    p1,
    p2
]

# Bob decrypting message
decrypted_pm = ecc_el_gamal.subtract(pc[1], ecc_el_gamal.iteration(pc[0],private_b))
print("Decrypted point message:", decrypted_pm, "is on curve: ", ecc_el_gamal.is_on_curve(decrypted_pm))


# ## ECC El Gamal + encoding koblitz

# In[7]:


# CONFIG
k = 20
p = 751
a = -1
b = 188
n = 727
str_message = "jokowi pki"

# ECC Elgamal
print("[ Initializing ECC El Gamal ]")
ecc = ECC(a, b, p)
y = is_y_exist(p,a,b,0)
point_basis =  Point(0,y) if (y != -1) else Point.INFINITY
print("Basis: ",point_basis)


# Alice's
print("\n[ Alice's ]")
private_a = random.randint(1,n)
public_a = ecc.iteration(point_basis, private_a)
print("Alice's public point:",public_a,"is_on_curve:",ecc.is_on_curve(public_a))

# Bob's
print("\n[ Bob's ]")
private_b = random.randint(1,n)
public_b = ecc.iteration(point_basis, private_b)
print("Bob's public point:",public_b,"is_on_curve:",ecc.is_on_curve(public_b))

# Encrypting messages 
print("\n[ Encrypting ]")
messages = str_message
print("Original message:",messages)
encoded_messages = do_encoding(k, n, p, a, b, messages)
print("Encoded message: ",encoded_messages)
choosen_k = k
encrypted_messages = [
    (ecc.iteration(point_basis, choosen_k),
     ecc.add(point_message, ecc.iteration(public_b, choosen_k)))
    for point_message in encoded_messages
]
print("Encrypted message: ", encrypted_messages)


# Encrypting messages 
print("\n[ Decrypting ]")
decrypted_messages = [
    ecc.subtract(
        message[1],
        ecc.iteration(message[0], private_b)
    )
    for message in encrypted_messages
]
print("Decrypted point messages: ",decrypted_messages)
decoded_messages = do_decoding(choosen_k, decrypted_messages)
print("Decoded messges: ",decoded_messages)
message = "".join(decoded_messages)
print("Message: ",message)

