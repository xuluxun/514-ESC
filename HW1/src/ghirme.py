# Eden Ghirmai
# CSE415 Spr16 - 4/6/2015
# Assignment 1: Basics of Python and String Manipulation
#
# This program contains an introduce, agentName and respond method for the agent "Donald Trump"
# Based on given responses he will respond accordingly matching his personality 

import random
from re import *   # Loads the regular expression module.


def introduce():
  return """Hi, I'm Donald Trump, and I am here to make America great again.
Eden Ghirmai programmed me, but I like to think you can\'t really code a mind
like mine. But if you get offended easily, contact her at ghirme@uw.edu
Now what do you want?"""

def agentName():
  return "Trump"

FREE_FORM_RESPONSE = ['WOW you are just so0o0o interesting.',
                      'I shall overcomb.',
                      'There will be hell toupee!',
                      'You should really comb down.',
                      'Yeahhhh uh huh.',
                      'Bing bing bong bong bing bing bing.']

INSTRUMENTS = ['piano', 'guitar', 'violin', 'trumpet', 'cello', 'drums', 'bass']

dislikes = []
verbs = []
played_instruments = []
i_am_cycle = 0
why_cycle = 0 
hungry_cycle = 0 
practice_cycle = 0


def respond(the_input):
  'Takes the given input (string) and returns a response (string)'

  the_input = the_input.strip()
  wordlist = split('[ \t]+', remove_punctuation(the_input))
  wordlist[0] = wordlist[0].lower()

  if 'education' in wordlist: 
    return 'Education is too high of a cost in America. If you want a good education work hard and make your own money.'
  elif 'healthcare' in wordlist:
    return 'I mean how silly is free healthcare? Pull yourself by your own bootstraps America!'
  elif 'ted' in wordlist and 'cruz' in wordlist:
    return 'Ted Cruz? All I know about that guy is that his face looks like a square. If you ever tell him be there or be square he never shows up.'
  elif 'work' in wordlist:
    return 'Who are you to talk about work? You\'re fired!'
  elif 'eat' in wordlist or 'food' in wordlist or 'hungry' in wordlist or 'eating' in wordlist:
    global hungry_cycle
    hungry_cycle += 1

    if hungry_cycle % 3 == 0:
      return 'Mmm all this talk about food makes me want to eat some Sharper Image Trump Steaks!'
    elif hungry_cycle % 3 == 1:
      return 'I love eating Steak, especially Trump Steaks. '
    elif hungry_cycle % 3 == 2:
      return 'Think about food some more, then buy some Trump Steak'
  elif 'day' in wordlist:
    return 'The day will be better once I\'m president. America will be great once again.'
  elif 'mexico' in wordlist:
    return 'Oh yeah, we are gonna have a HUGE wall. I mean HUUUGE. And we\'ll make Mexico pay for it'
  elif 'music' in wordlist:
    global practice_cycle
    practice_cycle += 1
    if practice_cycle % 2 == 0:
      return 'They say practice makes perfect, but I am already perfect'
    else:
      return 'I am in no need of practicing, I was born an excellent businessman'

  elif 'play' in wordlist or 'using' in wordlist:
    if 'play' in wordlist:
      index = wordlist.index("play")  
      instrument = wordlist[index + 2]
    else:
      index = wordlist.index("using")
      instrument = wordlist[index + 1]

    if 'music' in wordlist:
      return 'Who do you think you are talking about music so much?'

    if instrument in played_instruments:
      return 'You already told me you can play the ' + instrument + '!'
    else:
      played_instruments.append(instrument)
      return 'How did you learn how to use a ' + instrument + '? I own 30 symphonies.'
  elif 'money' in wordlist:
    return 'I have two donate buttons on my website, but yes I am a billionaire and fund my own campaign.'
  elif wordlist[0:2] == ['i', 'am']: # CYCLE FEATURE 1
    global i_am_cycle
    recreate = you_me_map(wordlist[2:])
    i_am_cycle += 1 

    if i_am_cycle % 3 == 0:
      return 'Do you think I even care that you\'re ' + stringify(recreate) + '? \nI became a billionaire with a small loan of a million dollars!'
    elif i_am_cycle % 3 == 1:
      return 'Me this and me that, you can\'t seem to get enough of yourself can you?'
    elif i_am_cycle % 3 == 2:
      return 'You are '  + stringify(recreate) + ' huh? How interesting because I always thought you were quite the opposite'
  elif wordlist[0:2] == ['you', 'are']:
    recreate = you_me_map(wordlist[2:])
    return 'You know what, maybe I am ' + stringify(recreate) + ' but I am the best damn American at doing it there is. I tell it like it is.'
  elif wordlist[0:3] == ['i', 'don\'t', 'like'] or wordlist[0:2] == ['i', 'dislike'] or wordlist[0:2] == ['i', 'hate']: # MEMORY FEATURE
    if wordlist[1] == 'don\'t':
      recreate = you_me_map(wordlist[3:]) 
    else:
      recreate = you_me_map(wordlist[2:]) 
    
    if recreate in dislikes:
      return 'You seem to dislike a lot of things, especially ' + stringify(recreate) + ', maybe you should get over it. People are offended to easily these days.'
    else:
      dislikes.append(recreate)
      return 'You dislike ' + stringify(recreate) + "? Seems you have a problem with people just telling it like it is."
  elif wordlist[0:2] == ['i', 'like'] or wordlist[0:2] == ['i', 'love']:
    recreate = you_me_map(wordlist[2:])
    return 'Probably not as much as America loves me.'
  elif wordlist[0] == 'i' and verbp(wordlist[1]):
    verb = wordlist[1]
    recreate = you_me_map(wordlist[1:])
    if verb in verbs:
      return 'You always have to ' + verb + ' don\'t you?'
    else:
      verbs.append(verb)
      return 'You ' + stringify(recreate) + ', huh? Well I feel hungry. Hungry for Trump Steaks. ' 
    
  elif wordlist[0] == 'why': # CYCLE FEATURE 2
    global why_cycle
    recreate = you_me_map(wordlist[1:])
    why_cycle += 1

    if why_cycle % 3 == 0:
      return 'You know I don\'t really need to be answering any of your dumb questions. Try talking like an Amurican.'
    elif why_cycle % 3 == 1:
      return 'Why ' + stringify(recreate) + '? I\'ll tell you why. I have a business background and that will make me the best president you could ask for. '
    elif why_cycle % 3 == 2:
      return 'You seem to keep asking why, why this why that, why ' + stringify(recreate) + " have you heard of the internet? Look it up!"

    return 'You know there\'s a lot of things I know. I\'ve done a lot of research in my life. Lots of problems but we will figure out why ' + stringify(recreate) + ' and will solve all the country\'s problems'
  else: # RANDOM-CHOICE FEATURE  
    randomIndex = random.randrange(len(FREE_FORM_RESPONSE)) 
    return FREE_FORM_RESPONSE[randomIndex]

CASE_MAP = {'i':'you', 'I':'you', 'me':'you','you':'me',
            'my':'your','your':'my',
            'yours':'mine','mine':'yours','am':'are'}

def you_me(w):
    'Changes a word from 1st to 2nd person or vice-versa.'
    try:
        result = CASE_MAP[w]
    except KeyError:
        result = w
    return result

def you_me_map(wordlist):
    'Applies YOU-ME to a whole sentence or phrase.'
    return [you_me(w) for w in wordlist]


def remove_punctuation(text):
    punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")  
    return sub(punctuation_pattern,'', text)

def stringify(wordlist):
    'Create a string from wordlist, but with spaces between words.'
    return ' '.join(wordlist)

def verbp(w):
    'Returns True if w is one of these known verbs.'
    return (w in ['go', 'have', 'be', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink',
                  'blink', 'crash', 'crunch', 'add', 'feel', 'practice'])









