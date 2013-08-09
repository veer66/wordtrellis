from wordtrellis import *


class TestPrunedChoicesGenerator(object):

    def test_gen_0_5_prune_0_2(self):
        trellis = TrellisImpl("".join([u"a" for i in range(10)]))
        element = ElementImpl(s = 0,
                              e = 10,
                              element_type = ElementType.WORD,
                              value = None)
        insep_element = ElementImpl(s = 1,
                                    e = 3,
                                    element_type = ElementType.INSEPARABLE_UNIT)
        trellis.add_element(element)
        trellis.add_element(insep_element)
        boundaries = [element]
        answer = Answer(trellis = trellis, boundaries = boundaries)
        generator = PrunedChoicesGenerator(
            max_len = 3,
            trellis_element_class = ElementImpl,
            insep_map_class = InsepMap)
        choices = generator.get_choices(answer, 0)
        
        assert len(choices) == 2
        assert choices[0].get_s() == 0
        assert choices[0].get_e() == 1
        assert choices[1].get_s() == 0
        assert choices[1].get_e() == 3
