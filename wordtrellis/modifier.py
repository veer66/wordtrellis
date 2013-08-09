class TrellisModifier:
    def modify(self, trellis):
        pass
        
class TransducerBasedTrellisModifier(TrellisModifier):
    def __init__(self, transducer, feeder):
        self._transducer = transducer
        self._feeder = feeder
        
    def modify(self, trellis):
        transducer_status = []
        for p, ch in enumerate(trellis.get_text()):
            transducer_status.append(self._transducer.get_start_state(p))
            temp_transducer_status = []
            for state in transducer_status:
                if state.apply(ch):
                    temp_transducer_status.append(state)
                    if state.is_break():
                        self._feeder.feed(trellis, state.get_s(), p + 1, 
                                          state.get_value())
            transducer_status = temp_transducer_status
            
