import os
import subprocess
import FuzzingBook_Mutational

url_lines = []

parsers = []

input_folders = [
    "./input/",
]

mutation_folder = [
    "./mutation_output/",
]

def load_urls(folder):
    for path in folder:
        for file in os.listdir(path):
            if file.endswith('.txt'):
                file1 = open(path+file, 'r', encoding='utf-8')#, errors='ignore')
                Lines = file1.read().splitlines()
                file1.close()
                for line in Lines: 
                    url_lines.append(line)


def main():    
    load_urls(input_folders)

    for url in url_lines:
        counter = 0
        while counter < 51:
            mutated_url = FuzzingBook_Mutational.mutate(url)
            create_new(mutated_url)
            counter+=1
    
    load_urls(mutation_folder)
    galimatias_execute_fuzz()
    jurl_execute_fuzz()

def create_new(data):
    path = "./mutation_output/java_mutation_urls.txt"
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

def galimatias_execute_fuzz(): 
    print('----- Galimatias Java Parser: -----')
    write_errors('----- Galimatias Java Parser : -----', "./grammarGeneration_output/GalimatiasJavaResults.txt")
    for url in url_lines:
        try:
            print()
            result = subprocess.run(['java', '-cp','galimatias-0.2.1.jar:icu4j-72.1.jar','io.mola.galimatias.cli.CLI', "\"" + url + "\""],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
            output = get_output(result)
            #If the length of the ouput is greater than 0 than the input file has failed
            if len(output) > 0:
                expected = False
                # for expected_out in parser[2]:
                #     if expected_out in output:
                #         expected = True
                #         break
                        
                if not expected or result.returncode != 0:
                    print(result)
                    write_errors(str(result), "./mutation_output/GalimatiasJavaResults.txt")
        except subprocess.TimeoutExpired:
            print('Timed out', url)
            write_errors('Timed out: %s' % url)

def jurl_execute_fuzz():
    print('----- Jurl Java Parser: -----')
    write_errors('----- Jurl Java Parser : -----', "./grammarGeneration_output/JurlJavaResults.txt")
    for url in url_lines:
        try:
            print()
            result = subprocess.run(['java', '-cp','.:jurl-v0.4.2.jar','com.example.App', "\"" + url + "\""],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
            output = get_output(result)
            #If the length of the ouput is greater than 0 than the input file has failed
            if len(output) > 0:
                expected = False
                # for expected_out in parser[2]:
                #     if expected_out in output:
                #         expected = True
                #         break
                        
                if not expected or result.returncode != 0:
                    print(result)
                    write_errors(str(result), "./mutation_output/JurlJavaResults.txt")
        except subprocess.TimeoutExpired:
            print('Timed out', url)
            write_errors('Timed out: %s' % url)

def get_output(result):
    output = result.stderr.decode('utf-8')
    return output

main()