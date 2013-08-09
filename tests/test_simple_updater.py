from wordtrellis import *
class TestSimpleUpdater(object):
    def setup(self):
        txt = u"abcabcabc"
        trellis = TrellisImpl(txt)
        elements = [ElementImpl(s = 0, e = 3, element_type = ElementType.WORD, value = None),
                    ElementImpl(s = 3, e = 6, element_type = ElementType.WORD, value = None),
                    ElementImpl(s = 6, e = 9, element_type = ElementType.WORD, value = None)]
        trellis.add_element(elements[0])
        trellis.add_element(elements[1])
        trellis.add_element(elements[2])
        boundaries = [Boundary(elements[0]), Boundary(elements[1]), Boundary(elements[2])]
        self.ans = Answer(boundaries = boundaries,
                          trellis = trellis)
                          
        self.updater = get_simple_answer_updater()
        
    def test_3_7_update(self):
        new_ans = self.updater.select(self.ans, 3, 7)
        boundaries = new_ans.get_boundaries()
        
        assert len(boundaries) == 3
        assert boundaries[0].get_element().get_s() == 0
        assert boundaries[0].get_element().get_e() == 3
        assert boundaries[1].get_element().get_s() == 3
        assert boundaries[1].get_element().get_e() == 7
        assert boundaries[2].get_element().get_s() == 7
        assert boundaries[2].get_element().get_e() == 9
        
    def test_3_9_update(self):
        new_ans = self.updater.select(self.ans, 3, 9)
        boundaries = new_ans.get_boundaries()
        print "BOUND", "|".join([str(b.get_element()) for b in boundaries])
        assert len(boundaries) == 2
        assert boundaries[0].get_element().get_s() == 0
        assert boundaries[0].get_element().get_e() == 3
        assert boundaries[1].get_element().get_s() == 3
        assert boundaries[1].get_element().get_e() == 9
    
    def test_1_2_update(self):
        new_ans = self.updater.select(self.ans, 1, 2)
        boundaries = new_ans.get_boundaries()
        print "BOUND", "|".join([str(b.get_element()) for b in boundaries])
        assert len(boundaries) == 4
        assert boundaries[0].get_element().get_s() == 1
        assert boundaries[0].get_element().get_e() == 2
        assert boundaries[1].get_element().get_s() == 2
        assert boundaries[1].get_element().get_e() == 3
        assert boundaries[2].get_element().get_s() == 3
        assert boundaries[2].get_element().get_e() == 6
        assert boundaries[3].get_element().get_s() == 6
        assert boundaries[3].get_element().get_e() == 9
    
    def test_1_2_0_3_3_6_update(self):
        new_ans = self.updater.select(self.ans, 1, 2)
        new_ans = self.updater.select(self.ans, 0, 3)
        new_ans = self.updater.select(self.ans, 3, 6)
        boundaries = new_ans.get_boundaries()
        print "BOUND", "|".join([str(b.get_element()) for b in boundaries])
        assert len(boundaries) == 3
        assert boundaries[0].get_element().get_s() == 0
        assert boundaries[0].get_element().get_e() == 3
        assert boundaries[1].get_element().get_s() == 3
        assert boundaries[1].get_element().get_e() == 6
        assert boundaries[2].get_element().get_s() == 6
        assert boundaries[2].get_element().get_e() == 9

         
