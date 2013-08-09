from wordbreaktst import Tst
from wordbreaktst import TstIter

def get_default_tst():
    tst = Tst()
    data = [(u'ab', 1), (u'bc', 2), (u'abc', 3), 
            (u'd',4), (u'a', 5), (u'bcd', 6)]
    data.sort(lambda x, y: cmp(x[0], y[0]))
    tst.insert_sorted_array(data)   
    return tst
    
