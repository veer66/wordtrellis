from transducer import Transducer
from transducer import State

class TstDictTransducer(Transducer):
    def __init__(self, tst, tst_iter_class, state_class):
        self._tst = tst
        self._tst_iter_class = tst_iter_class
        self._state_class = state_class
        
    def get_start_state(self, s):
        return self._state_class(self._tst_iter_class(self._tst), s)
        
class TstDictState(State):
    def __init__(self, tst_iter, s):
        self._tst_iter = tst_iter
        self._s = s

    def apply(self, ch):
        return self._tst_iter.apply(ch)

    def get_value(self):
        return self._tst_iter.get_value()

    def is_break(self):
        return self._tst_iter.is_break_pos()

    def get_s(self):
        return self._s