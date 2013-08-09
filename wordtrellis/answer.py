from trellis import ElementType
from copy import copy


class Answer:
    def __init__(self, trellis, boundaries):
        self._trellis = trellis
        self._boundaries = boundaries
        
    def __str__(self):
        return " ".join(str(b) for b in self._boundaries)
        
    def get_boundaries(self):
        return self._boundaries
    
    def get_trellis(self):
        return self._trellis
        
class AnswerUpdate:
    def select(self, answer, s, e):
        pass
        
class SimpleAnswerUpdater(AnswerUpdate):
    def __init__(self, trellis_element_class, boundary_class, answer_class):
        self._trellis_element_class = trellis_element_class
        self._boundary_class = boundary_class
        self._answer_class = answer_class
        
    def _index_boundaries(self, boundaries):
        self._s_idx = {}
        self._e_idx = {}
        self._se_idx = {}
        for i, boundary in enumerate(boundaries):
            s = boundary.get_element().get_s()
            e = boundary.get_element().get_e()
            self._s_idx.setdefault(s, {})[boundary] = i
            self._e_idx.setdefault(e, {})[boundary] = i
            self._se_idx["%d,%d" % (s, e)] = (boundary, i)
        
    def _get_element_type(self, answer, s, e):
        assoc_elements = answer.get_trellis().get_elements_by_se(s, e)
        if assoc_elements != None and len(assoc_elements) > 0:
            return assoc_elements[0].get_type()
        return ElementType.UNCERTAIN_UNIT
        
    def select(self, answer, s, e):
        self._index_boundaries(answer.get_boundaries())
        if self._se_idx.has_key("%d,%d" % (s, e)):
            self._se_idx["%d,%d" % (s, e)][0].set_human_decided()
            return answer
        else:
            return self._answer_class(trellis = answer.get_trellis(),
                boundaries = self._complex_select(answer, s, e))
            
            
    def _add_head(self, answer, s, e, new_ans):
        for i, b in enumerate(answer.get_boundaries()):
            if b.get_element().get_e() <= s:
                new_ans.append(b)
            else:
                break
        return i
    
    def _add_new_boundary(self, answer, s, e, new_ans):
        element = self._trellis_element_class(
                        s = s,
                        e = e,
                        element_type = self._get_element_type(answer, s, e),
                        value = None) 
        boundary = self._boundary_class(element)
        new_ans.append(boundary)
    
    def _find_tail_pos(self, answer, s, e, insert_pos):
        k = None        
        for j in range(insert_pos, len(answer.get_boundaries())):
            if e <= answer.get_boundaries()[j].get_element().get_e():
                k = j + 1
                break
        if k >= len(answer.get_boundaries()):
            return None
        else:
            return k
        
    def _add_tail(self, answer, s, e, new_ans, tail_pos):
        if tail_pos != None:            
            if e != answer.get_boundaries()[tail_pos].get_element().get_s():
                new_s = e
                new_e = answer.get_boundaries()[tail_pos].get_element().get_s()
                self._add_new_boundary(answer, new_s, new_e, new_ans)
            for i in range(tail_pos, len(answer.get_boundaries())):
                new_ans.append(answer.get_boundaries()[i])
        else:
            if e < len(answer.get_trellis().get_text()):
                new_s = e
                new_e = len(answer.get_trellis().get_text())
                self._add_new_boundary(answer, new_s, new_e, new_ans)
            
                
    def _complex_select(self, answer, s, e):
        new_ans = []
        insert_pos = self._add_head(answer, s, e, new_ans)
        self._add_new_boundary(answer, s, e, new_ans)
        tail_pos = self._find_tail_pos(answer, s, e, insert_pos)
        self._add_tail(answer, s, e, new_ans, tail_pos)
        return new_ans
            

                
class Boundary:
    def __init__(self, element, attrs = None):
        self._element = element
        self._attrs = attrs
        self._human_decided = False
                
    def set_human_decided(self, val = True):
        self._human_decided = val
        
    def set_attrs(self, attrs):
        self._attrs = attrs
        
    def get_attrs(self):
        return self._attrs
        
    def get_element(self):
        return self._element
        
    def __str__(self):
        return str(self._element)
