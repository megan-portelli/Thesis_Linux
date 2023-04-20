from typing import List, Dict, Tuple
import subprocess
import FuzzingBook_Generational
from datetime import datetime

Grammar = Dict[str, List[Tuple]]

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
        ["http", "https"],

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
    ["python3","./parsers/py-furl/main.py", '"%s"', ["Invalid URL"] ],
    ["python3","./parsers/py-url-parser/main.py", '"%s"', ["Invalid URL"] ],
    ["python3","./parsers/py-whatwg-url/main.py", '"%s"', ["Invalid URL"] ],
    ["python3","./parsers/py-urltools/main.py", '"%s"', ["Invalid URL"] ],
    ["python3","./parsers/py-p.url/main.py", '"%s"', ["Invalid URL"] ],
]



def create_new(data):
    path = "./grammarGeneration_output/generational_urls.txt"
    try:
        with open(path, 'a', encoding="utf-8") as f:
            f.write(data+"\n")
    except Exception as e:
        print(e)

def write_errors(data):
    path = "./grammarGeneration_output/PythonResults.txt"
    try:
        with open(path, 'a', encoding="utf-8") as f:
            f.write(data+"\n")
    except Exception as e:
        print(e)

def main():
    for i in range(5):
        url_lines.append(FuzzingBook_Generational.generateInputs(grammar=URL_GRAMMAR, max_nonterminals=10, log=False))
    
    #Writing to file just to have them in a separate text file
    for url in url_lines:
        create_new(url)

    execute_fuzz()

def execute_fuzz(): 
   for parser in parsers:
        print('----- Parser: %s -----' % parser[1])
        write_errors('----- Parser: %s '+  str(datetime.date()) + '-----' % parser[1])
        for url in url_lines:
            param = parser[2] % url
            try:
                print()
                result = subprocess.run([parser[0], parser[1], param], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
                output = get_output(result)
                #If the length of the ouput is greater than 0 than the input file has failed
                if len(output) > 0:
                    expected = False
                    for expected_out in parser[3]:
                        if expected_out in output:
                            expected = True
                            break
                            
                    if not expected or result.returncode != 0:
                        print(result)
                        write_errors(str(result))
            except subprocess.TimeoutExpired:
                print('Timed out', param)
                write_errors('Timed out: %s' % param)

def get_output(result):
    output = result.stderr.decode('utf-8')
    return output

if __name__ == "__main__":
    main()