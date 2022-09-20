"""GachaGuys Program."""


import os
from datetime import datetime

from GachaGuy import GachaGuy
from GuyCollection import GuyCollection
from wonderwords import RandomWord

ENERGY_DEFAULT = 100

FILE_SAVE = "gacha_guys_save.txt"

FILE_PROJECT = "../GachaGuys"

HEADING_TITLE = """  ___   ___    ___   _  _   ___      ___   _   _  __   __  ___
 / __| /   \  / __| | || | /   \    / __| | | | | \ \ / / / __|
| (_ | | - | | (__  | == | | - |   | (_ | | |_| |  \ V /  \__ \ 
 \___| |_|_|  \___| |_||_| |_|_|    \___|  \___/    |_|   |___/
---------------------------------------------------------------"""
INSTRUCTIONS = """Welcome to Gacha Guys, a text gacha game about guys.
              
Adventure with your guys to get gifts and fight bad guys.
Shift one of your guys to the front to take all the hits.
Train your guys in pairs for xp, but don't train too hard.
If they're the same stick type, the guy-ness can go up.
If a guy dies, your other guys share his max hp to heal.
Open gifts to get new guys and buy stuff from the shop.\n"""
WELCOME = "Welcome back!\n"
MENU = """(A) Adventure
(L) List Guys
(S) Shift Guy
(T) Train Guy
(P) Pull Guys
(Q) Quit"""

HEADING_LIST = "         YOUR GUYS\n---------------------------"
HEADING_SHIFT = "         SHIFT GUYS\n---------------------------"
HEADING_TRAIN = "         TRAIN GUYS\n---------------------------"
HEADING_PULL = "         PULL GUYS\n---------------------------"

MESSAGE_PULL = "You got a guy!\n"
MESSAGE_NO_GUYS = "No guys... :(\n"
MESSAGE_NEVERMIND = "Nevermind!"

ERROR_GUY = "Invalid guy!\n"
ERROR_CHOICE = "Invalid choice!\n"


def main():
    """Program for Gacha Guys."""
    print(HEADING_TITLE)
    guy_collection = GuyCollection()

    # item_to_amount = {"Guy Box": 1}

    os.chdir(FILE_PROJECT)
    if os.path.exists(FILE_SAVE):
        print(WELCOME)
        energy, max_energy = load_file(guy_collection)
    else:
        print(INSTRUCTIONS)
        print(MESSAGE_PULL)
        energy = ENERGY_DEFAULT
        max_energy = ENERGY_DEFAULT
        pull_guy(guy_collection)

    print(f"{energy}/{max_energy} energy left!\n")
    print(MENU)
    choice = input("> ").upper()
    while choice != "Q":
        if choice == "A":
            pass
        elif choice == "L":
            print(HEADING_LIST)
            list_guys(guy_collection)
        elif choice == "S":
            print(HEADING_SHIFT)
            shift_guy(guy_collection)
        elif choice == "T":
            print(HEADING_TRAIN)
            train_guy(guy_collection)
        elif choice == "P":
            pull_guy(guy_collection)
        else:
            print(ERROR_CHOICE)
        print(MENU)
        choice = input("> ").upper()

    # save file
    with open(FILE_SAVE, "w") as out_file:
        print(energy, file=out_file)
        print(max_energy, file=out_file)
        print(datetime.now().strftime("%Y, %m, %d, %H, %M, %S"), file=out_file)
        for guy in guy_collection.guys:
            print(guy.enter(), file=out_file)


def pull_guy(guy_collection):
    """Pull a new guy."""
    pulled_guy = GachaGuy(
        RandomWord().word(include_categories=["adjectives"]).title())
    print(pulled_guy)  # TODO letter dungeon, word length dungeon, starter dungeon, rarity dungeon, level dungeon
    nickname = input("What will his nickname be? ").title()  # TODO dungeons reset daily, weekly, hourly
    pulled_guy.handle_nickname(nickname)
    guy_collection.add_guy(pulled_guy)


def load_file(guy_collection):
    """Load a save file for energy and guys."""
    # read file
    with open(FILE_SAVE) as in_file:
        energy = int(in_file.readline())
        max_energy = int(in_file.readline())
        year, month, day, hour, minute, second = tuple([int(part) for part in in_file.readline().split(",")])
        lines = in_file.readlines()

    # add guys in file to collection
    for line in lines:
        adj, nickname, is_alive, level, rarity, xp, max_xp, attack, hp, max_hp = tuple(line.split(", "))
        guy_collection.add_guy(GachaGuy(adj, nickname, is_alive, level, rarity, xp, max_xp, attack, hp, max_hp))

    # calculate energy from last logoff
    logoff_datetime = datetime(year, month, day, hour, minute, second)
    current_datetime = datetime.now()
    datetime_difference = current_datetime - logoff_datetime
    minutes_difference = round(datetime_difference.total_seconds() / 60)
    for i in range(minutes_difference):
        energy += 1
    if energy >= max_energy:
        return max_energy, max_energy
    else:
        return energy, max_energy


def list_guys(guy_collection):
    """Print the list of guys, if there are any."""
    if not guy_collection.guys:  # if list of guys is empty
        print(MESSAGE_NO_GUYS)
    else:
        for guy in guy_collection.guys:
            print(guy)


def train_guy(guy_collection):
    """Train a guy from a list of guys with another guy for xp."""
    trainee_name = get_valid_name(guy_collection.guys, "Who do you want to train? ")
    if trainee_name == "":
        print(MESSAGE_NEVERMIND)
        return

    trainer_name = get_valid_name(guy_collection.guys, "Who do you want training him? ")
    if trainer_name == "":
        print(MESSAGE_NEVERMIND)
        return

    trainee_index = 0
    trainer_index = 0
    for index, guy in enumerate(guy_collection.guys):
        if trainee_name == guy.name:
            trainee_index = index
        elif trainer_name == guy.name:
            trainer_index = index
    guy_collection.guys[trainee_index].handle_train(guy_collection.guys[trainer_index])  # ignore warnings
    guy_collection.handle_death()  # TODO "get_guy" method in GuyCollection that takes in strings?


def get_valid_name(guys, prompt):
    """Get a valid name of a guy that must be in the list of guys."""
    guy_names = [guy.name for guy in guys]
    name = input(prompt).title()
    while name not in guy_names:
        if name == "":
            return ""
        print(ERROR_GUY)
        name = input(prompt).title()
    return name


def shift_guy(guy_collection):
    shifted_name = get_valid_name(guy_collection.guys, "Who do you want to shift? ")
    shifted_index = 0
    for index, guy in enumerate(guy_collection.guys):
        if shifted_name == guy.name:
            shifted_index = index
    guy_collection.shift_guy_to_front(guy_collection.guys[shifted_index])


main()
