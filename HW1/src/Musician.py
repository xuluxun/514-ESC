# CSE 415 Luxun Xu
# Assignment 1

from re import *
import random


def introduce():
    return """Hi I am a musician! Music is my life!
    I was programmed by Luxun Xu. If you do not understand
    what I am talking, contact him at luxunx@uw.edu
    Now Let's talk!"""


def agentName():
    return "Musician"


def respond(the_input):
    wordlist = split(' ', remove_punctuation(the_input))
    wordlist[0] = wordlist[0].lower()
    # Rule 1 Respond to nothing
    if wordlist[0] == '':
        return 'Hello? I am listening.'
    # Rule 2 Respond to "am"; memory feature included
    for word in wordlist:
        if word in am_list:
            ind_am = wordlist.index(word)
            if wordlist[ind_am + 1:] != '':
                if wordlist[ind_am + 1] in article_list and wordlist[ind_am + 2:] != '':
                    if wordlist[ind_am + 2] in property_list:
                        return 'I know you are ' + stringify(wordlist[ind_am + 1:ind_am + 3]) + \
                               ' and I already wrote a song for you using ' + property_instrument[wordlist[ind_am + 2]] + '.'
                    else:
                        property_list.append(wordlist[ind_am + 2])
                        property_instrument[wordlist[ind_am + 2]] = random.choice(instrument_list)
                        return 'Nice, now I know you are ' + stringify(wordlist[ind_am + 1:ind_am + 3]) + \
                               ' and I can write a song for you using ' + property_instrument[wordlist[ind_am + 2]] + "."
                else:
                    if wordlist[ind_am + 1] in property_list:
                        return 'I know you are ' + wordlist[ind_am + 1] + ' and I already wrote a song for you using ' + \
                               property_instrument[wordlist[ind_am + 1]] + '.'
                    else:
                        property_list.append(wordlist[ind_am + 1])
                        property_instrument[wordlist[ind_am + 1]] = random.choice(instrument_list)
                        return 'Nice, now I know you are ' + wordlist[ind_am + 1] + \
                               ' and I can write a song for you using ' + property_instrument[wordlist[ind_am + 1]] + '.'
    # Rule 3 Respond to preference; cycle feature included
    for word in wordlist:
        if word in preference_word:
            like = wordlist.index(word)
            if wordlist[like + 1] != '':
                if not wordlist[like + 1] in opp_preference_list:
                    opp_preference_list.append(wordlist[like + 1])
                    return "I like " + wordlist[like + 1] + " too!"
                else:
                    return "I know you like " + wordlist[like + 1] + " already. " + do_it_again()
    # Rule 4 Respond to "have"; cycle feature included
    if 'have' in wordlist:
        ind_have = wordlist.index('have')
        if wordlist[ind_have + 1] != 'to' and wordlist[ind_have + 1] != '':
            if not wordlist[ind_have + 1] in have_list:
                have_list.append(wordlist[ind_have + 1])
                return "I do not have that, but I have music!"
            else:
                return "I know you have that already. " + do_it_again()
    # Rule 5 Respond to "when"
    if wordlist[0] == 'when':
        return "Music is good for any time, any day."
    # Rule 6 Respond to "who"
    if wordlist[0] == 'who':
        return "I am the musician!"
    # Rule 7 Respond to "how"
    if wordlist[0] == 'how':
        return "I practice a lot."
    # Rule 8 Respond to "dislike"
    if 'dislike' in wordlist or 'hate' in wordlist:
        return "You should try listen to some music."
    # Rule 9 Respond to "if"
    if 'think' in wordlist or 'if' in wordlist or 'If' in wordlist:
        return "I agree with you. So let's play some music together?"
    # Rule 10 Respond to "can you" question
    if wordlist[0:2] == ['can', 'you'] or wordlist[0:2] == ['could', 'you']:
        if wordlist[2] == 'play' and wordlist[3] != '':
            return "I can if " + wordlist[3] + ' is a musical instrument.'
        return "Sorry I probably can't. I can only do music."
    # Rule 11 Respond to negativity; cycle feature included
    for word in wordlist:
        if word in negative_words:
            return negative()
    # Rule 12 Respond to "how about"
    if wordlist[0:2] == ['how', 'about']:
        return "I don't mind, but can we play some music first?"
    # Rule 13 Respond to "already"
    if 'already' in wordlist:
        return "Okay, lets's change topic. How about " + change_topic() + "?"
    # Rule 14 Respond to "what"
    if wordlist[0] == 'what':
        return "That depends, if it is related to music, then I might know."
    # Rule 15 Respond to "you are"
    for n in range(0, len(wordlist) - 1):
        if wordlist[n:n+1] == ['you', 'are']:
            return 'I hope I am ' + stringify(wordlist[2:]) + '.'
    # Rule 16 Respond to "you"; random feature included
    if wordlist[0] == 'you':
        return 'I hope I ' + stringify(wordlist[1:]) + ' by playing the ' + random.choice(instrument_list) + "."
    # Rule 17 Respond to greetings
    if wordlist[0] in greeting_words:
        return "Hello! I am a musician! Music is my work! Let's talk!"
    # Rule 18 Respond to actions; memory feature included
    if wordlist[1] in auxiliary_words:
        if wordlist[2] != '' and wordlist[2] not in did_word:
            did_word.append(wordlist[2])
            return "Okay, how about some music?"
        else:
            return "I have heard that before. Shall we change topic? How about " + change_topic() + "?"
    # Rule 19 Respond to random sentences; memory and random feature included
    if wordlist not in random_sentences:
        random_sentences.append(wordlist)
        return "I feel " + random.choice(emotion_list) + " and I want to play the " + random.choice(instrument_list) + "."
    else:
        return "I have heard that before. Shall we change topic? How about " + change_topic() + "?"


def remove_punctuation(text):
    return sub(punctuation_pattern, '', text)


def stringify(wordlist):
    return ' '.join(wordlist)


def do_it_again():
    global dia_count
    dia_count += 1
    return DO_IT_AGAIN[dia_count % 4]


def negative():
    global negative_count
    negative_count += 1
    return NEGATIVE[negative_count % 4]


def change_topic():
    global ct_count
    ct_count += 1
    return TOPIC[ct_count % 4]

opp_preference_list = []

preference_word = ['like', 'love', 'enjoy', 'prefer']

property_list = []

punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:|\"|\'")

emotion_list = ['sad', 'happy', 'confused', 'exciting']

article_list = ['a', 'an', 'the']

instrument_list = ['piano', 'guitar', 'violin', 'trumpet', 'cello', 'drums', 'bass']

property_instrument = {}

DO_IT_AGAIN = ['Let\'s do it together!',
               'Let\'s do it one more time!',
               'We should do it more often.',
               'Why not we do it again?']

dia_count = 0

negative_count = 0

NEGATIVE = ['Let me play some music to cheer you up.',
            'I recommend nocturne to calm you down.',
            'Just listen to some music, you will feel less negative.',
            'If you don\'t feel good, just listen to me playing music.']

greeting_words = ['hello', 'hi', 'greetings', 'good']

auxiliary_words = ['do', 'can', 'should', 'would', 'will', 'shall', 'must']

negative_words = ['cant', 'dont', 'not', 'no', 'negative']

have_list = []

am_list = ['am', 'Im', 'im']

random_sentences = []

ct_count = 0

TOPIC = ['money', 'mexico', 'education', 'healthcare']

did_word = []