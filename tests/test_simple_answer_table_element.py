from wordtrellis import SimpleAnswerTableElement

class FakeInSep:
    def can_link(self, v, w):
        return True

class TestSimpleAnswerTableElement(object):
    def setup(self):
        self.fake_insep = FakeInSep()
        
    def test_link_with_unk(self):
        e1 = SimpleAnswerTableElement(1)
        e2 = SimpleAnswerTableElement(2)
        e2.links_by_unk(e1, self.fake_insep)
        assert e2.is_unk()
        
    def test_link_with_not_unk(self):
        e1 = SimpleAnswerTableElement(1)
        e2 = SimpleAnswerTableElement(2)
        e2.links_by_known(e1, self.fake_insep, None)
        assert not e2.is_unk()
        
    def test_link_by_unk_when_source_is_not_unk(self):
        source = SimpleAnswerTableElement(8, is_unk = False)
        element = SimpleAnswerTableElement(16)
        element.links_by_unk(source, self.fake_insep)
        assert element.get_unk_char_count() == 8
        assert element.get_word_count() == 2
        assert element.get_pos() == 16
        assert element.get_link() == 8

    def test_link_by_unk_when_source_is_unk(self):
        source = SimpleAnswerTableElement(8, is_unk = True)
        source.set_link(5)
        source.set_unk_char_count(3)
        element = SimpleAnswerTableElement(16)
        element.links_by_unk(source, self.fake_insep)
        assert element.get_unk_char_count() == 11
        assert element.get_word_count() == 1
        assert element.get_pos() == 16
        assert element.get_link() == 5
