from trellis import *

class Analyzer:
    def analyze(self, text):
        pass
        
class AnalyzerImpl(Analyzer):
    def __init__(self, modifiers, trellis_class):
        self._trellis_class = trellis_class
        self._modifiers = modifiers

    def analyze(self, text):
        trellis = self._trellis_class(text)
        for modifier in self._modifiers:
            modifier.modify(trellis)
        return trellis
