from typing import List, Dict, Tuple
import subprocess
import FuzzingBook_Generational

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

parsers = []

def create_new(data):
    path = "./grammarGeneration_output/java_generational_urls.txt"
    try:
        with open(path, 'a', encoding="utf-8") as f:
            f.write(data+"\n")
    except Exception as e:
        print(e)

def write_errors(data, path):
    try:
        with open(path, 'a', encoding="utf-8") as f:
            f.write(data+"\n")
    except Exception as e:
        print(e)

def load_urls():
    file = open("./grammarGeneration_output/java_generational_urls.txt", 'r', encoding='utf-8')#, errors='ignore')
    Lines = file.read().splitlines()
    file.close()
    for line in Lines: 
        url_lines.append(line)

def main():
    for i in range(10000):
        url_lines.append(FuzzingBook_Generational.generateInputs(grammar=URL_GRAMMAR, max_nonterminals=10, log=False))
    
    #Writing to file just to have them in a separate text file
    for url in url_lines:
        create_new(url)
    
    load_urls()
    galimatias_execute_fuzz()
    jurl_execute_fuzz()

def galimatias_execute_fuzz(): 
    print('----- Galimatias Java Parser: -----')
    write_errors('----- Galimatias Java Parser : -----', "./grammarGeneration_output/GalimatiasJavaResults.txt")
    for url in url_lines:
        try:
            write_errors("info. Starting process for url: %s" % url, "./grammarGeneration_output/GalimatiasJavaResults.txt")
            result = subprocess.run(['java', '-cp','./fuzzers/galimatias.jar:./fuzzers/icu4j-72.1.jar','io.mola.galimatias.cli.CLI', "\"" + url + "\""],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
            output = get_output(result)
            print(result)
            write_errors(str(result), "./grammarGeneration_output/GalimatiasJavaResults.txt")
            #If the length of the ouput is greater than 0 than the input file has failed
            if len(output) > 0:
                expected = False
                write_errors("info. Error as expected for url: %s" % url, "./grammarGeneration_output/GalimatiasJavaResults.txt")
                # for expected_out in parser[2]:
                #     if expected_out in output:
                #         expected = True
                #         break
                        
                if not expected or result.returncode != 0:
                    print(result)
                    write_errors(str(result), "./grammarGeneration_output/GalimatiasJavaResults.txt")
            else:
                write_errors("info. URL parsed successfully: %s" % url, "./grammarGeneration_output/GalimatiasJavaResults.txt")
        except subprocess.TimeoutExpired:
            print('Timed out', url)
            write_errors('Timed out: %s' % url, "./grammarGeneration_output/GalimatiasJavaResults.txt")
        except ValueError:
                print('Embedded null byte', url)
                write_errors('Embedded null byte: %s' % url, "./grammarGeneration_output/GalimatiasJavaResults.txt")

def jurl_execute_fuzz():
    print('----- Jurl Java Parser: -----')
    write_errors('----- Jurl Java Parser : -----', "./grammarGeneration_output/JurlJavaResults.txt")
    for url in url_lines:
        try:
            write_errors("info. Starting process for url: %s" % url, "./grammarGeneration_output/JurlJavaResults.txt")
            result = subprocess.run(['java', '-cp','.:jurl-v0.4.2.jar','com.example.App', "\"" + url + "\""],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
            output = get_output(result)
            #If the length of the ouput is greater than 0 than the input file has failed
            if len(output) > 0:
                expected = False
                write_errors("info. Error as expected for url: %s" % url, "./grammarGeneration_output/JurlJavaResults.txt")
                # for expected_out in parser[2]:
                #     if expected_out in output:
                #         expected = True
                #         break
                        
                if not expected or result.returncode != 0:
                    print(result)
                    write_errors(str(result), "./grammarGeneration_output/JurlJavaResults.txt")
            else:
                write_errors("info. URL parsed successfully: %s" % url, "./grammarGeneration_output/JurlJavaResults.txt")
        except subprocess.TimeoutExpired:
            print('Timed out', url)
            write_errors('Timed out: %s' % url, "./grammarGeneration_output/JurlJavaResults.txt")
 

def get_output(result):
    output = result.stdout.decode('utf-8')
    return output

if __name__ == "__main__":
    main()