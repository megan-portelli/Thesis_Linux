import subprocess
import os

url_lines = []
parsers = [
    [ "/home/student/Documents/Fuzzing/1st_Prototype/fuzzing/parsers/c-url-parser/main", "%s", ["Invalid URL"] ],
    [ "/home/student/Documents/Fuzzing/1st_Prototype/fuzzing/parsers/liburl/main", "%s", ["Invalid URL"] ],
    [ "/home/student/Documents/Fuzzing/1st_Prototype/fuzzing/parsers/liburl_V2015/main", "%s", ["Invalid URL"] ],
    [ "/home/student/Documents/Fuzzing/1st_Prototype/fuzzing/parsers/url-parser-c/main", "%s", ["Invalid URL"] ],
    [ "/home/student/Documents/Fuzzing/1st_Prototype/fuzzing/parsers/url.h/main", "%s", ["Invalid URL"] ],
    [ "/home/student/Documents/Fuzzing/1st_Prototype/fuzzing/parsers/url.h_V2013/main", "%s", ["Invalid URL"] ],
    [ "/home/student/Documents/Fuzzing/1st_Prototype/fuzzing/parsers/yuarel/main", "%s", ["Invalid URL"] ],
    [ "/home/student/Documents/Fuzzing/1st_Prototype/fuzzing/parsers/yuarel_V2016/main", "%s", ["Invalid URL"] ],

]

input_folders = [
    "input/",
]

#defining function load_urls
''' This function uses a for in loop which performs exactly like a for each loop.
    Going through all the paths in the input_folders array and therefore going through
    each file for each path, it will check that the file ends with extension .json
    (this continues to emphasise what fuzzing is all about) so the program could load 
    it and feed it to the fuzzer in the main function'''
def load_urls():
    for path in input_folders:
        for file in os.listdir(path):
            if file.endswith('.txt'):
                url_lines.append(os.path.join(path, file))
    
    url_lines.sort()

''' This function will simply take the result from the fuzzer and decode it into utf-8
    which is then made available in the console'''
def get_output(result):
    output = result.stderr.decode('utf-8')
    #if len(output) == 0:
        #output = result.stdout.decode('utf-8')
    return output

if __name__ == "__main__":
    load_urls()
    for parser in parsers:
        print('----- Parser: %s -----' % parser[0])
        for url in url_lines:
            param = parser[1] % url
            try:
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

