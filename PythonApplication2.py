import random
import os
import time
import math

inv = [] #ekwipunek
command = None
str = 5 #siła
agi = 5 #zręczność
vit = 5 #żywotność
hp = None #punkty życia
att = 0 #siła ataku
name = None #imię postaci
answer = None
enstr = 0 #siła wroga
enagi = 0 #zręczność wroga
envit = 0 #żywotność wroga
enhp = 0 #punkty życia wrogatat
enatt = 0 #siła ataku wroga
ename = None #nazwa wroga
newitem = None
fenatt = 0 #finalny atak wroga
fatt = 0 #finalny atak postaci
pxp = 0 #xp bohatera
enxp = 0 #xp za przeciwnika
exp = 1 #xp potrzebne do nastepnego lvlu
plvl = 1 #lvl bohatera

def menu():
    global command, answer, inv, name
    os.system("cls")
    print("Welcome to the simple text game by Adam Gabrysiak and Mateusz Zagorski."
          "\n\n\t\t**THE MAIN MENU**"
          "\n\n1. Create a new character and start a new game. (Start)"
          "\n2. Continue"
          "\n3. Exit")
    command = input(": ")
    command = command.lower()
    answer = ["start", "s", "continue", "c", "exit", "e"]
    invalid(answer)
    os.system("cls")
    if command == "start" or command == "s":
        champ()
    if command == "exit" or command == "e":
        exit()
    if command == "continue" or command == "c":
        if name == None:
            print("\nThere is nothing you can continue.")
            menu()
        else:
            start()

def showeq():
    global command, answer
    command = str(input("\nWould you like to see yout inventory? (yes/no): "))
    answer = ["yes", "no"]
    invalid(answer)
    os.system("cls")
    if command == "yes":
        eq()
    if command == "no":
        menu()

def eq():
    command = None
    global inv, vit, str, agi
    if "sword" in inv:
        str += 5
    elif "boots" in inv:
        agi += 5
    elif "armor" in inv:
        vit += 5
    elif "amulet" in inv:
        str += 5
        agi += 5
        vit += 5
    calcstats()
    print("\nYou have ", len(inv), "items in your inventory.\nYour inventory consists of: ")
    if len(inv) != 0:
        for item in inv:
            print(item)
    else:
        print("Nothing.")
    input()
    start()

def additem():
    global inv, answer, command, newitem
    if newitem == None:
        command = input("\nWould you like to add an item? (yes/no): ")
        answer = ["yes", "y", "no", "n"]
        invalid(answer)
        if command == "yes" or command == "y":
            newitem = input("\nWhat item do you want to add?: ")
            inv.append(newitem)
            print("Item has been added")
            newitem = None
            start()
        if command == "no" or command == "n":
            start()
    else:
        command = input("\nWould you like to add the item to your inventory?  (yes/no): ")
        answer = ["yes", "y", "no", "n"]
        invalid(answer)
        if command == "yes" or command == "y":
            if newitem in inv:
                print("You can't take two items of the same kind")
                time.sleep(2)
            else:
                inv.append(newitem)
                print("Item has been added")
                newitem = None
                eq()
                start()
        if command == "no" or command == "n":
            start()

def invalid(answer):
    global command
    while command not in answer:
        print("Invalid answer. You can only use", answer, ". Try again.")
        command = input(": ")

def champ():
    global command, name, str, agi, vit, hp
    os.system("cls")
    clear()
    command = None
    name = input("\nState the name of the character: ")
    print("\nWhat is the strongest side of your character?: "
          "\n\t1. Strength"
          "\n\t2. Agility"
          "\n\t3. Vitality")
    command = input("\n:")
    answer = ["1","2","3"]
    invalid(answer)
    if command == "1":
        str += 2
    elif command == "2":
        agi += 2
    elif command == "3":
        vit += 2
    calcstats()
    start()

def start():
    global command, answer, inv
    os.system("cls")
    calcstats()
    print("\nFor some unknown to you reason you are imprisoned in a dark dungeon. \nYou are safe for now and you attend to your wounds."
          "\n\nIf you want to see", name, "'s inventory then write 'inventory'"
          "\nIf you want to go back to the menu write 'menu'"
          "\nIf you want to see", name, "'s statistics then write 'stats'"
          "\nIf you want to explore write 'explore'")
    command = input("\n: ")
    command = command.lower()
    answer = ["explore", "e", "inventory", "i", "menu", "m", "stats", "s", "debug"]
    invalid(answer)
    if command == "inventory" or command == "i":
        eq()
    elif command == "explore" or command == "e":
        fight()
    elif command == "menu" or command == "m":
        menu()
    elif command == "stats" or command == "s":
        stats()
    elif command == "debug":
        additem()    
    
def fight():
    global hp, enhp, enatt, command, answer, name, att, fenatt, fatt, pxp
    os.system("cls")
    randomenemy()
    while enhp > 0 and hp > 0:
        ranchance()
        print("\n", ename, " attacks! He hits", name, "for", fenatt, "points.")
        hp = hp - fenatt
        if hp <= 0:
            print("\nYou have lost. You are a disgrace to the mankind")
            input()
            clear()
            menu()
        print("\n", name, "has", hp, "health points and", ename, "has", enhp, "health points.")
        command = input("\nWould you like to fight or run like a little bitch?" "\nIf you have a healing potion you can heal your wounds.: " )
        answer = ["run", "r", "fight", "f", "heal", "h"]
        os.system("cls")
        invalid(answer)
        if command == "run" or command == "r":
            start()
        elif command == "fight" or command == "f":
            print("\nWith all your might you hit", ename, "for", fatt, "points.\nHe is confused as to why did you do that.")
            enhp = enhp - fatt
        elif command == "heal" or command == "h":
            if "healing potion" in inv:
                calcstats()
            else:
                print("You don't have a healing potion.")
    if enhp <= 0:
        print("\nYou have won. Yay. Your hero gain", enxp, "xp!")
        dropitem()
        print("\n")
        pxp = enxp + pxp
        lvlup()
        if newitem != None:
            additem()
        else:
            input()
            start()
        
def stats():
    global name, vit, agi, str, hp, pxp, plvl
    os.system("cls")
    print("\n\nYour character's name is", name, ". \nHe has:\n", str, "points of strenght,\n", agi, "points of agility \n", vit, "points of vitality (which gives the character", hp, "health points.)", "\n Your character has:", pxp, "xp points. \n Your character level is:", plvl, "\n You need:", math.floor(10 * math.pow(exp,2)) - pxp, "xp points to lvl up")
    input()
    start()

def calcenstats():
    global envit, enhp, enatt, enstr, enagi
    enhp = envit * 10
    enatt = enstr * 2 + enagi * 2

def calcstats():
    global hp, vit, str, agi, att
    hp = vit * 10
    att = str * 2 + agi * 2

def clear():
    global name, str, vit, agi, hp, att, inv, newitem, pxp
    name = None
    str = 15
    vit = 15
    agi = 15
    pxp = 0
    att = None
    hp = None
    inv = []
    newitem = None

def randomenemy():
    choice = random.randrange(5)
    if choice == 0:
        goblin()
    elif choice == 1:
        ghoul()
    elif choice == 2:
        troll()
    elif choice == 3:
        janusz()
    elif choice == 4:
        bardlord()

def lvlup():
    global pxp, str, agi, vit, exp, plvl
    if pxp >= math.floor(10 * math.pow(exp,2)): 
        plvl = plvl + 1
        addstats()
        calcstats()
        pxp = 0
        exp = exp * math.pow(1.1,2)
        print("Congratulations You leveledup")

def addstats():
    global str, agi, vit
    str = str + 1
    agi = agi + 1
    vit = vit + 1

def goblin():
    global enstr, envit, enagi, enhp, ename, enxp
    os.system("cls")
    ename = "Goblin"
    enstr = 2
    enagi = 2
    envit = 2
    enxp = 2
    calcenstats()
    print("\nYou have met a goblin. He is quite weak")

def hobgoblin():
    global enstr, envit, enagi, enhp, ename, enxp
    os.system("cls")
    ename = "HobGoblin"
    enstr = 3
    enagi = 3
    envit = 3
    enxp = 3
    calcenstats()
    print("\nYou have met a hobgoblin. It seems like goblins are making armor now for themselves")

def ghoul():
    global enstr, envit, enagi, enhp, ename, enxp
    os.system("cls")
    ename = "Ghoul"
    enstr = 4
    enagi = 4
    envit = 4
    enxp = 3
    calcenstats()
    print("\nYou have met a ghoul. He is really ugly")

def troll():
    global enstr, envit, enagi, enhp, ename, enxp
    ename = "Troll"
    enstr = 5
    enagi = 1
    envit = 10
    enxp = 5
    calcenstats()
    print("\nBefore you stands a mighty troll. He is as strong as he is ugly. \nHe grins at you and says 'Fresh meat'.")

def bardlord():
    global enstr, envit, enagi, enhp, ename, enxp
    os.system("cls")
    ename = "Bardlord"
    enstr = 8
    enagi = 5
    envit = 5
    enxp = 8
    calcenstats()
    print("\nWalking through the forest You encountered an ancient creature. It's a Bardlord from Summoner's Rift. He's collecting meeps peacefully, when suddenly ") 

def janusz():
    global enstr, envit, enagi, enhp, ename, enxp
    ename = "Janusz"
    enstr = 1
    enagi = 30
    envit = 5
    enxp = 10
    calcenstats()
    print("\nIn the depths of this forsaken dungeon you meet a strange creature. He is scarily tall and his eyes gleam with unbound insanity.\nYou can hear him muttering angrily, over and over the same phrase.\n'WHY ARE THOSE CABLES AREN'T WORKING'")

def dropitem():
    global newitem, ename
    choice = random.randrange(10)
    if choice == 0:
        newitem = "sword"
    elif choice == 1:
        newitem = "armor"
    elif choice == 2:
        newitem = "boots"
    elif choice == 3:
        newitem = "amulet"
    elif choice == 4:
        newitem = "healing potion"
    else:
        newitem = None
    if newitem != None:
        print("After looking at", ename, "'s dead body you see that he had", newitem)
    else:
        print("Bad luck. The enemy had nothing")

def ranchance():
    global enatt, att, fenatt, fatt
    ran = random.randrange(100)
    if 0 < ran < 10:
        attack = 0.0
    elif 10 <= ran < 30:
        attack = 0.5
    elif  30 <= ran < 50:
        attack = 0.75
    elif 50 <= ran < 70:
        attack = 1.0
    elif 70 <= ran < 90:
        attack = 1.25
    else:
        attack = 1.5
    fatt = att * attack
    fenatt = enatt * attack

menu()
