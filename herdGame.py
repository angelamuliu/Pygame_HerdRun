
#HERD RUN

"""
A fun action game with strategic elements mixed in!
The goal is to reach the point goal in order to move on to the next level.
Points are earned by dropping cows into a pen area. However, watch the time!
The game is over when the time runs out!
"""

import pygame, random, sys, os
from pygame.locals import *
import object_creator, Util

#We will use globals to store vital information.
FPS = 60

def initiateGameValues():
    global playerObj1, monster1, animals, powerUps, score, weapons

    #Setting up player, animal, monster, and powerup objects
    playerObj1 = object_creator.Player()
    monster1 = object_creator.Monster()
    animals = []
    powerUps = []
    score = object_creator.Score()
    weapons = object_creator.Weapon()
    spawnAnimals()

#MAIN - run function, intialize values
def run():
    #These globals are more constant and not reset when a new game is created
    global fpsClock, surface, sfx
    global startScreen, instructions, gameOverBoard
    
    pygame.init()
    fpsClock = pygame.time.Clock()
    surface = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Save ALL the animals!")
    
    # Loading and playing background music:
    pygame.mixer.music.load(os.path.join("sound", 'Bits-Of-Happiness-8.mp3'))
    pygame.mixer.music.play(-1, 0.0) #-1 => REPEATS FOREVER.
    
    #Loading sound effects
    sfx = {}
    sfx["pickup"] = pygame.mixer.Sound(os.path.join("sound", "sfx_pickup.wav"))
    sfx["drop"] = pygame.mixer.Sound(os.path.join("sound", "sfx_drop.wav"))
    sfx["hit"] = pygame.mixer.Sound(os.path.join("sound", "sfx_hit.wav"))
    sfx["powerup"] = pygame.mixer.Sound(os.path.join("sound", "sfx_powerup.wav"))
    sfx["attackZAP"] = pygame.mixer.Sound(os.path.join("sound", "sfx_attackZAP.wav"))
    sfx["attackFOOD"] = pygame.mixer.Sound(os.path.join("sound", "sfx_attackFOOD.wav"))
    sfx["attackFIRE"] = pygame.mixer.Sound(os.path.join("sound", "sfx_attackFIRE.wav"))
    sfx["monsterEatAnimal"] = pygame.mixer.Sound(os.path.join("sound", "sfx_monsterEatAnimal.wav"))
    sfx["monsterEatFood"] = pygame.mixer.Sound(os.path.join("sound", "sfx_monsterEatFood.wav"))
    
    startScreen = True
    instructions = False
    
    instructBoard = pygame.image.load(os.path.join("images", "splash_Controls.png"))
    startBoard = pygame.image.load(os.path.join("images", "splash_Start.png"))
    gameOverBoard = pygame.image.load(os.path.join("images", "gameOver.png"))
    
    while True:
        #runSplash will set startScreen to False once player decides to start playing game
        while startScreen:
            runSplash(instructBoard, startBoard)
        
        #New game -> Reset vital game values and then go into main game loop
        initiateGameValues()
        while not score.gameOver:
            runGame()

        while score.gameOver:
            gameoverMove()
            #get gameover move

############### SPLASH SCREEN #################

def runSplash(iB, sB):
    redrawSplash(iB, sB)
    getMoveSplash()
    pygame.display.update()

def redrawSplash(iB, sB):
    if instructions:
        surface.blit(iB, (0,0))
    else:
        surface.blit(sB, (0,0))

def getMoveSplash():
    global startScreen, instructions
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key in (K_s,): #start game
                startScreen = False
            elif event.key in (K_d,): #instructions & credits
                instructions = not instructions


############### GAMEOVER RENDERING #####################

def gameoverMove():
    global startScreen, instructions
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            score.gameOver = False
            startScreen = True
            instructions = False

def drawGameOver():
    surface.blit(gameOverBoard, (200,100))
    raavi = pygame.font.match_font('raavi')
    raaviFont = pygame.font.Font(raavi, 35)
    font = raaviFont.render(str(score.score), True, (255,255,255))
    surface.blit(font, (300, 285))
    score.gameOver = True

############### HERD GAME #####################

def runGame():
    score.gameStartedTime = pygame.time.get_ticks()
    while score.score < score.scoreGoal and not score.gameOver:
        redrawAll()
        getMove(playerObj1)
        if Util.Moving.playerEdgeCheck(playerObj1): #Returns TRUE if not hitting edge of board
            Util.Moving.moveObj(playerObj1)
            playerPickup(playerObj1)
        Util.Moving.checkDirFacing(playerObj1)
        Util.Tossing.inFencePointsCheck(playerObj1, animals, score)
        powerCheck(playerObj1)
        if not playerObj1.invuln: #Only check for crash effect if player is not invulnerable
            Util.Moving.monsterPlayerCrash(monster1, playerObj1, score)
            if playerObj1.invuln: #A crash has occured if invuln. has been switched on. Record that time for future use.
                sfx["hit"].play()
                playerObj1.invulnTime = pygame.time.get_ticks()
        moveAnimals()
        moveMonster(monster1)
        Util.Managing.animalSpawner(animals, pygame.time.get_ticks())
        managePowerUps()
        pygame.display.update()
        fpsClock.tick(FPS)
    if not score.gameOver:
        score.transition = True
        Util.Using.resetFire(weapons)
        playerObj1.invuln = False
        score.gamelvl += 1
        Util.Managing.difficultyUp(monster1, score)
    while score.transition:
        getUpdateMove()
        redrawStatus()
        if score.transition == False:
            #Use set score goals to keep challenge from growing exponentially hard
            try: score.scoreGoal = score.scoreGoals[score.gamelvl]
            #If no more score goals exist, difficulty increases using this equation
            except: score.scoreGoal = int(score.scoreGoal * 1.5)
    Util.Points.setTime(score) #resets time bonus/penalties back to 0
    Util.Moving.moveReset(playerObj1, monster1)

def getUpdateMove():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            pygame.mixer.music.stop()
        elif event.type == KEYDOWN: #Key press
            if event.key in (K_s,):
                if score.selector == "fire": #upgrade fire
                    playerObj1.firelvl += 1
                    Util.Points.upgradeFire(weapons, score)
                score.selector = "fire"
            elif event.key in (K_d,):
                if score.selector == "zap" and playerObj1.zaplvl != 6: #update zap
                    playerObj1.zaplvl += 1
                    Util.Points.upgradeZap(weapons, score)
                score.selector = "zap"
            elif event.key in (K_f,):
                if score.selector == "food" and playerObj1.foodlvl != 5: #upgrade food
                    playerObj1.foodlvl += 1
                    Util.Points.upgradeFood(weapons, score)
                score.selector = "food"
            elif event.key in (K_w,):
                if score.selector == "speed": #upgrade speed
                    playerObj1.speedlvl += 1
                    Util.Points.upgradeSpeed(playerObj1, score)
                score.selector = "speed"
            elif event.key in (K_e,):
                if score.selector == "time": #upgrade starting time
                    playerObj1.timelvl += 1
                    Util.Points.upgradeTime(score)
                score.selector = "time"
            elif event.key in (K_r,):
                if score.selector == "energy": #upgrade staimina
                    playerObj1.staiminalvl += 1
                    Util.Points.upgradeEnergy(playerObj1, score)
                score.selector = "energy"

def redrawStatus():
    pygame.draw.rect(surface, (255,255,255), (200, 150, 500, 400))
    pygame.draw.rect(surface, (0,0,0), (205, 155, 490, 390))
    
    raavi = pygame.font.match_font('raavi')
    raaviTitle = pygame.font.Font(raavi, 35)
    raaviFont = pygame.font.Font(raavi, 16)
    
    surface.blit((raaviTitle.render("LEVEL PASSED!", True, (255,255,255))), (335, 165))
    surface.blit((raaviFont.render("Prepare for the next...double-click a key to upgrade your performance.",
                                   True, (255,255,255))), (225, 210))
    
    surface.blit(weapons.icon_Fire, (230, 250))
    fireFont = "(S) FIREWALL LVL " + str(playerObj1.firelvl) + " | Upgrade to reduce energy cost"
    surface.blit((raaviFont.render(fireFont, True, (255,255,255))), (270, 250))
    
    surface.blit(weapons.icon_Zap, (230, 300))
    zapFont = "(D) ZAP LVL " + str(playerObj1.zaplvl) + "/6 | Upgrade to reduce energy cost"
    surface.blit((raaviFont.render(zapFont, True, (255,255,255))), (270, 300))
    
    surface.blit(weapons.icon_Food, (230, 350))
    foodFont = "(F) FOOD DECOY LVL " + str(playerObj1.foodlvl) + "/5 | Upgrade to reduce energy cost"
    surface.blit((raaviFont.render(foodFont, True, (255,255,255))), (270, 350))
    
    surface.blit(score.icon_Speed, (230, 400))
    speedFont = "(W) SPEED LVL " + str(playerObj1.speedlvl) + " | Upgrade to increase movement speed"
    surface.blit((raaviFont.render(speedFont, True, (255,255,255))), (270, 400))
    
    surface.blit(score.icon_Time, (230, 450))
    timeFont = "(E) TIME LVL " + str(playerObj1.timelvl) + " | Upgrade to increase starting time"
    surface.blit((raaviFont.render(timeFont, True, (255,255,255))), (270, 450))
    
    surface.blit(score.icon_Energy, (230, 500))
    energyFont = "(R) AP LVL " + str(playerObj1.staiminalvl) + " | Upgrade to increase total attack power"
    surface.blit((raaviFont.render(energyFont, True, (255,255,255))), (270, 500))
    
    if score.selector == "fire": pygame.draw.rect(surface, (255,255,255), (210, 250, 10, 10))
    elif score.selector == "zap": pygame.draw.rect(surface, (255,255,255), (210, 300, 10, 10))
    elif score.selector == "food": pygame.draw.rect(surface, (255,255,255), (210, 350, 10, 10))
    elif score.selector == "speed": pygame.draw.rect(surface, (255,255,255), (210, 400, 10, 10))
    elif score.selector == "time": pygame.draw.rect(surface, (255,255,255), (210, 450, 10, 10))
    elif score.selector == "energy": pygame.draw.rect(surface, (255,255,255), (210, 500, 10, 10))

    pygame.display.update()

def getMove(player):
    for event in pygame.event.get():
        #print event
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            pygame.mixer.music.stop()
        elif event.type == KEYDOWN: #Key press
            if event.key in (K_LEFT,): #Move left if click left
                player.facing = "LEFT"
                player.move_left = True
                player.move_right = False
            elif event.key in (K_RIGHT,): #Move right if click right
                player.facing = "RIGHT"
                player.move_right = True
                player.move_left = False
            elif event.key in (K_UP,):
                player.move_up = True
                player.move_down = False
            elif event.key in (K_DOWN,):
                player.move_down = True
                player.move_up = False
            elif event.key in (K_a,):
                #a -> let go of animal you are carrying
                if not player.canAttack:
                    sfx["drop"].play()
                Util.Tossing.letgo_animal(player, animals, score)
            elif event.key in (K_SPACE,):
                #SPACE -> Use powerup
                Util.Using.activatePower(player, monster1)
                sfx["powerup"].play()
                player.startTime = pygame.time.get_ticks() #power activation time
            if event.key in (K_s,):
                #s -> FIRE WALL attack
                if player.canAttack:
                    if not Util.Tossing.infence(player):
                        weapons.fireNum += 1
                        if weapons.fireNum == 1:
                            weapons.usingFire = True
                            sfx["attackFIRE"].play()
                            weapons.fireStartTime = pygame.time.get_ticks()
                            (weapons.firex, weapons.firey) = (player.x, player.y)
            elif event.key in (K_d,):
                #d -> ZAP attack
                if player.canAttack:
                    if not Util.Tossing.infence(player):
                        weapons.usingZap = True
                        sfx["attackZAP"].play()
                        player.startTime = pygame.time.get_ticks()
            elif event.key in (K_f,):
                #f -> FOOD attack
                weapons.usingFood = True
                if player.canAttack:
                    if not Util.Tossing.infence(player):
                        if player.staimina >= weapons.foodCost:
                            weapons.foodNum += 1
                            if weapons.foodNum == 1:
                                sfx["attackFOOD"].play()
                                player.staimina -= weapons.foodCost
                                (weapons.x, weapons.y) = (player.x, player.y)
                        weapons.foodStart = pygame.time.get_ticks()
        elif event.type == KEYUP:
            #player stopped pressing down key. Stop moving now..
            if event.key in (K_LEFT,):
                player.move_left = False
            elif event.key in (K_RIGHT,):
                player.move_right = False
            elif event.key in (K_UP,):
                player.move_up = False
            elif event.key in (K_DOWN,):
                player.move_down = False
            elif event.key in (K_s,):
                weapons.usingFire = False
            elif event.key in (K_d,):
                weapons.usingZap = False
            elif event.key in (K_f,):
                weapons.usingFood = False

def moveAnimals():
    locations = object_creator.Animal.animallocations(animals)
    for animal in animals:
        currentTime = pygame.time.get_ticks()
        if Util.Moving.inDanger(animal, monster1): #Animal in danger! Run away from monster, turn around.
            if Util.Moving.edgeCheck(animal):
                Util.Moving.animalRunAway(animal, monster1)
            if Util.Moving.animalCollision(animal, animals, locations):
                Util.Moving.turnAround(animal)
            Util.Moving.runningCollision_wall(animal)
            Util.Moving.checkDirFacing(animal)
            Util.Moving.moveObj(animal)
        elif (currentTime % animal.wander_time) < 50:
            Util.Moving.getMoveAnimal(animal)
        elif Util.Moving.animalCollision(animal, animals, locations):
            Util.Moving.turnAround(animal)
            Util.Moving.checkDirFacing(animal)
            Util.Moving.moveObj(animal)            
        elif Util.Moving.edgeCheck(animal): #on legal board, just move.
            Util.Moving.checkDirFacing(animal)
            Util.Moving.moveObj(animal)
        else: #TURN AROUND, hit a wall
            Util.Moving.turnAround(animal)
            Util.Moving.checkDirFacing(animal)
            Util.Moving.moveObj(animal)
        manageSprite(animal)

def moveMonster(monster):
    if Util.Moving.monsterEat(monster):
        if type(monster.target) == object_creator.Animal:
            score.timePenalty += 5000
            score.event = "Monster ate animal. You LOST 5 seconds..."
            sfx["monsterEatAnimal"].play()
            animals.remove(monster.target)
        elif type(monster.target) == object_creator.Weapon:
            score.event = "Monster ate your decoy hamburger! nomnomnom"
            sfx["monsterEatFood"].play()
            weapons.foodNum = 0
        monster.target = None #After eating, reset monster's target to None
    else:
        if Util.Moving.edgeCheck(monster):
            if weapons.foodNum >= 1:
                Util.Moving.monsterLocateFood(monster, weapons)
            else:
                Util.Moving.monsterLocateClosest(monster, animals)
            Util.Moving.getMoveMonster(monster, animals)
            Util.Moving.checkDirFacing(monster)
            Util.Moving.monsterEdgeBump(monster)
            if monster.speed == 0: #If monster is frozen, allow that effect to stay
                pass
            elif Util.Using.fireSense(weapons, monster) and (weapons.fireNum > 0):
                #Check if monster is in the fire wall area, if true, then slow it down.
                monster.speed = monster.slowSpeed
            else:
                monster.speed = monster.speedStore
            Util.Moving.moveObj(monster)


#IF emptyhands..Senses when player is close enough to interactable object to pick it up
def playerPickup(player):
    for animal in animals:
        sameX = False
        sameY = False
        if (player.x > animal.x-25) and (player.x < animal.x+25):
            sameX = True
        if (player.y > animal.y-25) and (player.y < animal.y+25):
            sameY = True
        if sameX and sameY:
            if Util.Tossing.emptyHands_animal(player):
                Util.Tossing.pickup_animal(player, animal)
                sfx["pickup"].play()
                #SPECIAL CASE: When player picks up last animal, monster needs to correctly target "NONE" instead.
                Util.Tossing.targetCheck(monster1, animal, animals)
                animals.remove(animal) #Remove animal from larger list, b/c now animal is held by player
    for powerup in powerUps:
        if powerup.scaler >= 25: #Finizhed spawning to full size, can pick up
            sameX = False
            sameY = False
            if (player.x > powerup.x-20) and (player.x < powerup.x+20):
                sameX = True
            if (player.y > powerup.y-20) and (player.y < powerup.y+20):
                sameY = True
            if sameX and sameY:
                if not Util.Tossing.fullpowerups(player):
                    Util.Tossing.pickup_powerUp(player, powerup)
                    powerUps.remove(powerup) #Remove powerup from list b/c powerup is held by player
    
#Can manage switching out images for objects for basic sprite animation!
def manageSprite(thing):
    currentTime = pygame.time.get_ticks()
    if (thing.move_up == False) and (thing.move_left == False) and (thing.move_down == False) and (thing.move_right == False):
        #not moving, idle animation.
        Util.Sprite.spriteIdle(thing, currentTime)
    else:
        Util.Sprite.spriteRun(thing, currentTime)

def manageInvuln(player):
    currentTime = pygame.time.get_ticks()
    activeTime = currentTime - player.invulnTime #Time invulnerability has lasted so far
    if (activeTime > 1900) and (activeTime < 2000): #invulnerablity lasts ~2 seconds
        player.invuln = False

#Used to spawn powerups on board and remove them if not picked up
def managePowerUps():
    posPowers = ["SPEED", "FREEZE"]
    currentTime = pygame.time.get_ticks()
    #print "TIME=", currentTime
    #LATER: make spawnrate depend on difficulty
    spawnRate = 2600 #Milliseconds
    existTime = spawnRate + 5100
    if len(powerUps) == 0:
        if (currentTime % spawnRate) < 100:
            powerType = random.choice(posPowers)
            powerup1 = object_creator.Powerups(powerType)
            powerUps.append(powerup1)
    elif len(powerUps) == 1:
        if (currentTime % existTime) < 100:
            powerUps.pop(0)

#IF player has active power, keep track of how long power has been active.
#Deactivates once power has been active for ~5 seconds
def powerCheck(player):
    currentTime = pygame.time.get_ticks()
    activeTime = currentTime - player.startTime #Time power has been activated so far
    if (activeTime > 4900) and (activeTime < 5000): #power lasts ~5 seconds
        Util.Using.deactivatePower(player, monster1)

# Fill up animal list with fresh batch of animals
def spawnAnimals():
    global animals
    animals = [] #reset to empty in order to RESPAWN animals
    #Later make it depend on game's level / difficulty.
    numAnimals = 5
    for num in xrange(numAnimals):
        animal = object_creator.Animal()
        animals.append(animal) #add animal object onto list animals

def drawPowerups():
    for index in xrange(len(powerUps)):
        power = powerUps[index]
        if power.scaler < 25:
            power.scaler += 1
            power.rescaler()
        surface.blit(power.image, (power.x, power.y))

def powerupDisplay():
    x = 750
    y = 28
    bcolor = (67,67,67)
    pygame.draw.rect(surface, bcolor, (650, 20, 130, 40))
    pygame.draw.rect(surface, (100,100,100), (745, 20, 35, 40))
    raavi = pygame.font.match_font('raavi')
    raaviFont = pygame.font.Font(raavi, 14)
    powerupFont = raaviFont.render("Powerups:", True, (255,255,255))
    surface.blit(powerupFont, (648, 2))
    for powerup in playerObj1.holding_powerUps:
        surface.blit(powerup.image, (x, y))
        x -= 30

def playerStatDisplay():
    #Draw staimina bar and outline!
    bcolor = (67,67,67)
    pygame.draw.rect(surface, bcolor, (10, 181, 125, 13))
    pygame.draw.rect(surface, bcolor, (5, 176, 5, 30))
    pygame.draw.rect(surface, bcolor, (135, 176, 5, 30))
    
    raavi = pygame.font.match_font('raavi')
    raaviFont = pygame.font.Font(raavi, 14)
    fontStaimina = raaviFont.render("Attack power", True, bcolor)
    surface.blit(fontStaimina, (40, 190))
    
    #Manage constant regernation of staimina over time
    currentTime = pygame.time.get_ticks()
    if (currentTime % 500 < 15):
        playerObj1.staimina += 2
    if playerObj1.staimina > 100:
        playerObj1.staimina = 100
    
    staiminaRatio = playerObj1.staimina / 100.0
    greenVar = int(255 * staiminaRatio)
    redVar = int(255 * (1-staiminaRatio))
    color = (redVar, greenVar, 0)
    width = 125 * staiminaRatio
    pygame.draw.rect(surface, color, (10, 185, width, 5))
    
    #Draw Attack icons, levels, and other stats
    fontAttack = raaviFont.render("Player Stats:", True, (255,255,255))
    strSpeed = "Speed = " + str(playerObj1.speed)
    fontSpeed = raaviFont.render(strSpeed, True, (255,255,255))
    surface.blit(fontAttack, (10, 75))
    surface.blit(fontSpeed, (40, 95))
    
    surface.blit(weapons.icon_Fire, (20, 120))
    surface.blit(weapons.icon_Zap, (60, 120))
    surface.blit(weapons.icon_Food, (100,120))
    
    fireLvl = raaviFont.render(str(playerObj1.firelvl), True, (255,255,255))
    zapLvl = raaviFont.render(str(playerObj1.zaplvl), True, (255,255,255))
    foodLvl = raaviFont.render(str(playerObj1.foodlvl), True, (255,255,255))
    surface.blit(fireLvl, (20, 145))
    surface.blit(zapLvl, (60, 145))
    surface.blit(foodLvl, (100, 145))

def timerDisplay():
    #Draw the border around the timer
    bcolor = (67,67,67)
    pygame.draw.rect(surface, bcolor, (225, 25, 400, 24))
    pygame.draw.rect(surface, bcolor, (220, 20, 5, 35))
    pygame.draw.rect(surface, bcolor, (625, 20, 5, 35))
    
    #Draw the timer
    #Will record how long each "game" / level lasts!
    score.timeRun = pygame.time.get_ticks() - score.gameStartedTime
    timePassed = score.initTime - score.timeRun #Starting time minus time game has run on for
    score.time = timePassed + score.timeBonus - score.timePenalty #Time left is time passed plus any bonuses earned, minus penalty
    if score.time > score.initTime: #If bonus pushes beyond timer allowance, DON'T let it extend beyond
        score.time = score.initTime
        #NOTE: HERE would be the place to add bonus points for this occurance!
    timeRatio = float(score.time) / float(score.initTime)
    width = 400 * timeRatio
    greenVar = int(255 * timeRatio)
    redVar = int(255 * (1-timeRatio))
    #Prevent color crashes
    if redVar >= 255: redVar = 255
    if greenVar <= 0: greenVar = 0
    color = (redVar, greenVar, 0)
    pygame.draw.rect(surface, color, (225, 30, width, 13))
    
    raavi = pygame.font.match_font('raavi')
    raaviFont = pygame.font.Font(raavi, 14)
    fontTime = raaviFont.render("Time:", True, (255,255,255))
    surface.blit(fontTime, (218, 2))

#White text underneath timer - description of events!
def eventDisplay():
    raavi = pygame.font.match_font('raavi')
    raaviFont = pygame.font.Font(raavi, 14)
    if score.event == "Monster Player Collision":
        font = raaviFont.render("OUCH! The monster stole some of your power and time.", True, (255,255,255))
    elif score.event == "Cow points":
        font = raaviFont.render("Moooo~ You saved a cow! +20 power | +3s bonus time!", True, (255,255,255))
    elif score.event == "Monster ate animal":
        font = raaviFont.render("Uhoh, the monster ate an animal.", True, (255,255,255))
    else:
        font = raaviFont.render("Hurry and save the animals!", True, (255,255,255))
    surface.blit(font, (230,50))

#Displays useful information about stuff picked up!
def handDisplay():
    raavi = pygame.font.match_font('raavi')
    raaviFont = pygame.font.Font(raavi, 14)
    pygame.draw.circle(surface, (67,67,67), (75, 525), 50)
    if playerObj1.holding_animal != "NONE":
        image = playerObj1.holding_animal.current_image
        surface.blit(image, (55, 502))
        font = raaviFont.render("Effects: Mooo", True, (255,255,255))
        handsFont = raaviFont.render("Holding: Cow", True, (255,255,255))
    else:
        handsFont = raaviFont.render("Holding: Nothing.", True, (255,255,255))
        font = raaviFont.render("Effects: NONE", True, (255,255,255))
    surface.blit(font, (10,580))
    surface.blit(handsFont, (10,455))

def drawAnimals():
    for index in xrange(len(animals)):
        curanimal = animals[index]
        manageInvuln(curanimal)
        currentTime = pygame.time.get_ticks()
        if curanimal.invuln: #Give animal invulnerability flashing effect
            delay = 25
            if (currentTime / delay) % 2 == 0:
                surface.blit(curanimal.current_image, (curanimal.x, curanimal.y))
        else:
            surface.blit(curanimal.current_image, (curanimal.x, curanimal.y))

def drawScore():
    black = (0,0,0)
    yellow = (255, 255, 0)
    orange = (255, 128, 0)
    raavi = pygame.font.match_font('raavi')
    raaviFont = pygame.font.Font(raavi, 35)
    raaviFont2 = pygame.font.Font(raavi, 14)
    
    #convert score variables into text-able strings
    curscore = str(score.score)
    goalScore = str(score.scoreGoal)
    
    #Create font objects for drawing
    wordScore = raaviFont2.render("Score:", True, yellow)
    slash = raaviFont.render("/", True, orange)
    playerscore = raaviFont.render(curscore, True, yellow)
    goalscore = raaviFont.render(goalScore, True, orange)
    surface.blit(wordScore, (10,3))
    surface.blit(slash, (100, 13))
    surface.blit(playerscore, (10, 15))
    surface.blit(goalscore, (120, 15))
    
def drawPlayer():
    manageSprite(playerObj1)
    manageInvuln(playerObj1)
    currentTime = pygame.time.get_ticks()
    if playerObj1.invuln:
        delay = 50
        if (currentTime / delay) % 2 == 0:
            surface.blit(playerObj1.current_image, (playerObj1.x, playerObj1.y))
    else:
        surface.blit(playerObj1.current_image, (playerObj1.x, playerObj1.y))
    if playerObj1.holding_animal != "NONE": #if player is holding animal, draw animal
        heldAnimal = playerObj1.holding_animal
        surface.blit(heldAnimal.current_image, (playerObj1.x+5, playerObj1.y+5))

def drawMonster():
    manageSprite(monster1)
    if monster1.speed == 0:
        if monster1.facing == "LEFT":
            monster1.current_image = monster1.l_freeze
        else:
            monster1.current_image = monster1.r_freeze
    surface.blit(monster1.current_image, (monster1.x, monster1.y))

def drawAttack():
    Util.Using.attack(playerObj1, weapons, monster1, surface)
    Util.Using.foodDraw(weapons, surface)
    Util.Using.drawFire(surface, playerObj1, weapons)
    Util.Using.fireTimeCheck(weapons, pygame.time.get_ticks())

def drawHelp():
    currentTime = pygame.time.get_ticks()
    #Display arrow help when holding animal AND for game levels 1, 2, and 3
    if not (Util.Tossing.emptyHands_animal(playerObj1)) and (score.gamelvl <= 2):
        Util.Sprite.arrowSprite(score, currentTime)
        surface.blit(score.arrowImg, (150,300))

#Display changing tips for game levels 1, 2, 3, 4
def drawTip():
    currentTime = pygame.time.get_ticks()
    existTime = 7000
    if score.gamelvl <= 3:
        if not (Util.Tossing.emptyHands_animal(playerObj1)) and (score.gamelvl < 1):
            #For level 1, display warning when holding animal
            score.curTip = 7
        elif (currentTime % existTime) < 30:
            score.curTip += 1
            score.curTip = score.curTip % 7
        surface.blit(score.tipImgs[score.curTip], (150, 75))

def drawBoard():
    field = pygame.image.load(os.path.join("images", "board.gif"))
    safeZone = pygame.image.load(os.path.join("images", "SafeZone.gif"))
    surface.blit(field, (0,0))
    surface.blit(safeZone, (0,225))

def redrawAll():
    drawBoard()
    drawHelp()
    drawAttack()
    pygame.draw.rect(surface, (0,0,0), (0, 0, 800, 75)) #score area
    pygame.draw.rect(surface, (0,0,0), (0, 75, 150, 150)) #Attack area
    pygame.draw.rect(surface, (0,0,0), (0, 450, 150, 150)) #Hands area
    drawPlayer()
    drawMonster()
    drawPowerups()
    drawAnimals()
    drawTip()
    drawScore()
    eventDisplay()
    handDisplay()
    powerupDisplay()
    playerStatDisplay()
    timerDisplay()
    if score.time < 0: drawGameOver()

run()
