import wordtrellis

from trellis_builder import build_trellis_from_pair_list
from wordtrellis import get_simple_answer_finder

class TestSimpleAnswerFinder:
    def setup(self):
        self._answer_finder = get_simple_answer_finder()
        
    def test_from_bug_0_3_2_4(self):
        trellis = build_trellis_from_pair_list([(0, 3), (2, 4)], 4)
        answer = self._answer_finder.find_answer(trellis)
        boundaries = answer.get_boundaries()
        print "ANSWER", answer
        assert len(boundaries) == 2
        assert boundaries[0].get_element().get_s() == 0
        assert boundaries[0].get_element().get_e() == 3
        assert boundaries[1].get_element().get_s() == 3
        assert boundaries[1].get_element().get_e() == 4
          
        
