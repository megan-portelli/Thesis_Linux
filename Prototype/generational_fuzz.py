from typing import List, Dict
import os
import random
import subprocess

Grammar = Dict[str, List[Expansion]]

URL_GRAMMAR: Grammar = {
    "<url>":
        ["<scheme>://<authority>/<path>?<query>#<fragment>"],

    "<fragment>":
        ["<word>&<word>&<fragment>", "<word>", " "],

    "<query>":
        ["<word>=<word>&<query>", "<word>=<word>&<query>", " "],
    
    "<path>":
        ["<word>/<word>/<path>", "<word>"],

    "<authority>":
        ["<word><domain>:port", "<word><domain>"],

    "<domain>":
        [".com", ".net", ".org", ".edu", ".gov", ".<alpha><alpha>", ".<alpha><alpha><alpha>"],   

    "<scheme>":
        ["http", "https"], #do I also add word to have any combination of letters? Personally, I dont think its ideal

    "<reserved_characters>":
        [";", "/", "?", ":", "@", "&", "=", "+", "$", "#"],
    
    "<port>":
        ["<digit><digit><digit><digit>"],

    "<integer>":
        ["<digit><integer>", "<digit>"],

    "<word>":
        ["<alpha><word>", "<word"],

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