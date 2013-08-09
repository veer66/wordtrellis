        
def cmp_pairs(*args):
    for pair in args:
        a, b = pair
        r = cmp(a,b)
        if r != 0:
            return r


