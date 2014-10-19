from random import *

def random_walk(n):
    x = [gauss(0,0.01)]
    for step in range(n-1):
        x.append(x[-1] + gauss(0,0.01))
    return x
