# Game theory tournament

# This is a script to represent how the game theory works between players who are called to cooperate with each other or defect.

# Feel free to modify the existing or create your own srategies, or experiment with the points system and extract your own results and conclusions

## ++points differ depending on strategy

from random import randint
from numpy import argsort


# User input choice function for custom player's choices
def user_inp():
    while True:
        try:
            var = int(input('Type 0 to defect or 1 for cooperate: '))
            if var != 0 and var != 1: raise
            break
        except: print('Wrong input!')
    return var


# Rules: {Both cooperate : 3 points each, Both defect : 1 point each, One defects : 5 points, One cooperates : 0 points}
# !!!Changes can be made at this point!!!
rules_dict = {'coop': 3, 'defect': 1, 'solo_defects': 5, 'solo_coops': 0}

# Score resolve function based on the player's choice
def play_round(p1_dec, p2_dec):
    p1_score = p2_score = rules_dict['defect']
    if p1_dec == p2_dec == 1:
        p1_score = p2_score = rules_dict['coop']
    elif p1_dec > p2_dec:
        p2_score = rules_dict['solo_defects']
        p1_score = rules_dict['solo_coops']
    elif p2_dec > p1_dec:
        p1_score = rules_dict['solo_defects']
        p2_score = rules_dict['solo_coops']
    return (p1_score, p2_score)


# Duel function for 1vs1
# Print functions are disabled for now, but feel free to enable them in order to check specific results.
def duel(p1, p2, games, rounds):
    choice_dict = {0: 'Defect', 1: 'Coop'}
    p1_total = p2_total = 0

    for j in range(1, games + 1):
#        print('Game: ', j)
        for i in range(1, rounds + 1):
            p1_curr, p2_curr = p1.choice, p2.choice
            res = play_round(p1_curr, p2_curr)
#            print('Round: ', i)
#            print(f'Players choices: {choice_dict[p1_curr]} - {choice_dict[p2_curr]}')
#            print(f'Round result: {res[0]} - {res[1]}')
            p1_total += res[0]
            p2_total += res[1]
            if hasattr(p1, 'next_choice') and i < rounds: p1.next_choice(p2_curr, res[0])
            if hasattr(p2, 'next_choice') and i < rounds: p2.next_choice(p1_curr, res[1])

    p1_avg = p1_total / games
    p2_avg = p2_total / games
#    print('\nThe average points per game for each player are: ', p1.name, '=', p1_avg, ' : ', p2.name, '=', p2_avg, '\n')
    return (p1_avg, p2_avg)



# Sort dictionary function, to display the results in descending points order
def sort(k,v):
    sorted_value_index = argsort(v)
    desc_value_index = sorted_value_index[::-1]
    sorted_dictonary = {k[i]:v[i] for i in desc_value_index}
    return sorted_dictonary



# Iteration function to make all the players in the list face each other
def all_vs_all(players_list):
    players_dict = {}
    for k in players_list:
        players_dict[k.name] = 0
    for j in range(len(players_list) - 1):
        for i in range(1, len(players_list)):
            if i > j:
                global rounds 
                rounds = 50 # custom number of rounds per game
                games = 5 # custom number of games per duel
                res = duel(players_list[j], players_list[i], games, rounds)
                players_dict[players_list[j].name] += int(res[0])
                players_dict[players_list[i].name] += int(res[1])

    players_dict = sort(list(players_dict.keys()), list(players_dict.values()))
    print(players_dict)



# Classes represent player's strategies

class Player:
    def __init__(self):
        pass


class Custom(Player): # Human player
    def __init__(self):
        super().__init__()
        self.name = input('Type player\'s name: ')
        self.choice = user_inp()

    def next_choice(self, *args):
        self.choice = user_inp()

class Random(Player): # random choice every round
    def __init__(self):
        super().__init__()
        self.name = 'Random'
        self.choice = randint(0,1)
            
    def next_choice(self, *args):
        self.choice = randint(0,1)


class Sneaky(Player): # always defects
    def __init__(self):
        super().__init__()
        self.name = 'Sneaky'
        self.choice = 0     

class Nice(Player): # always coops
    def __init__(self):
        super().__init__()
        self.name = 'Nice'
        self.choice = 1



class Needy(Sneaky): # needs an average of at least 3 points per round
    counter = 0
    global rounds
    def __init__(self):
        super().__init__()
        self.name = 'Needy'
        self.need = 3.0
        self.points = 0

    def next_choice(self, *args):
        if Needy.counter == rounds: 
            Needy.counter = 0
            self.points = 0
        Needy.counter += 1
        self.points += args[1]
        avg_points = self.points / Needy.counter
        self.choice = 0 if avg_points < self.need else 1


    
class Too_Needy(Needy): # needs an average of at least 4 points per round
    def __init__(self):
        super().__init__()
        self.name = 'Too Needy'
        self.need = 4.0

class Not_Needy(Needy): # needs an average of at least 2 points per round
    def __init__(self):
        super().__init__()
        self.choice = 1
        self.name = 'Not Needy'
        self.need = 2.0



class Tit_for_Tat(Nice): # defects after opponent's defect but forgives next round
    def __init__(self):
        super().__init__()
        self.name = 'Tit for Tat'

    def next_choice(self, *args):
        self.choice = args[0]

class Forgive(Nice): # defects after 2 consecutive oppenent's defects and forgives next round
    counter = 0
    def __init__(self):
        super().__init__()
        self.name = 'Forgive'
    
    def next_choice(self, *args):
        if args[0] == 0:
            Forgive.counter += 1
        else:
            Forgive.counter = 0
        if Forgive.counter == 2:
            self.choice = 0
            Forgive.counter = 0
        else:
            self.choice = 1
    
class Revenge(Nice): # defects twice after opponent's defection and then forgives
    counter = 0
    def __init__(self):
        super().__init__()
        self.name = 'Revenge'
    
    def next_choice(self, *args):
        self.choice = args[0]
        if self.choice == 0:
            Revenge.counter = 1
            return
        if Revenge.counter == 1:
            self.choice = Revenge.counter = 0



class UnstableN(Nice): # constantly switch (starts coop)
    def __init__(self):
        super().__init__()
        self.name = 'Unstable Nice'
    
    def next_choice(self, *args):
        self.choice = 0 if self.choice == 1 else 1

class UnstableS(UnstableN): # constantly switch (starts defect)
    def __init__(self):
        super().__init__()
        self.choice = 0
        self.name = 'Unstable Sneaky'



class Devious(Sneaky): # defects when opponent previously cooped
    def __init__(self):
        super().__init__()
        self.name = 'Devious'

    def next_choice(self, *args):
        self.choice = 0 if args[0] == 1 else 1

class Spicy(Sneaky): # defects every 4 rounds
    counter = 0
    global rounds
    def __init__(self):
        super().__init__()
        self.name = 'Spicy'

    def next_choice(self, *args):
        Spicy.counter += 1
        self.choice = 0 if Spicy.counter % 3 == 0 else 1
        if Spicy.counter == rounds: Spicy.counter = 0



class Clever(Sneaky): # tries to predict opponent's choice
    self_choices = []
    opp_choices = []
    counter = 0
    global rounds
    
    def __init__(self):
        super().__init__()
        self.name = 'Clever'
    
    def next_choice(self, *args):
        Clever.counter += 1
        Clever.self_choices.append(self.choice)
        Clever.opp_choices.append(args[0])    
        if Clever.counter <= 10:
            self.choice = 0 if args[0] == 1 else 1
        else:
            for i in range (-10,0):
                pass
        if Clever.counter == rounds: 
            Clever.counter = 0
            Clever.self_choices.clear()
            Clever.opp_choices.clear()


# Feel free to choose which players participate by modifing the list, or creating a new one as argument in the all_vs_all function
# !!!Changes can be made at this point!!!
strat_list = [Random(), Sneaky(), Nice(), Too_Needy(), Needy(), Not_Needy(), Tit_for_Tat(), Forgive(), Revenge(),
              UnstableN(), UnstableS(), Devious(), Spicy()]

all_vs_all(strat_list)

# Watch how the results change when there are many players instead of when there are only a few of them

