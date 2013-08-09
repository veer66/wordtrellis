from wordtrellis import *
class TestTrellis(object):
    def setup(self):
        self.trellis = TrellisImpl()
        
    def test_get_element_by_s_from_empty(self):
        assert len(self.trellis.get_elements_by_s(0)) == 0 
        
    def test_get_element_by_e_from_empty(self):
        assert len(self.trellis.get_elements_by_e(0)) == 0
        
    def test_get_element_by_s_happy(self):
        element = ElementImpl(3,5,0,0)
        self.trellis.add_element(element)
        assert self.trellis.get_elements_by_s(3)[0] == element
        
    def test_get_element_by_e_happy(self):
        element = ElementImpl(3,5,0,0)
        self.trellis.add_element(element)
        assert self.trellis.get_elements_by_e(5)[0] == element
        
    def test_get_element_by_se_happy(self):
        element = ElementImpl(3,5,0,0)
        self.trellis.add_element(element)
        assert self.trellis.get_elements_by_se(3, 5)[0] == element
        

