#This class contains any methods used in the Mutational Fuzzer, which were taken from the Fuzzing Book.
#The applicable links may be found below.

#Andreas Zeller, Rahul Gopinath, Marcel Böhme, Gordon Fraser, and Christian Holler: "Mutation-Based Fuzzing". 
# In Andreas Zeller, Rahul Gopinath, Marcel Böhme, Gordon Fraser, and Christian Holler, "The Fuzzing Book", 
# https://www.fuzzingbook.org/html/MutationFuzzer.html.

import random

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
