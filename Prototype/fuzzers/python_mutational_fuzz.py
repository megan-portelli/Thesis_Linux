import os
import subprocess
import FuzzingBook_Mutational

url_lines = []

parsers = [
    ["python3","./parsers/py-furl/main.py", '"%s"', ["Invalid URL"] ],
    ["python3","./parsers/py-url-parser/main.py", '"%s"', ["Invalid URL"] ],
    ["python3","./parsers/py-whatwg-url/main.py", '"%s"', ["Invalid URL"] ],
    ["python3","./parsers/py-urltools/main.py", '"%s"', ["Invalid URL"] ],
    ["python3","./parsers/py-p.url/main.py", '"%s"', ["Invalid URL"] ],

]

input_folders = [
    "./input/",
]


#ADD LOGS
#COMMENT OUT CREATE NEW METHOD
#FIX @ IN INPUT FILES FROM https://hexed.it/
mutation_folder = [
    "./mutation_output/",
]

def load_urls(folder):
    for path in folder:
    #     for file in os.listdir(path):
    #         if file.endswith('.txt'):
        file = open(path+"python_mutation_urls2.txt", 'r', encoding='utf-8')#, errors='ignore')
        Lines = file.read().splitlines()
        file.close()
        for line in Lines: 
            url_lines.append(line)

def load_urls_input(folder):
    for path in folder:
        for file in os.listdir(path):
            if file.endswith('.txt'):
                file = open(path+"urls.txt", 'r', encoding='utf-8')#, errors='ignore')
                Lines = file.read().splitlines()
                file.close()
                for line in Lines: 
                    url_lines.append(line)

def main():    
    # load_urls_input(input_folders)

    # for url in url_lines:
    #     counter = 0
    #     while counter < 51:
    #         mutated_url = FuzzingBook_Mutational.mutate(url)
    #         create_new(mutated_url)
    #         counter+=1
    
    load_urls(mutation_folder)
    execute_fuzz()

def create_new(data):
    path = "./mutation_output/python_mutation_urls2.txt"
    try:
        with open(path, 'a', encoding="utf-8") as f:
            f.write(data+"\n")
    except Exception as e:
        print(e)

def write_errors(data):
    path = "./mutation_output/PythonResults2.txt"
    try:
        with open(path, 'a', encoding="utf-8") as f:
            f.write(data+"\n")
    except Exception as e:
        print(e)

def execute_fuzz(): 
   for parser in parsers:
        print('----- Parser: %s -----' % parser[1])
        write_errors('----- Parser: %s -----' % parser[1])
        for url in url_lines:
            param = parser[2] % url
            try:
                write_errors("info.Starting process for url: %s" % param)
                result = subprocess.run([parser[0], parser[1], param], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
                output = get_output(result)
                #If the length of the ouput is greater than 0 than the input file has failed
                if len(output) > 0:
                    expected = False
                    for expected_out in parser[3]:
                        if expected_out in output:
                            expected = True
                            write_errors("info.URL %s parsed with expected error" % param)
                            break
                            
                    if not expected or result.returncode != 0:
                        print(result)
                        write_errors(str(result))
                else:
                    write_errors("info.URL %s parsed successfully with no errors" % param)
            except subprocess.TimeoutExpired:
                print('Timed out', param)
                write_errors('Timed out: %s' % param)
            except ValueError:
                write_errors('Embedded null byte: %s' % param)
                break


def get_output(result):
    output = result.stderr.decode('utf-8')
    return output

if __name__ == "__main__":
    main()