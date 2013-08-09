# -*- coding: UTF-8 -*-

import os
import cPickle as pickle
from wordbreaktst import Tst
from wordbreaktst import TstIter
from transducer import *
from tst_transducer import *
from feeder import *
from trellis import *
from modifier import *
from analyzer import *
from answer import *
from answer_finder import *
from choices_generator import *
from depstr_modifier import *
import depstr
import yaitst

def _get_tst(tst_path):
    f = open(tst_path)
    tst = pickle.load(f)
    f.close()
    return tst
    
def _get_tst_dict_transducer(tst):
    return  TstDictTransducer(
                tst = tst, 
                tst_iter_class = TstIter,
                state_class = TstDictState)
    
def get_wordtrellis_analyzer():
    tst_dict_transducer = _get_tst_dict_transducer(get_tdict_tst())
    simple_word_feeder = SimpleWordFeeder(ElementImpl)
    yai_modifier = TransducerBasedTrellisModifier(transducer = tst_dict_transducer,
                                                 feeder = simple_word_feeder)
    return AnalyzerImpl(modifiers = [yai_modifier], 
                        trellis_class = TrellisImpl)
                        
def get_tdict_tst():
    return _get_tst(yaitst.get_tdict_tst_path())

def get_yaitron_tst():
    return _get_tst(yaitst.get_yaitron_tst_path())

def get_dict_modifier(tst):
    tst = tst if tst != None else get_tdict_tst()
    tst_dict_transducer = _get_tst_dict_transducer(tst)
    simple_word_feeder = SimpleWordFeeder(ElementImpl)
    return  TransducerBasedTrellisModifier(transducer = tst_dict_transducer,
                                                 feeder = simple_word_feeder)

def get_default_analyzer(tst = None):
    return AnalyzerImpl(modifiers = [get_dict_modifier(tst)], 
                        trellis_class = TrellisImpl)
                        
def get_simple_answer_finder(): 
    return SimpleOneAnswerFinder(table_class = SimpleAnswerTable,
                                table_element_class = SimpleAnswerTableElement,
                                answer_class = Answer,
                                trellis_element_class = ElementImpl,
                                insep_map_class = InsepMap)
                                
def get_simple_choices_generator():
    return SimpleChoicesGenerator(max_choices = 29, 
                                  trellis_element_class = ElementImpl)
    
    
def get_simple_answer_updater():
    return SimpleAnswerUpdater(trellis_element_class = ElementImpl, 
                               boundary_class = Boundary,
                               answer_class = Answer)

def get_thai_sep_str_finder():
    dep_str_finder = depstr.DepStrFinder(depstr.read_dep_rules_simple)
    dep_str_finder.load_rules(depstr.get_thai_rules_path())
    return dep_str_finder

def get_thai_sep_str_modifier():
    return DepStrTrellisModifier(
        depstr_finder = get_thai_sep_str_finder(),
        element_class = ElementImpl)

def get_pruned_analyzer(tst = None):
    return AnalyzerImpl(
        modifiers = [get_dict_modifier(tst),
                     get_thai_sep_str_modifier()], 
        trellis_class = TrellisImpl)

def get_pruned_choices_generator():
    return PrunedChoicesGenerator(
            max_len = 29,
            trellis_element_class = ElementImpl,
            insep_map_class = InsepMap)

def get_rerank_pruned_choices_generator(choice_cmp_func = None):
    return RerankPrunedChoicesGenerator(
        max_len = 29, 
        trellis_element_class = ElementImpl,
        insep_map_class = InsepMap,
        word_segment_counter = WordSegmentCounter(),
        choice_cmp_func = default_choice_cmp_func \
            if choice_cmp_func == None \
            else choice_cmp_func)
    
def main():
    analyzer = get_pruned_analyzer()
    
if __name__ == '__main__':
    main()
    
