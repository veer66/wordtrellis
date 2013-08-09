class ElementType:
    WORD = 0x1
    INSEPARABLE_UNIT = WORD << 1
    UNCERTAIN_UNIT = WORD << 2
    ALL = WORD | INSEPARABLE_UNIT | UNCERTAIN_UNIT

class Trellis:        
    def get_elements_by_s(self, s, element_type):
        pass
        
    def get_elements_by_e(self, e, element_type):
        pass
        
    def get_elements(self, element_type):
        pass
        
    def add_element(self, element):
        pass
        
    def set_text(self, text):
        pass
        
    def get_text(self):
        pass
        
class Element:

    def get_s(self):
        pass

    def get_e(self):
        pass

    def get_type(self):
        pass

    def get_value(self):
        pass

    def set_s(self, s):
        pass

    def set_e(self, e):
        pass

    def set_value(self, v):
        pass

class ElementImpl(Element):
    def __init__(self, s, e, element_type, value = None):
        self._s = s
        self._e = e
        self._value = value
        self._element_type = element_type

    def get_s(self):
        return self._s; 

    def get_e(self):
        return self._e;

    def get_type(self):
        return self._element_type

    def get_value(self):
        return self._value

    def set_s(self, s):
        self._s = s

    def set_e(self, e):
        self._e = e

    def set_value(self, v):
        self._value = v

    def __str__(self):
        return "(TrellisElement " + str(self._s) + ", " + str(self._e)  + " " + \
                str(self._element_type) + " )"
    
    def __repr__(self):
        return str(self)

class TrellisImpl(Trellis):
    def __init__(self, text = ""):
        self._s_idx = {}
        self._e_idx = {}
        self._se_idx = {}
        self._elements = []
        self._text = text

    def _filter_type(self, elements, element_type = None):
        if element_type != None:
            return filter(
                lambda element: (element.get_type() & element_type) > 0,
                elements)
        else:
            return elements

    def get_elements_by_s(self, s, element_type = None):
        if not self._s_idx.has_key(s):
            return []
        return self._filter_type(self._s_idx[s].keys(), element_type)

    def get_elements_by_e(self, e, element_type = None):
        if not self._e_idx.has_key(e):
            return []        
        return self._filter_type(self._e_idx[e].keys(), element_type)
        
    def get_elements_by_se(self, s, e, element_type = None):
        pair_str = "%d,%d" % (s, e)
        if not self._se_idx.has_key(pair_str):
            return []
        return self._filter_type(self._se_idx[pair_str].keys())

    def get_elements(self, element_type = None):
        return self._filter_type(self._elements, element_type);

    def _pair_to_string(self, element):
        return "%d,%d" % (element.get_s(), element.get_e())

    def _add_index(self, element):
        if not self._s_idx.has_key(element.get_s()):
            self._s_idx[element.get_s()] = {}
        self._s_idx[element.get_s()][element] = True

        if not self._e_idx.has_key(element.get_e()):
            self._e_idx[element.get_e()] = {}
        self._e_idx[element.get_e()][element] = True

        if not self._se_idx.has_key(self._pair_to_string(element)):
            self._se_idx[self._pair_to_string(element)] = {}
            self._se_idx[self._pair_to_string(element)][element] = True

    def add_element(self, element):
        self._add_index(element)
        self._elements.append(element)

    def set_text(self, text):
        self._text = text

    def get_text(self, element = None):
        if element == None:
            return self._text
        else:
            return self._text[element.get_s():element.get_e()]

    def __str__(self):
        return "(Trellis " + "\n".join([str(e) + 
                ":" + self.get_text(e).encode("UTF-8") 
                    for e in self._elements]) + " )"

