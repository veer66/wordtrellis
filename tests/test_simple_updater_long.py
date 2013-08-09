from wordtrellis import *
class TestSimpleUpdaterLong(object):
    def setup(self):
        e = 13
        txt = "".join([u"a" for i in range(13)])
        trellis = TrellisImpl(txt)
        cuts = [(0, 3), (3, 6), (6, 10), (10, 11), (11, 13)]
        elements = [ElementImpl(s = cut[0], 
                                e = cut[1], 
                                element_type = ElementType.WORD, 
                                value = None) for cut in cuts]
        for element in elements:
            trellis.add_element(element)

        boundaries = [Boundary(element) for element in elements]

        self.ans = Answer(boundaries = boundaries,
                          trellis = trellis)

        self.updater = get_simple_answer_updater()

    def test_0_10_update(self):
        new_ans = self.updater.select(self.ans, 0, 10)
        print [(b.get_element().get_s(), b.get_element().get_e()) for b in new_ans.get_boundaries()]
        assert len(new_ans.get_boundaries()) == 3
        assert new_ans.get_boundaries()[0].get_element().get_s() == 0
        assert new_ans.get_boundaries()[0].get_element().get_e() == 10
        assert new_ans.get_boundaries()[1].get_element().get_s() == 10
        assert new_ans.get_boundaries()[1].get_element().get_e() == 11
        assert new_ans.get_boundaries()[2].get_element().get_s() == 11
        assert new_ans.get_boundaries()[2].get_element().get_e() == 13
