'''PartII.py
Luxun Xu, CSE 415, Spring 2016, University of Washington
Instructor:  S. Tanimoto.
Assignment 2 Part II.  ISA Hierarchy Manipulation

I have worked alone (no partner).

Status of the implementation of new features:
1. direct redundancy detection implemented
2. simple indirect redundancy detection implemented
3. intermediate indirect redundancy detection implemented
4. complex indirect redundancy detection implemented

All forms of redundancy detection and processing are working.
Extra credit not attempted.

'''

# Linneus3.py
# Implements storage and inference on an ISA hierarchy
# This Python program goes with the book "The Elements of Artificial
# Intelligence".
# This version runs under Python 3.x.

# Steven Tanimoto
# (C) 2012.

# The ISA relation is represented using a dictionary, ISA.
# There is a corresponding inverse dictionary, INCLUDES.
# Each entry in the ISA dictionary is of the form
#  ('turtle' : ['reptile', 'shelled-creature'])

from re import *   # Loads the regular expression module.

ISA = {}
INCLUDES = {}
ARTICLES = {}
REDUNDANCY_LIST = []
COUNT = 0

def store_isa_fact(category1, category2):
    'Stores one fact of the form A BIRD IS AN ANIMAL'
    # That is, a member of CATEGORY1 is a member of CATEGORY2
    try :
        c1list = ISA[category1]
        c1list.append(category2)
    except KeyError :
        ISA[category1] = [category2]
    try :
        c2list = INCLUDES[category2]
        c2list.append(category1)
    except KeyError :
        INCLUDES[category2] = [category1]

def get_isa_list(category1):
    'Retrieves any existing list of things that CATEGORY1 is a'
    try:
        c1list = ISA[category1]
        return c1list
    except:
        return []

def get_includes_list(category1):
    'Retrieves any existing list of things that CATEGORY1 includes'
    try:
        c1list = INCLUDES[category1]
        return c1list
    except:
        return []

def isa_test1(category1, category2):
    'Returns True if category 2 is (directly) on the list for category 1.'
    c1list = get_isa_list(category1)
    return c1list.__contains__(category2)

def isa_test(category1, category2, depth_limit = 10):
    'Returns True if category 1 is a subset of category 2 within depth_limit levels'
    if category1 == category2 : return True
    if isa_test1(category1, category2) : return True
    if depth_limit < 2 : return False
    for intermediate_category in get_isa_list(category1):
        if isa_test(intermediate_category, category2, depth_limit - 1):
            return True
    return False

def store_article(noun, article):
    'Saves the article (in lower-case) associated with a noun.'
    ARTICLES[noun] = article.lower()

def get_article(noun):
    'Returns the article associated with the noun, or if none, the empty string.'
    try:
        article = ARTICLES[noun]
        return article
    except KeyError:
        return ''


def idd(category1, category2):
    global COUNT
    for hasItem in get_includes_list(category2):
        if isa_test(hasItem, category1) and hasItem != category1:
            REDUNDANCY_LIST.append(hasItem)
            REDUNDANCY_LIST.append(category2)
            COUNT += 1
            get_isa_list(hasItem).remove(category2)
    for isItem in get_isa_list(category2):
        idd(category2, isItem)
    return COUNT

def linneus():
    'The main loop; it gets and processes user input, until "bye".'
    print('This is Linneus.  Please tell me "ISA" facts and ask questions.')
    print('For example, you could tell me "An ant is an insect."')
    while True :
        info = input('Enter an ISA fact, or "bye" here: ')
        if info == 'bye': return 'Goodbye now!'
        process(info)

# Some regular expressions used to parse the user sentences:
assertion_pattern = compile(r"^(a|an|A|An)\s+([-\w]+)\s+is\s+(a|an)\s+([-\w]+)(\.|\!)*$", IGNORECASE)
query_pattern = compile(r"^is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
what_pattern = compile(r"^What\s+is\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
why_pattern = compile(r"^Why\s+is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)

def process(info) :
    'Handles the user sentence, matching and responding.'
    result_match_object = assertion_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        if isa_test1(items[1], items[3]):
            print("You told me that earlier.")
            return
        if isa_test(items[1], items[3]):
            print("You don't have to tell me that.")
            return
        store_article(items[1], items[0])
        store_article(items[3], items[2])
        store_isa_fact(items[1], items[3])
        number = idd(items[1], items[3])
        if number > 0:
            if number == 1:
                get_includes_list(REDUNDANCY_LIST[1]).remove(REDUNDANCY_LIST[0])
                print("Your earlier statement that " + get_article(REDUNDANCY_LIST[0]) + " " + REDUNDANCY_LIST[0] + " is " + \
                get_article(REDUNDANCY_LIST[1]) + " " + REDUNDANCY_LIST[1] + " is now redundant.")
                return
            else:
                print("The following statements you made earlier are now all redundant:")
                for i in range(0, number):
                    get_includes_list(REDUNDANCY_LIST[i*2+1]).remove(REDUNDANCY_LIST[i*2])
                    if i < number - 1:
                        print(get_article(REDUNDANCY_LIST[i*2]) + " " + REDUNDANCY_LIST[i*2] + " is " +
                              get_article(REDUNDANCY_LIST[i*2+1]) + " " + REDUNDANCY_LIST[i*2+1] + ";")
                    else:
                        print(get_article(REDUNDANCY_LIST[i * 2]) + " " + REDUNDANCY_LIST[i * 2] + " is " +
                              get_article(REDUNDANCY_LIST[i * 2 + 1]) + " " + REDUNDANCY_LIST[i * 2 + 1] + ".")
                return
        print("I understand.")
        return
    result_match_object = query_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        answer = isa_test(items[1], items[3])
        if answer :
            print("Yes, it is.")
        else :
            print("No, as far as I have been informed, it is not.")
        return
    result_match_object = what_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        supersets = get_isa_list(items[1])
        if supersets != [] :
            first = supersets[0]
            a1 = get_article(items[1]).capitalize()
            a2 = get_article(first)
            print(a1 + " " + items[1] + " is " + a2 + " " + first + ".")
            return
        else :
            subsets = get_includes_list(items[1])
            if subsets != [] :
                first = subsets[0]
                a1 = get_article(items[1]).capitalize()
                a2 = get_article(first)
                print(a1 + " " + items[1] + " is something more general than " + a2 + " " + first + ".")
                return
            else :
                print("I don't know.")
        return
    result_match_object = why_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        if not isa_test(items[1], items[3]) :
            print("But that's not true, as far as I know!")
        else:
            answer_why(items[1], items[3])
        return
    print("I do not understand.  You entered: ")
    print(info)

def answer_why(x, y):
    'Handles the answering of a Why question.'
    if x == y:
        print("Because they are identical.")
        return
    if isa_test1(x, y):
        print("Because you told me that.")
        return
    print("Because " + report_chain(x, y))
    return

from functools import reduce
def report_chain(x, y):
    'Returns a phrase that describes a chain of facts.'
    chain = find_chain(x, y)
    all_but_last = chain[0:-1]
    last_link = chain[-1]
    main_phrase = reduce(lambda x, y: x + y, map(report_link, all_but_last))
    last_phrase = "and " + report_link(last_link)
    new_last_phrase = last_phrase[0:-2] + '.'
    return main_phrase + new_last_phrase

def report_link(link):
    'Returns a phrase that describes one fact.'
    x = link[0]
    y = link[1]
    a1 = get_article(x)
    a2 = get_article(y)
    return a1 + " " + x + " is " + a2 + " " + y + ", "

def find_chain(x, z):
    'Returns a list of lists, which each sublist representing a link.'
    if isa_test1(x, z):
        return [[x, z]]
    else:
        for y in get_isa_list(x):
            if isa_test(y, z):
                temp = find_chain(y, z)
                temp.insert(0, [x,y])
                return temp

def test() :
    '''process("OK")
    process("A sockeye is a salmon.")
    process("A salmon is a fish.")
    process("A sockeye is a fish.")
    process("A spade is a spade.")
    process("A sockeye is a salmon.")

    process("A hawk is a bird.")
    process("A hawk is a raptor.")
    process("A raptor is a bird.")

    process("A hawk is a raptor")
    process("A hawk is an animal")
    process("A bird is an animal")
    process("A raptor is a bird")'''

    process("A chinook is an organism.")
    process("A sockeye is a salmon.")
    process("A fish is an animal.")
    process("A sockeye is an organism.")
    process("A chinook is an animal.")
    process("A chinook is a salmon.")
    process("A sockeye is an animal.")
    process("A fish is an organism.")
    process("A salmon is a fish.")

test()
linneus()

