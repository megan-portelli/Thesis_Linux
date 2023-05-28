#This class contains any methods used in the Generational Fuzzer, which were taken from the Fuzzing Book.
#The applicable links may be found below.

#Andreas Zeller, Rahul Gopinath, Marcel Böhme, Gordon Fraser, and Christian Holler: "Fuzzing with Grammars". 
# In Andreas Zeller, Rahul Gopinath, Marcel Böhme, Gordon Fraser, and Christian Holler, "The Fuzzing Book", 
# https://www.fuzzingbook.org/html/Grammars.html.

import re
import random

RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')
START_SYMBOL = "<start>"


def nonterminals(expansion):
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return RE_NONTERMINAL.findall(expansion)

def generateInputs(grammar, start_symbol = START_SYMBOL, max_nonterminals = 10, max_expansion_trials=100, log=False):
    term = start_symbol
    expansionTrials = 0

    while len(nonterminals(term)) > 0:
        symbolToExpand = random.choice(nonterminals(term))
        expansions = grammar[symbolToExpand]
        expansion = random.choice(expansions)
        newTerm = term.replace(symbolToExpand, expansion, 1)

        if len(nonterminals(newTerm)) < max_nonterminals:
            term = newTerm
            if log:
                print("%-40s" % (symbolToExpand + " -> " +expansion), term)
            expansionTrials = 0
        else:
            expansionTrials += 1
            if expansionTrials >= max_expansion_trials:
                print("Cannot expand "+repr(term))
    
    return term
   