def Roman2():
    """Roman numeral conversion with ordered Production System"""
    x = ''; ans = ''
    while True:
        if x=='': x = input('Enter number: ')
        elif x > 39:
            print('too big'); x = ''
        elif x > 9:
            ans += 'X'; x -= 10
        elif x == 9:
            ans += 'IX'; x = 0
        elif x > 4:
            ans += 'V'; x -= 5
        elif x == 4:
            ans += 'IV'; x = 0
        elif x > 0:
            ans += 'I'; x -= 1
        elif x == 0:
            print(ans); x = ''; ans = ''
        else: print('bad number'); break

Roman2()
