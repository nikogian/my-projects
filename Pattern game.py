# Let's play "Find the pattern"

import random

#importing time to make a pause
import time


# User input function
def user_inp():
    x = input("Type Y for Yes or N for No: ").upper()
    while x != "Y" and x != "N":
        x = input("Please type Y for Yes or N for No: ").upper()
    return x


# Player customization function
def player_custom():
    
    print("Number of players: choose in range 4-9")
    while True:
        user_input = input("How many players?: ")
        try:
            player_count = int(user_input)
            if 4 <= player_count <= 9:
                break
            else:
                print("Wrong number of players!")
                print("Please choose a number between 4 and 9")
        except ValueError:
            print("Invalid input. Please enter a valid number.")      

    players_list = []
    for i in range(player_count):
        player = input(f"Name player {i+1}: ").upper()
        while player in players_list:
            print ("This name already exists!")
            player = input(f"Please choose a different name for player {i+1}: ").upper()

        players_list.append(player)

    game = True
    players_list.sort()
    return players_list,player_count,game


# Hint function for when the players lose the game and want to try again
def hint():
    print("Do you want a hint?")
    hint = user_inp()

    if hint == "Y":
        print("The pattern is two yes - one no")
        time.sleep(2)
        print("But...")
        time.sleep(2)
        print("There are some impostors who reset the pattern every time the get they lighter, while they are always a yes")
        time.sleep(2)
        print("The number of impostors depends on the number of the players")
        time.sleep(2)


# Lit or not Lit functions
def lit(a):
    if a == "Y":
        print("Yes, it's ON!")
    else:
        print("No, it's ON!")

def not_lit(a):
    if a == "N":
        print("Yes, it's OFF!")
    else:
        print("No, it's OFF")


# The pattern function
def pattern(player,impostors,count):
    print(f"{player} is it lit or not?")
    tst = user_inp()
    if player in impostors:
        lit(tst)
        count = 0
    elif count == 0 or count == 1:
        lit(tst)
        count += 1
    else:
        not_lit(tst)
        count = 0
    return count


# Impostors reveal function
def reveal(impostrors):
    print("Do you want the impostors to be revealed?")
    a = user_inp()
    if a == "Y":
        print("The impostors are...")
        time.sleep(2)
        print(f"{impostors}")



#The game:

input("Press enter to start the game")

print("Let's play the lighter game...")
time.sleep(1.5)
print("We pass a lighter one to another and guess if its lit or not")
time.sleep(1.5)
print("Good luck and enjoy!")
time.sleep(1.5)

winner = "Congratulations, you won!!!"
loser = "Sorry, you didn't figure out the pattern correctly!"
loser_2 = "Sorry, you lost!"


players_list,player_count,game = player_custom()


while game:   
    if player_count > 6:
        impostors = random.sample(players_list,2)
    else:
        impostors = random.choice(players_list)

    
        while True:
            user_input = input("How many times do we pass the lighter? (5-150 times): ")
            try:
                counter = int(user_input)
                if 5 <= counter <= 150:
                    break
                else:
                    print("Invalid number!")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    input("Press enter to start the pattern")

    player = input(f"Who takes the lighter first? {players_list}: ").upper()
    while player not in players_list:
        print("This player doesn't exist!")
        player = input(f"Who takes the lighter first? {players_list}: ").upper()

    p_count = 0
    
    for i in range(counter):

        plist = [pl for pl in players_list if pl != player]          
        
        plist.sort()
                
        player = input(f"Who do you {player} give the lighter to? {plist}: ").upper()
        while player not in plist:
            print("Please choose one of the remaining players!")
            player = input(f"Who do you give the lighter to? {plist}: ").upper()

        p_count = pattern(player,impostors,p_count)

    print("PATTERN OVER!")

    time.sleep(1.5)

    print("Did you figure out the pattern?")

    final_step = user_inp()

    if final_step == "Y":
        time.sleep(1)
        print("Good job!")
        time.sleep(1)
        print("I guess you also figured out the impostors then...")

        if player_count > 6:
            choice_1 = input("Impostor 1: ").upper()
            while choice_1 not in players_list:
                choice_1 = input("This name is not in the player list. Please select a player for impostor: ").upper()
            choice_2 = input("Impostor 2: ").upper()
            while choice_2 not in players_list:
                choice_2 = input("This name is not in the player list. Please select a player for impostor: ").upper()

            time.sleep(2)
        
            if choice_1 in impostors and choice_2 in impostors:
                result = winner
                print(result)
            elif choice_1 in impostors:
                result = loser
                print(f"Sorry you lost. You only got right the {choice_1} impostor!")
            elif choice_2 in impostors:
                result = loser
                print(f"Sorry you lost. You only got right the {choice_2} impostor!")
            else:
                result = loser
                print(result)
                reveal(impostors)
                 
       
        else:
            choice_1 = input("Impostor: ").upper()
            while choice_1 not in players_list:
                choice_1 = input("This name is not in the player list. Please select a player for impostor: ").upper()

            time.sleep(2)
        
            if choice_1 in impostors:
                result = winner
                print(result)
            else:
                result = loser
                print(result)
                reveal(impostors)
                
    else:
        result = loser_2
        print(result)

    time.sleep(1)  
   
    print("Do you want to play again?")
    new_game = user_inp()
    time.sleep(1)
    if new_game == "Y":
        if result == loser or result == loser_2:
            time.sleep(1)
            hint()

        time.sleep(1)
        print("Same players or not?")
        same_players = user_inp()

        if same_players == "N":
            players_list,player_count,game = player_custom()
    else:
        game = False

    time.sleep(1)


#Game over

feedback = input("Did you like the game?: ")
print(feedback)
print("Thank you very much for the feedback! Bye")

time.sleep(1.5)
input("Press enter to close the game")
    
