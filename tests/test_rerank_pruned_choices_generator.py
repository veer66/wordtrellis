from wordtrellis import *
from text_generator import generate_unicode_text

class FakeWordSegmentCounter:
    def __init__(self):
        pass

    def count(self, trellis, s, e):
        if s == 2 and e == 4:
            return -1
        elif s == 2 and e == 6:
            return -2
        else:
            return 0

class FakeInsepMap:
    def __init__(self, trellis):
        pass
   
    def can_link(self, v, w):
        return True

class TestRerankPrunedChoicesGenerator:
    def test_with_fake_counter(self):
        fake_word_segment_counter = FakeWordSegmentCounter()
        generator = RerankPrunedChoicesGenerator(max_len = 4, 
                       trellis_element_class = ElementImpl,
                       insep_map_class = FakeInsepMap,
                       word_segment_counter = FakeWordSegmentCounter(),
                       choice_cmp_func = default_choice_cmp_func)
        trellis = TrellisImpl(generate_unicode_text(txt_len = 10))
        answer = Answer(trellis = trellis,
                        boundaries = [])
        choices = generator.get_choices(answer, 2)
        assert len(choices) == 4
        assert choices[0].get_e() == 6
        assert choices[1].get_e() == 4
        assert choices[2].get_e() == 3
        assert choices[3].get_e() == 5
    
    def test_with_real_count(self):
        counter = WordSegmentCounter()
        generator = RerankPrunedChoicesGenerator(max_len = 4,
                        trellis_element_class = ElementImpl,
                        insep_map_class = FakeInsepMap,
                        word_segment_counter = counter,
                        choice_cmp_func = default_choice_cmp_func)
        trellis = TrellisImpl(generate_unicode_text(txt_len = 10))
        trellis.add_element(
            ElementImpl(s = 2, 
                        e = 4, 
                        element_type = ElementType.WORD,
                        value = None))
        trellis.add_element(
            ElementImpl(s = 4, 
                        e = 6, 
                        element_type = ElementType.WORD,
                        value = None))
        
        answer = Answer(trellis = trellis,
                        boundaries = [])
        choices = generator.get_choices(answer, 2)
        assert len(choices) == 4
        assert choices[0].get_e() == 6
        assert choices[1].get_e() == 4
        assert choices[2].get_e() == 3
        assert choices[3].get_e() == 5
        
    
    def test_get_from_factory(self):
        generator = get_rerank_pruned_choices_generator()
        
