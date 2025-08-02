import random

def test():
    print("Hello world!")

def challenge(challenge, player):
    # Universal challenge modus
    earnedPoints = 0

    match challenge:
        case "Running (100yd)":
            # Generic Challenge Format
            for x in range(10):
                earnedPoints += random.randint(1, player.dex)
        case "Archery":
            for x in range(4):
                earnedPoints += random.randint(1, player.dex)
        case "PSaT":
            for x in range(4):
                earnedPoints += random.randint(1, player.int)
        case "BMX Cycling":
            for x in range(4):
                earnedPoints += random.randint(1, player.str)
            for x in range(4):
                earnedPoints += random.randint(1, player.dex)
        case "Obstacle Course":
            for x in range(4):
                earnedPoints += random.randint(1, player.dex)
            for x in range(4):
                earnedPoints += random.randint(1, player.int)
        case "Ninja Takedown":
            for x in range(4):
                earnedPoints += random.randint(1, player.str)
            for x in range(4):
                earnedPoints += random.randint(1, player.int)
        case "The Ultimate Test of Your Sheer Willpower":
            for x in range(4):
                earnedPoints += random.randint(1, player.str)
            for x in range(4):
                earnedPoints += random.randint(1, player.dex)
            for x in range(4):
                earnedPoints += random.randint(1, player.int)
        case "Maxing":
            playerRoll = 1
            while playerRoll > 0:
                playerRoll = random.randint(0, player.str)
                earnedPoints += 1
        case "The FitnessGram Pacer Test":
            playerRoll = 1
            while playerRoll > 0:
                playerRoll = random.randint(0, player.dex)
                earnedPoints += 1
        case "The ASCI Spelling Bee":
            playerRoll = 1
            while playerRoll > 0:
                playerRoll = random.randint(0, player.int)
                earnedPoints += 1
        case "Pole Vault":
            playerRoll1 = random.randint(1, player.str)
            playerRoll2 = random.randint(1, player.dex)
            earnedPoints = (playerRoll1 * playerRoll2)
        case "Discus Throw":
            for x in range(4):
                earnedPoints += random.randint(1, player.str)
        case _:
            earnedPoints = random.randint(1, 20)
            
    return earnedPoints

def challengeMerge(ultimateShowdown, showdownRound, challenges, athletes):
    if ultimateShowdown == True:
        challengeName = challenges[showdownRound]
    else:
        challengeTypes = ["Running (100yd)", "Archery", "PSaT", "BMX Cycling", "Obstacle Course", "Ninja Takedown", "The Ultimate Test of Your Sheer Willpower", "Maxing", "The FitnessGram Pacer Test", "The ASCI Spelling Bee", "Pole Vault", "Discus Throw"]
        challengeName = random.choice(challengeTypes)
        challenges.append(challengeName)

    playerPoints = [0] * len(athletes)
    print(f"Challenge: {challengeName}")

    for player in range(len(athletes)):
        playerPoints[player] = challenge(challengeName, athletes[player])

    # Sort the points per player, returning a list of players from MOST POINTS to LEAST.

    results = playerPoints.copy()
    results.sort(reverse=True)
    
    print(f"Results:")
    for x in range(len(athletes)):
        print(f"{athletes[x].name}: {playerPoints[x]}")
    for x in range(len(results)):

        index = playerPoints.index(results[x])
        results[x] = index
        playerPoints[index] = 0 # Clears the player's index so that repeat values aren't used. This breaks the sim

    return results

