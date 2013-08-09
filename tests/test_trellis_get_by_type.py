from wordtrellis import *

class TestTrellisGetByType(object):
    def setup(self):
        self.trellis = TrellisImpl()
        self.trellis.add_element(
            ElementImpl(s = 1, e = 1, 
                element_type = ElementType.INSEPARABLE_UNIT, value = 1))
        self.trellis.add_element(
            ElementImpl(s = 2, e = 2, 
                element_type = ElementType.WORD, value = 2))
        self.trellis.add_element(
            ElementImpl(s = 3, e = 3, 
                element_type = ElementType.UNCERTAIN_UNIT, value = 2))        
        
    def test_get_insep_only(self):
        elements = self.trellis.get_elements(ElementType.INSEPARABLE_UNIT)
        assert len(elements) == 1
        assert elements[0].get_type() == ElementType.INSEPARABLE_UNIT
        
    def test_get_insep_and_word(self):
        elements = self.trellis.get_elements(ElementType.INSEPARABLE_UNIT | ElementType.WORD)
        assert len(elements) == 2
        s1 = set()
        for e in elements:
            s1.add(e.get_type())
        s2 = set()
        s2.add(ElementType.WORD)
        s2.add(ElementType.INSEPARABLE_UNIT)
        assert s1 == s2

    def test_get_all(self):
        elements = self.trellis.get_elements(ElementType.ALL)
        assert len(elements) == 3
        s1 = set()
        s1 = set()
        for e in elements:
            s1.add(e.get_type())
        s2 = set()
        s2.add(ElementType.WORD)
        s2.add(ElementType.INSEPARABLE_UNIT)
        s2.add(ElementType.UNCERTAIN_UNIT)
        assert s1 == s2
