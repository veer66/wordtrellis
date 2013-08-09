# -*- coding: UTF-8 -*-
import re
import os 
   
def _readlines(path):
    f = open(path)
    lines = f.readlines()
    f.close()
    return lines

def read_dep_rules_simple(path):
    symtab = {}
    deplist = []
    lines = _readlines(path)
    for line in lines:
        if re.match("^\*", line):
            deplist.append(filter(lambda tok: tok != "", re.split("[\*\s]+", line)))
        elif re.match("^\s*$", line):
            pass
        else:
            m = re.match("(\w+)\:\s*(.+)\s*$", line)
            if not m:
                raise RuntimeError, "invalid rules"
            symtab[m.group(1)] = unicode(m.group(2), "UTF-8")
    return (symtab, deplist)

class DepStrFinder:
    def __init__(self, read_dep_rules_func):
        self._read_dep_rules_func = read_dep_rules_func

    def load_rules(self, path):
        self._symtab, self.deplist = self._read_dep_rules_func(path)
        self._build_re()

    def _build_re(self):
        def val_list(syms):
            return map(lambda sym: self._symtab[sym], syms)
        
        def join_val_list(val_list):
            return u"".join(val_list)
            
        split_pats = map(lambda syms: u"(%s)" % join_val_list(val_list(syms)), self.deplist)
        match_pats = map(lambda syms: u"^%s$" % join_val_list(val_list(syms)), self.deplist)
        self._pats = zip(split_pats, match_pats)

    def _find_unit(self, txt, pat, units):
        s = None
        e = None
      
        for tok in filter(lambda tok: tok != "", re.split(pat[0], txt)):
            if s == None:
                s = 0
            else:
                s = e
            e = s + len(tok)
            if re.match(pat[1], tok):
                units.append((s,e))
    
    def _check_merge(self, u1, u2):
        if u1[0] <= u2[0] and u1[1] > u2[0]:
            return True
        if u2[0] <= u1[0] and u2[1] > u1[0]:
            return True
        return False 
    
    def _merge(self, v, w):
        return (v[0] if v[0] < w[0] else w[0], 
                v[1] if v[1] > w[1] else w[1])
      
    def _uniq(self, units):
        h = {}
        for u in units:
            h["%d,%d" % (u[0], u[1])] = u
        return h.values()
                
    def _merge_units(self, units):
        merge = True
        for i in range(len(units)):            
            for j in range(len(units)):
                if i != j and units[j] != None and units[i] != None:                    
                    if self._check_merge(units[i], units[j]):
                        units[j] = self._merge(units[i], units[j])
        return self._uniq(filter(lambda u: u != None, units))
        
    def find_dep_str(self, txt):
        units = []
        for pat in self._pats:
            self._find_unit(txt, pat, units)
        return self._merge_units(units)
        
def get_thai_rules_path():
    return os.path.join(
        os.path.dirname(__file__), "rules", 
            "thai_dep_rules.txt")  

if __name__ == "__main__":
    dep_str_finder = DepStrFinder(read_dep_rules_simple)
    dep_str_finder.load_rules("rules/thai_dep_rules.txt")
    dep_str_finder.find_dep_str(u"ไอ้สัดมึงว่าไหงนะค้ำขี่หมี")
