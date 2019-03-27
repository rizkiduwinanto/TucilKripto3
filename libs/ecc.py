from .utils import *

"""Implementation of Eliptic curve cryptography"""
__author__ = "Azis Adi Kuncoro"

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
            x_r = (grad**2 - point_p.x - point_q.x) % self.p
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
        
