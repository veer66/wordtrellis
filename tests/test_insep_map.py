from wordtrellis import *
class TestInsepMap(object):
    def setup(self):
        txt = "".join([u"a" for i in range(10)])
        trellis = TrellisImpl(txt)
        elements = [(0, 3), (4,6), (8,10)]
        for e in elements:
            trellis.add_element(
                ElementImpl(
                    s = e[0], 
                    e = e[1],
                    element_type = ElementType.INSEPARABLE_UNIT,
                    value = None))
        self._insep_map = InsepMap(trellis)

    def test_can_link_0_3(self):
        assert self._insep_map.can_link(0,3)
        
    def test_can_link_0_4(self):
        assert self._insep_map.can_link(0,4)
        
    def test_can_link_0_5(self):
        assert not self._insep_map.can_link(0,5)    
        
    def test_can_link_8_10(self):
        assert self._insep_map.can_link(8, 10)
                                     
    def test_can_link_9_10(self):
        assert not self._insep_map.can_link(9, 10)
                                     
    def test_can_link_4_6(self):
        assert self._insep_map.can_link(4, 6)

    def test_can_link_3_7(self):
        assert self._insep_map.can_link(3, 7)

    def test_can_link_3_7(self):
        assert self._insep_map.can_link(3, 6)

    def test_can_link_3_5(self):
        assert not self._insep_map.can_link(3, 5)

    def test_can_link_3_4(self):
        assert self._insep_map.can_link(3, 4)
        
    def test_can_link_1_2(self):
        assert not self._insep_map.can_link(1, 2)    
