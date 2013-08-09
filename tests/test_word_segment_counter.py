from wordtrellis import *
class TestWordSegmentCounter:
    def setup(self):
        self.wsc = WordSegmentCounter()
        self.trellis = TrellisImpl(u"".join([u"a" for i in range(10)]))
        e1 = ElementImpl(s = 2, 
                         e = 4, 
                         value = None, 
                         element_type = ElementType.WORD)
        e2 = ElementImpl(s = 4, 
                         e = 6, 
                         value = None, 
                         element_type = ElementType.WORD)
        self.trellis.add_element(e1)
        self.trellis.add_element(e2)
    
    def test_count_happy_4_6(self):
        c = self.wsc.count(self.trellis, 4, 6)        
        assert c == -1
        
    def test_count_happy_2_6(self):
        c = self.wsc.count(self.trellis, 2, 6)        
        assert c == -2
        
    def test_count_happy_1_6(self):
        c = self.wsc.count(self.trellis, 1, 6)        
        assert c == 0
    
    def test_count_happy_2_5(self):
        c = self.wsc.count(self.trellis, 2, 5)        
        assert c == 0
    
    def test_count_happy_2_7(self):
        c = self.wsc.count(self.trellis, 2, 7)        
        assert c == 0
        
    def test_count_happy_0_10(self):
        c = self.wsc.count(self.trellis, 0, 10)        
        assert c == 0
    
    def test_count_happy_0_20(self):
        #FIXME: should raise error?
        c = self.wsc.count(self.trellis, 0, 20)        
        assert c == 0
