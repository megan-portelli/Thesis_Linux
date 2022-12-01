import os
import random
import subprocess

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

input_folders = [
    "input/",
]

mutation_folder = [
    "mutation_output/",
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
        while counter < 5:
            mutated_url = mutate(url)
            create_new(mutated_url)
            counter+=1
    
    load_urls(mutation_folder)
    execute_fuzz()

#MUTATION ENGINE
def mutate(data):
    #Returns data with a random bit flipped in a random position
    if data == "":
        return data

    mutators = [
        delete_random_character,
        insert_random_character,
        flip_random_character
    ]

    mutator = random.choice(mutators)

    return mutator(data)

def delete_random_character(data):
    pos = random.randint(0, len(data)-1)
    return data[:pos] + data[pos + 1:]

def insert_random_character(data):
    #Inserting random characters
    pos = random.randint(0, len(data))
    random_character = chr(random.randrange(32,127))
    return data[:pos] + random_character + data[pos:]

def flip_random_character(data): 
    pos = random.randint(0, len(data) - 1)
    c = data[pos]
    bit = 1 << random.randint(0,6)
    new_c = chr(ord(c)^bit)
    return data[:pos] + new_c + data[pos+1:]

#Write new mutated URL to text file
def create_new(data):
    path = "mutation_output/mutation_urls.txt"
    try:
        with open(path, 'a', encoding="utf-8") as f:
            f.write(data+"\n")
    except Exception as e:
        print(e)

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