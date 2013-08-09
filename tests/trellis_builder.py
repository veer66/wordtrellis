from wordtrellis import TrellisImpl
from wordtrellis import ElementImpl
from wordtrellis import ElementType

def build_trellis_from_pair_list(pair_list, l):
    trellis = TrellisImpl("".join([u"a" for i in range(l)]))
    for pair in pair_list:
        trellis.add_element(ElementImpl(s = pair[0],
                                        e = pair[1],
                                        element_type = ElementType.WORD,
                                        value = None))
    return trellis
