import tst_factory
from wordbreaktst import TstIter
from wordtrellis import *

class TestTstDictTransducer(object):
    def setup(self):
        tst = tst_factory.get_default_tst()
        self.tdt = TstDictTransducer(tst = tst,
                                     tst_iter_class = TstIter,
                                     state_class = TstDictState)        
        
    def teardown(self):
        pass
        
    def test_happy_state_apply(self):
        state = self.tdt.get_start_state(0)
        assert state.apply(u'a') == True
        assert state.apply(u'b') == True
        assert state.apply(u'c') == True
        assert state.apply(u'd') == False

    def test_happy_state_apply(self):
        state = self.tdt.get_start_state(0)
        assert state.apply(u'a') == True
        assert state.apply(u'b') == True
        assert state.apply(u'c') == True
        assert state.apply(u'd') == False
        
    def test_happy_state_apply_happy_false(self):
        state = self.tdt.get_start_state(0)
        assert state.apply(u'A') == False

    def test_happy_state_is_break_start(self):
        state = self.tdt.get_start_state(0)
        assert state.is_break() == False

    def test_happy_state_is_break_happy(self):
        state = self.tdt.get_start_state(0)
        assert state.apply(u'a') == True
        assert state.is_break() == True

    def test_happy_state_is_break_false_state(self):
        state = self.tdt.get_start_state(0)
        assert state.apply(u'k') == False
        assert state.is_break() == False
