from trellis import ElementType

class ElementFeeder:
    def feed(self, trellis, s, e, value):
        pass

class SimpleWordFeeder(ElementFeeder):
    def __init__(self, element_class):
        self._element_class = element_class
        
    def feed(self, trellis, s, e, value):
        trellis.add_element(self._element_class(s, e, ElementType.WORD))