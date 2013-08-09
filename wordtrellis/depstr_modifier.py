from modifier import TrellisModifier
from trellis import *

class DepStrTrellisModifier(TrellisModifier):
    def __init__(self, depstr_finder, element_class):
        self._depstr_finder = depstr_finder
        self._element_class = element_class
        
    def modify(self, trellis):
        for u in self._depstr_finder.find_dep_str(trellis.get_text()):
            trellis.add_element(
                self._element_class(
                    s = u[0],
                    e = u[1],
                    element_type = ElementType.INSEPARABLE_UNIT,
                    value = None))
