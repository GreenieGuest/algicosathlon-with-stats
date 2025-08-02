import random
import math
from time import sleep
from colorama import Fore, Style
import json
from challenges import challengeMerge
import os
from pathlib import Path

file = Path(__file__)
parent = file.parent
os.chdir(parent)

# [[ CONFIGURATION ]] ----------------------------------------------------------------------------------
# Player Names
season_name = "Algicosathlon with Stats"
names = ["Red","Orange","Tan","Yellow","Lime","Green","Cyan","Blue","Navy","Purple","Pink","Lavender","Magenta","Gray","Brown","Olive"]
base_points = [100,70,50,40,30,25,20,15,12,10,8,6,4,3,2,1]

FASTFORWARD = False

PRESET_PROFILES = False
PROFILE_FILE_PATH = 'profiles.json'

# If you know what you're doing, have fun tweaking below! ----------------------------------------------------------------------------------

# [[ IMPORTANT SIMULATION STUFF ]] ----------------------------------------------------------------------------------
bootOrder = []
challenges = []
round = 1

class Player:
    def __init__(self, name, points, finalePoints, lastPlacement, str, dex, int):
        self.name = name
        # Game Points
        self.points = points
        self.finalePoints = finalePoints
        self.lastPlacement = lastPlacement

        # Stats
        self.str = str
        self.dex = dex
        self.int = int

def decode(obj):
    return Player(obj['name'], 0, 0, 0, obj['strStat'], obj['dexStat'], obj['intStat'])
    
# [[ SIM FUNCTIONS ]] ----------------------------------------------------------------------------------

def Elimination(athletes):
    athletes.sort(key=getPoints)
    eliminated = athletes[0]

    athletes.sort(reverse=True, key=getPoints)
    stillInTheRunning(athletes, True)
    wait(3)
    print(f"{eliminated.name} has been {Fore.RED}ELIMINATED{Style.RESET_ALL} with {eliminated.points} points. {numPlayers - 1} remain.\n")
    athletes.remove(eliminated)

    bootOrder.insert(0, eliminated)
        
def stillInTheRunning(athletes, update):
    for x in range(len(athletes)):
        if update == True:
            if x < athletes[x].lastPlacement:
                print(f"{x+1}{suffix(x+1)} | {athletes[x].name} - {athletes[x].points} {Fore.GREEN}(↑{athletes[x].lastPlacement - x}){Style.RESET_ALL}")
            elif x > athletes[x].lastPlacement:
                print(f"{x+1}{suffix(x+1)} | {athletes[x].name} - {athletes[x].points} {Fore.RED}(↓{x - athletes[x].lastPlacement}){Style.RESET_ALL}")
            else:
                print(f"{x+1}{suffix(x+1)} | {athletes[x].name} - {athletes[x].points}")
            athletes[x].lastPlacement = x
        else:
            print(f"{x+1}{suffix(x+1)} | {athletes[x].name} - {athletes[x].points}")
    print(" ")

def suffix(n):
    if 11 <= n % 100 <= 13:
        return "th"
    else:
        return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

def proceed():
    proceed = input("Press enter to proceed.")
    print(" ")

def getPoints(player):
    """
    Get a stat.
    """
    return player.points

def wait(time): # Lua relic
    if FASTFORWARD == False:
        sleep(time)

# [[ SIMULATION ]] ----------------------------------------------------------------------------------
athletesList = [Player(item, 0, 0, 0, random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)) for item in names]

if PRESET_PROFILES == True:
    try:
        with open(PROFILE_FILE_PATH, 'r') as f:
            data = json.load(f, object_hook=decode)

            for player in range(min(len(athletesList), len(data))): # If not 64 players, then replace up to that many players
                athletesList[player] = data[player]

            # if more than default entries, add them to the pile so they might be picked out via random sample
            if len(data) > len(athletesList):
                athletesList.extend(data[len(athletesList):])
    except FileNotFoundError:
        print(f"Error: file '{PROFILE_FILE_PATH}' not found")
    except json.JSONDecodeError:
        print(f"Error: syntax error in '{PROFILE_FILE_PATH}'")
    except Exception as e:
        print(f"Error: {e}")

athletes = random.sample(athletesList, 16) # more than 16 is bad mkay
castSize = len(athletes)
numPlayers = len(athletes)

proceed()

while numPlayers > 2:
    print(f"[- Day {castSize + 1 - numPlayers} -]\n")
    stillInTheRunning(athletes, False)
    
    placements = challengeMerge(False, 0, challenges, athletes)
    for x in range(len(placements)):
        print(f"{x+1}{suffix(x+1)}: {athletes[placements[x]].name} - +{math.ceil(base_points[x] * 1.5 ** (round-1))} points")
    print(" ")

    wait(2)

    stillInTheRunning(athletes, False)

    wait(.5)

    for x in range(len(placements)):
        athletes[placements[x]].points += math.ceil(base_points[x] * 1.5 ** (round-1))
    
    stillInTheRunning(athletes, False)

    wait(.5)

    Elimination(athletes)
    numPlayers -= 1
    round += 1
    proceed()
stillInTheRunning(athletes, False)
print(f"[- Day {castSize} -]\n")
print("The final challenge, to decide which of the final 2 wins, is a marathon of every previous challenge in order. The player with the most wins at the end wins the season.")
proceed()

# Ultimate Showdown

for x in range(castSize - 2):
    challengeResults = challengeMerge(True, x, challenges, athletes)
    challengeWinner = athletes[challengeResults[0]]
    if athletes[challengeResults[0]] == athletes[challengeResults[1]]:
        print(f"Round {x+1}: Draw, status quo. | {athletes[0].name}: {athletes[0].finalePoints}, {athletes[1].name}: {athletes[1].finalePoints}\n")
    else:
        challengeWinner.finalePoints += 1
        print(f"Round {x+1}: {challengeWinner.name} wins. | {athletes[0].name}: {athletes[0].finalePoints}, {athletes[1].name}: {athletes[1].finalePoints}\n")
    wait(0.5)


runnerUp = None
if athletes[0].finalePoints < athletes[1].finalePoints:
    runnerUp = athletes[0]
elif athletes[1].finalePoints < athletes[0].finalePoints:
    runnerUp = athletes[1]
else: #Tie
    print(f"The votes tied, so a loser will be randomly chosen.")
    runnerUp = random.choice(athletes)
wait(1)

athletes.remove(runnerUp)
print(f"{runnerUp.name} failed to win and was eliminated in 2nd.")
numPlayers -= 1
bootOrder.insert(0, runnerUp)

winner = random.choice(athletes)
bootOrder.insert(0, winner)
athletes.remove(winner)
print(f"{winner.name} is the winner of {season_name}.")

proceed()
for x in range(len(bootOrder)):
    print(f"{x+1}{suffix(x+1)}: {bootOrder[x].name} - {bootOrder[x].points}")
        

proceed()
