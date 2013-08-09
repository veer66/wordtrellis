from trellis import *

class ChoicesGenerator:
    def __init__(self):
        pass
        
    def get_choices(self, answer, s):
        pass
        
class SimpleChoicesGenerator(ChoicesGenerator):
    def __init__(self, max_choices, trellis_element_class):
        self._max_choices = max_choices  
        self._trellis_element_class = trellis_element_class
        
    def get_choices(self, answer, s):
        e = None
        if self._max_choices + s < len(answer.get_trellis().get_text()):
            e = self._max_choices + s
        else:
            e = len(answer.get_trellis().get_text())
        choices = []
        for i in range(s + 1, e + 1):
            element =  \
                self._trellis_element_class(
                    s = s, 
                    e = i, 
                    element_type = ElementType.UNCERTAIN_UNIT,
                    value = None)
            choices.append(element)
        return choices
        
class PrunedChoicesGenerator(ChoicesGenerator):
    def __init__(self, max_len, 
                       trellis_element_class,
                       insep_map_class):
        self._max_len = max_len 
        self._trellis_element_class = trellis_element_class
        self._insep_map_class = insep_map_class
        
    def get_choices(self, answer, s):
        insep_map = self._insep_map_class(answer.get_trellis())
        e = None
        if self._max_len + s < len(answer.get_trellis().get_text()):
            e = self._max_len + s
        else:
            e = len(answer.get_trellis().get_text())
        choices = []
        for i in range(s + 1, e + 1):
            if insep_map.can_link(s, i):
                element = \
                    self._trellis_element_class(
                        s = s, 
                        e = i, 
                        element_type = ElementType.UNCERTAIN_UNIT,
                        value = None)
                choices.append(element)
        return choices
            
            
class WordSegmentCounterMap:
    def __init__(self, s, e):
        self._m = [dict(valid = False, score = 0, link = -1) 
                    for i in range(e - s + 1)]
        self._m[0]['valid'] = True
        self._s = s
        self._e = e

    def __getitem__(self, i):
        if i > self._e or i < self._s:
            raise RuntimeError, "Index out of range"
        return self._m[i - self._s]
    
    def __str__(self):
        return "s=%s e=%s m=%s" % (self._s, self._e, str(self._m))


class WordSegmentCounter:
    def __init__(self):
        pass        
    
    def count(self, trellis, s, e):
        m = WordSegmentCounterMap(s, e)
        for i in range(s + 1, e + 1):
            for trellis_element in trellis.get_elements_by_e(i, ElementType.WORD): 
                source = trellis_element.get_s()
                if source >= s and m[source]['valid'] and \
                        (m[i]['link'] == -1 or  \
                            m[source]['score'] + 1 < m[i]['score']):
                    m[i]['link'] = source
                    m[i]['valid'] = True
                    m[i]['score'] = m[source]['score'] + 1
                #endif
            #endfor
        #endfor
        
        
        if m[e]['valid']:
            return -m[e]['score']
        else:
            return 0
     
def default_choice_cmp_func(a, b):
    r = cmp(a[1], b[1])
    if r != 0:
        return r
    len_a = a[0].get_e() - a[0].get_s()
    len_b = b[0].get_e() - a[0].get_s()
    return cmp(len_a, len_b)

class RerankPrunedChoicesGenerator(ChoicesGenerator):
    def __init__(self, max_len, 
                       trellis_element_class,
                       insep_map_class,
                       word_segment_counter,
                       choice_cmp_func):
        
        self._max_len = max_len 
        self._trellis_element_class = trellis_element_class
        self._insep_map_class = insep_map_class
        self._word_segment_counter = word_segment_counter
        self._choice_cmp_func = choice_cmp_func
        
    
    def _count_word_seg(self, trellis, element):
        return \
            self._word_segment_counter.count(
                trellis = trellis,
                s = element.get_s(),
                e = element.get_e())
    
    
    def get_choices(self, answer, s):
        insep_map = self._insep_map_class(answer.get_trellis())
        e = None
        if self._max_len + s < len(answer.get_trellis().get_text()):
            e = self._max_len + s
        else:
            e = len(answer.get_trellis().get_text())
        choices = []
        for i in range(s + 1, e + 1):
            if insep_map.can_link(s, i):
                element = \
                    self._trellis_element_class(
                        s = s, 
                        e = i, 
                        element_type = ElementType.UNCERTAIN_UNIT,
                        value = None)
                choices.append(
                    (element, 
                     self._count_word_seg(
                        answer.get_trellis(), element)))
        choices.sort(self._choice_cmp_func)
        
        return map(lambda a: a[0], choices)
        
