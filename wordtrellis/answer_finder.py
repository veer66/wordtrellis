from trellis import *
from answer import *
import score

class SimpleAnswerTableElement:
    def __init__(self, 
                 pos, 
                 word_count = 1, 
                 is_unk = False, 
                 link = 0,
                 trellis_element = None, 
                 is_linked = False,
                 is_valid_link = False):
        self._pos = pos
        self._word_count = word_count
        self._is_unk = is_unk
        self._link = link
        self._trellis_element = trellis_element
        self._is_linked = is_linked
        self._unk_char_count = 0
        self._is_valid_link = is_valid_link

    def __str__(self):
        return str(self._trellis_element) + \
            " pos=" + str(self._pos) +  \
            " link=" + str(self._link) + \
            " word_count=" + str(self._word_count) + \
            " is_unk=" + str(self._is_unk) + \
            " unk_char_count=" + str(self._unk_char_count) + \
            " is_linked=" + str(self._is_linked)
        
    def set_trellis_element(self, element):
        self._trellis_element = element
    
    def get_word_count(self):
        return self._word_count
        
    def get_unk_char_count(self):
        return self._unk_char_count
        
    def is_unk(self):
        return self._is_unk

    def get_link(self):
        return self._link
    
    def set_link(self, link):
        self._link = link
        
    def set_unk_char_count(self, count):
        self._unk_char_count = count
        
    def get_trellis_element(self):
        return self._trellis_element

    def get_pos(self):
        return self._pos
        
    def set_valid_link(self, is_valid_link = True):
        self._is_valid_link = is_valid_link
        
    def is_valid_link(self):
        return self._is_valid_link

    def links_it(self, unk_char_count, 
                       word_count, 
                       is_valid_link, 
                       link_pos,
                       trellis_element = None):
        self._is_linked = True
        self._unk_char_count = unk_char_count
        self._word_count = word_count
        self._is_valid_link = is_valid_link
        self._link = link_pos
        self._trellis_element = trellis_element

    def is_higher_score(self, is_valid_link, unk_char_count, word_count):
        return (score.cmp_pairs(
                (not is_valid_link, not self._is_valid_link),
                (unk_char_count, self._unk_char_count),
                (word_count, self._word_count)) <= 0)

    def links_by_unk(self, source, insep_map):
        link_pos = source.get_link() if source.is_unk() else source.get_pos()
        is_valid_link = insep_map.can_link(link_pos, self.get_pos())
        word_count = source.get_word_count() + (0 if source.is_unk() else 1)
        unk_char_count = source.get_unk_char_count() - source.get_pos() + self._pos
        if not self._is_linked or \
                self.is_higher_score(is_valid_link = is_valid_link, 
                                   unk_char_count = unk_char_count, 
                                   word_count = word_count):
            self.links_it(is_valid_link  = is_valid_link, 
                          unk_char_count = unk_char_count, 
                          word_count = word_count, 
                          link_pos = link_pos)
            self._is_unk = True
    
    def links_by_known(self, source, insep_map, trellis_element):
        link_pos = source.get_pos()
        is_valid_link = insep_map.can_link(link_pos, self.get_pos())
        word_count = source.get_word_count() + 1
        unk_char_count = source.get_unk_char_count()
	if not self._is_linked or \
                self.is_higher_score(is_valid_link = is_valid_link, 
                                   unk_char_count = unk_char_count, 
                                   word_count = word_count):
            self.links_it(is_valid_link  = is_valid_link, 
                          unk_char_count = unk_char_count, 
                          word_count = word_count, 
                          link_pos = link_pos,
                          trellis_element = trellis_element)
            self._is_unk = False
        

class SimpleAnswerTable:
    def __init__(self, n, table_element_class):
        self._elements = [table_element_class(i) for i in range(n + 1)]
        self._elements[0].set_valid_link(True)
        
        
    def add_element(self, element):
        self._elements[element.get_pos()] = element
    
    def get_element_at(self, i):
        return self._elements[i]
        
    def get_n(self):
        return len(self._elements)
    
    def __str__(self):
        return "\n".join(["(%d %s)" % i for i in enumerate(self._elements)])
            

class InsepMap:
    def __init__(self, trellis):
        self._l = len(trellis.get_text()) + 1
        self._m = [0 for i in range(self._l)]
        dep_elements = trellis.get_elements(ElementType.INSEPARABLE_UNIT)
        for c, dep_elements in enumerate(dep_elements):
            for i in range(dep_elements.get_s(), dep_elements.get_e()):
                self._m[i] = c + 1
        
    def _is_left_edge(self, p):
        if p == 0:
            return True
        if self._m[p] != self._m[p-1]:
            return True
            
    def _is_right_edge(self, p):
        if p == self._l - 1:
            return True
        if self._m[p] != self._m[p + 1]:
            return True    
            
    def can_link(self, v, w):
        if self._m[v] == self._m[w - 1]:
            if self._m[v] == 0:
                return True
            elif self._is_left_edge(v) and self._is_right_edge(w - 1):
                return True
        else:
            if (self._m[v] == 0 or self._is_left_edge(v)) and \
               (self._is_right_edge(w - 1) or self._m[w - 1] == 0):
                return True
                
        return False
           
        
class SimpleOneAnswerFinder:
    def __init__(self, table_class, table_element_class, 
                answer_class, trellis_element_class, insep_map_class):
        self._table_class = table_class
        self._table_element_class = table_element_class
        self._answer_class = answer_class
        self._trellis_element_class = trellis_element_class
        self._insep_map_class = insep_map_class
        
    def _construct_answer(self, trellis, tab):
        i = tab.get_n() - 1
        boundaries = []
        while i > 0:
            tab_element = tab.get_element_at(i)
            trellis_element = None 
            if tab_element.is_unk():
                trellis_element =  self._trellis_element_class(
                                            tab_element.get_link(),
                                            i,
                                            ElementType.UNCERTAIN_UNIT, None)
            else:
                trellis_element = tab_element.get_trellis_element()
            boundaries.append(Boundary(trellis_element))
            i = tab_element.get_link()
        boundaries.reverse()
        return self._answer_class(trellis = trellis, 
                                  boundaries = boundaries)

    def find_answer(self, trellis):
        insep_map = self._insep_map_class(trellis)
        tab = self._table_class(len(trellis.get_text()), 
                                self._table_element_class)
        for i in range(1, len(trellis.get_text()) + 1):
            tab_element = tab.get_element_at(i)
            trellis_elements = trellis.get_elements_by_e(i)        
            for trellis_element in trellis_elements:
                s = trellis_element.get_s()
                source = tab.get_element_at(s)
                tab_element.links_by_known( 
                    source = source,
                    insep_map = insep_map,
                    trellis_element = trellis_element)
 
            #endif
            max_jump_dist = 3
            for jump_dist in range(max_jump_dist if i >= max_jump_dist else i):
              source = tab.get_element_at(i - jump_dist - 1)
              tab_element.links_by_unk(
                    source = source,
                    insep_map = insep_map) 
        #endfor
        return self._construct_answer(trellis, tab)
