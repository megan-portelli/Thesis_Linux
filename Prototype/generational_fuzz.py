from typing import List, Dict, Tuple
import os
import random
import subprocess
import re

Grammar = Dict[str, List[Tuple]]

START_SYMBOL = "<start>"
RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')

URL_GRAMMAR: Grammar = {
    "<start>":
        ["<url>"], 

    "<url>":
        ["<scheme>://<authority>/<path>" ,"<scheme>://<authority>/<path>?<query>#<fragment>"],

    "<fragment>":
        ["<word>&<word>&<fragment>", "<word>", " "],

    "<query>":
        ["<word>=<word>&<query>", "<word>=<word>&<query>", " "],
    
    "<path>":
        ["<word>/<word>/<path>", "<word>"],

    "<authority>":
        ["<word><domain>:<port>", "<word><domain>"],

    "<domain>":
        [".com", ".net", ".org", ".edu", ".gov", ".<alpha><alpha>", ".<alpha><alpha><alpha>"],   

    "<scheme>":
        ["http", "https"], #do I also add word to have any combination of letters? Personally, I dont think its ideal

    "<reserved_characters>":
        [";", "/", "?", ":", "@", "&", "=", "+", "$", "#"],
    
    "<port>":
        ["<digit><digit>", "<digit><digit><digit>" ,"<digit><digit><digit><digit>",  "<digit><digit><digit><digit><digit>"],

    "<integer>":
        ["<digit><integer>", "<digit>"],

    "<word>":
        ["<alpha>", "<alpha><alpha>", "<alpha><alpha><alpha>", "<alpha><alpha><alpha><alpha>", "<alpha><alpha><alpha><alpha><alpha>",
        "<alpha><alpha><alpha><alpha><alpha><alpha>", "<alpha><alpha><alpha><alpha><alpha><alpha><alpha>", 
        "<alpha><alpha><alpha><alpha><alpha><alpha><alpha><alpha>"],

    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    
    "<alpha>":
        ["a", "b", "c", "d", "e", "f", "g", "h" , 
        "i", "j", "k", "l", "m", "n", "o", "p", "q", 
        "r", "s", "t", "u", "v", "w", "x", "y", "z"]
}

url_lines = []

parsers = [
    ["parsers/c-url-parser/main", "%s", ["Invalid URL"] ],
    ["parsers/liburl/main", "%s", ["Invalid URL"] ],
    ["parsers/liburl_V2015/main", "%s", ["Invalid URL"] ],
    ["parsers/url-parser-c/main", "%s", ["Invalid URL"] ],
    ["parsers/url.h/main", "%s", ["Invalid URL"] ],
    ["parsers/url.h_V2013/main", "%s", ["Invalid URL"] ],
    ["parsers/yuarel/main", "%s", ["Invalid URL"] ],
    ["parsers/yuarel_V2016/main", "%s", ["Invalid URL"] ]
]

#https://www.fuzzingbook.org/html/Grammars.html

def nonterminals(expansion):
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return RE_NONTERMINAL.findall(expansion)

def generateInputs(grammar, start_symbol = START_SYMBOL, max_nonterminals = 10, max_expansion_trials=50, log=False):
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

def create_new(data):
    path = "grammarGeneration_output/generational_urls.txt"
    try:
        with open(path, 'a', encoding="utf-8") as f:
            f.write(data+"\n")
    except Exception as e:
        print(e)


def main():
    for i in range(5):
        url_lines.append(generateInputs(grammar=URL_GRAMMAR, max_nonterminals=5))

    execute_fuzz()

def execute_fuzz(): 
   for parser in parsers:
        print('----- Parser: %s -----' % parser[0])
        for url in url_lines:
            param = parser[1] % url
            try:
                print()
                result = subprocess.run([parser[0], param], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
                output = get_output(result)
                #If the length of the ouput is greater than 0 than the input file has failed
                if len(output) > 0:
                    expected = False
                    for expected_out in parser[2]:
                        if expected_out in output:
                            expected = True
                            break
                            
                    if not expected or result.returncode != 0:
                        print(result)
            except subprocess.TimeoutExpired:
                print('Timed out', param)

def get_output(result):
    output = result.stderr.decode('utf-8')
    return output

main()
