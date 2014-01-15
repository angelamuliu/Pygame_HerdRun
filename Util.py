
# Set of utility functions for modifying objects, keeping track, etc

"""
CONTENTS:
    > Tossing - Functions involved in picking up/letting go
    > Moving - Functions involved in moving player/animal/monster
    > Managing - Keep track of misc. topics
    > Using - Functions involved in player activating powers
    > Sprite - Functions involved in managing sprite animation on top of movement
    > Points - Keep track of score, penalties, time, and more
"""

import pygame, random, sys, os
from pygame.locals import *
import object_creator

class Tossing(object):
    
    # Makes player pick up a thing (ANIMALS AND BOMBS ONLY)
    @classmethod
    def pickup_animal(klass, player, animal):
        if Tossing.emptyHands_animal(player):
            player.holding_animal = animal
            player.canAttack = False
            #print player.holding_animal
    
    # Makes player let go of a thing
    @classmethod
    def letgo_animal(klass, player, animals, score):
        Tossing.inFencePointsCheck(player, animals, score) #First check if points can be made
        if not Tossing.emptyHands_animal(player): #only drop animal if holding in first place
            if player.facing == "RIGHT":
                player.holding_animal.x = player.x - 40
            else:
                player.holding_animal.x = player.x + 40
            player.holding_animal.y = player.y
            animals.append(player.holding_animal) #add back to animal list
            player.holding_animal = "NONE"
            player.canAttack = True
    
    #Automatically gives point if player has cow and is in fence
    @classmethod
    def inFencePointsCheck(klass, player, animals, score):
        if not Tossing.emptyHands_animal(player):
            if Tossing.infence(player):
                score.score += 5
                score.timeBonus += 3000 #Every animal gives you a 3 second time extension
                player.staimina += 20 #Staimina boost bonus as well!
                score.event = "Cow points"
                if player.staimina > 100: player.staimina = 100
                player.holding_animal = "NONE"
                player.canAttack = True
    
    #Prevents crashing when player picks up last animal, which is monster's target.
    @classmethod
    def targetCheck(klass, monster, animal, animals):
        if monster.target == animal:
            if len(animals) == 0:
                monster.target = None
    
    #Returns true if player is in fence area
    @classmethod
    def infence(klass, player):
        if (player.x > 0) and (player.x < 150) and (player.y > 225) and (player.y + player.size < 450):
            return True
        else:
            return False
    
    #Used to check if player has empty hands -> if so, CAN pick something up.
    @classmethod
    def emptyHands_animal(klass, player):
        if player.holding_animal == "NONE":
            #empty hands!
            return True
        else:
            #holding something..
            return False
    
    #checks if player has max num of powerups. Returns true if "full!"
    @classmethod
    def fullpowerups(klass, player):
        if len(player.holding_powerUps) == 3:
            return True
        return False
    
    #Makes player pick up a powerup
    @classmethod
    def pickup_powerUp(klass, player, powerup):
        if not Tossing.fullpowerups(player):
            #Only pick up powerup if "bag" not full
            player.holding_powerUps.append(powerup)
            #print player.holding_powerUps


class Moving(object):
    
    #Chooses random direction of movement for an animal
    @classmethod
    def getMoveAnimal(klass, animal):
        horizposMoves = ["L", "R", "NONE"]
        vertposMoves = ["U", "D", "NONE"]
        horizmove = random.choice(horizposMoves)
        vertmove = random.choice(vertposMoves)
        if horizmove == "L":
            animal.move_left = True
            animal.move_right = False
            animal.facing = "LEFT"
        elif horizmove == "R":
            animal.move_right = True
            animal.move_left = False
            animal.facing = "RIGHT"
        else:
            animal.move_left = False
            animal.move_right = False
        if vertmove == "U":
            animal.move_up = True
            animal.move_down = False
        elif vertmove == "D":
            animal.move_down = True
            animal.move_up = False
        else:
            animal.move_up = False
            animal.move_down = False
    
    #Calculates monster's "dangerzone" for animals to run from, and whether SINGLE animal is in it
    @classmethod
    def inDanger(klass, animal, monster):
        animal_centerx = animal.x + (animal.size/2)
        animal_centery = animal.y + (animal.size/2)
        monster_centerx = monster.x + (monster.size/2)
        monster_centery = monster.y + (monster.size/2)
        #Now calculate the danger zone of the monster
        danger_leftx = monster_centerx - 100
        danger_lefty = monster_centery - 100
        danger_rightx = monster_centerx + 100
        danger_righty = monster_centery + 100
        if (animal_centerx > danger_leftx) and (animal_centery > danger_lefty):
            if (animal_centerx < danger_rightx) and (animal_centery < danger_righty):
                return True
        return False
    
    #Different move method if animal is RUNNING FOR DEAR LIFE.
    @classmethod
    def animalRunAway(klass, animal, monster):
        animal.move_left = monster.move_left
        animal.move_right = monster.move_right
        animal.move_up = monster.move_up
        animal.move_down = monster.move_down
    
    #When animal hits wall OR another animal while running, will switch directions (no bouncing in opp. dir)
    @classmethod
    def runningCollision_wall(klass, animal):
        if animal.x == 1: #hit left edge
            animal.move_left = False
            animal.move_up = True
            animal.move_down = False
        if animal.y == 51: #hit top edge
            animal.move_up = False
            animal.move_left = True
            animal.move_right = False
            animal.facing = "LEFT"
        if animal.x == 800 - animal.size - 1: #hit right edge
            animal.move_right = False
            animal.move_down = True
            animal.move_up = False
        if animal.y == 600 - animal.size - 1: #hit bottom edge
            animal.move_down = False
            animal.move_right = True
            animal.move_left = False
            animal.facing = "RIGHT"

    @classmethod
    def getMoveMonster(klass, monster, animals):
        if monster.targetdist_x > 0:
            monster.move_left = True
            monster.move_right = False
            monster.facing = "LEFT"
        elif monster.targetdist_x < 0:
            monster.move_right = True
            monster.move_left = False
            monster.facing = "RIGHT"
        else:
            monster.move_left = False
            monster.move_right = False
        if monster.targetdist_y > 0:
            monster.move_up = True
            monster.move_down = False
        elif monster.targetdist_y < 0:
            monster.move_down = True
            monster.move_up = False
        else:
            monster.move_up = False
            monster.move_down = False
    
    @classmethod
    #Used to calculate distance from given monster and an animal! Resets monster's target to closet animal
    def monsterLocateClosest(klass, monster, animals):
        closest = 10000000000 #Initially set closest to huge value b/c target = smallest close value
        for animal in animals:
            xdist = abs(monster.x - animal.x)
            ydist = abs(monster.y - animal.y)
            distance = ( xdist**2 + ydist**2 ) ** 0.5
            if distance < closest:
                closest = distance
                monster.target = animal
                monster.targetdist_x = monster.x - animal.x
                monster.targetdist_y = monster.y - animal.y
    
    #Used to calculate distance from monster and FOOD.
    @classmethod
    def monsterLocateFood(klass, monster, weapon):
        xdist = abs(monster.x - weapon.x)
        ydist = abs(monster.y - weapon.y)
        monster.target = weapon
        monster.targetdist_x = monster.x - weapon.x
        monster.targetdist_y = monster.y - weapon.y
    
    #Manages monster/player crashes and its penalties!
    @classmethod
    def monsterPlayerCrash(klass, monster, player, score):
        (m_topleft, m_botright) = ((monster.x, monster.y), (monster.x+monster.size, monster.y+monster.size))
        (p_topleft, p_botright) = ((player.x, player.y), (player.x+player.size, player.y+player.size))
        inCol = False
        inRow = False
        if (m_topleft[0] > p_topleft[0]) and (m_topleft[0] < p_botright[0]):
            inCol = True
        if (m_botright[0] > p_topleft[0]) and (m_botright[0] < p_botright[0]):
            inCol = True
        if (m_topleft[1] > p_topleft[1]) and (m_topleft[1] < p_botright[1]):
            inRow = True
        if (m_botright[1] > p_topleft[1]) and (m_botright[1] < p_botright[1]):
            inRow = True
        if inCol and inRow:
            #IF player and monster ARE IN FACT crashing into each other...extract a penalty
            Points.crashPenalty(monster, player, score)
    
    #Check if monster ate it's target! True if ate something.
    @classmethod
    def monsterEat(klass, monster):
        if monster.target == None:
            return False
        elif (type(monster.target) == object_creator.Animal) and monster.target.invuln:
            return False
        elif (monster.x > monster.target.x-15) and (monster.x < monster.target.x+15):
            if (monster.y > monster.target.y-15) and (monster.y < monster.target.y+15):
                return True
            else:
                return False
        else:
            return False
    
    #Given certain animal and location list, checks if collision has occured.
    #Returns true when a collision happens
    @classmethod
    def animalCollision(klass, animal, animals, locations):
        try:
            animal_index = animals.index(animal)
            (topleft, botright) = locations[animal_index] #topleft / botright = (x, y)
            #Make a new list of locations that DO NOT include the animal we are evaluating!
            otheranimal_locations = locations[0:animal_index] + locations[animal_index+1:]
        except:
            (topleft, botright) = ((animal.x, animal.y),(animal.x+40, animal.y+40))
            otheranimal_locations = locations
        #We'll be checking to see if a neighbor lies in the same col / row. If both true, collision occured!
        for loc in xrange(len(otheranimal_locations)):
            inCol = False
            inRow = False
            (other_topleft, other_botright) = otheranimal_locations[loc]
            if (other_topleft[0] > topleft[0]) and (other_topleft[0] < botright[0]):
                inCol = True
            if (other_botright[0] > topleft[0]) and (other_botright[0] < botright[0]):
                inCol = True
            if (other_topleft[1] > topleft[1]) and (other_topleft[1] < botright[1]):
                inRow = True
            if (other_botright[1] > topleft[1]) and (other_botright[1] < botright[1]):
                inRow = True
            if inCol and inRow:
                return True #Neighbor in BOTH same row and col -> Collision!
        return False
    
    @classmethod
    def moveObj(klass, player):
        if player.move_left:
            player.x -= player.speed
        if player.move_right:
            player.x += player.speed
        if player.move_up:
            player.y -= player.speed
        if player.move_down:
            player.y += player.speed
    
    @classmethod
    def checkDirFacing(klass, player):
        if player.facing == "RIGHT":
            player.current_image = player.r_image
        elif player.facing == "LEFT":
            player.current_image = player.l_image

    #Used to switch directions of one of wandering things
    @classmethod
    def turnAround(klass, thing):
        if thing.move_left:
            thing.move_left = False
            thing.move_right = True
            thing.facing = "LEFT"
        elif thing.move_right:
            thing.move_left = True
            thing.move_right = False
            thing.facing = "RIGHT"
        if thing.move_up:
            thing.move_up = False
            thing.move_down = True
        elif thing.move_down:
            thing.move_up = True
            thing.move_down = False

    #Players can move a little more than others (i.e. pen)
    @classmethod
    def playerEdgeCheck(klass, player):
        leftx = player.x
        lefty = player.y
        rightx = player.x + player.size
        righty = player.y + player.size
        if (leftx < 150): #Fence edge check
            if leftx > 0:
                if (lefty >= 225) and (righty <= 450): #Fence entrance
                    return True
                else:
                    if lefty < 75: #Corner left check
                        player.x = 151
                        player.y = 76
                        return False
                    elif righty > 600: #Corner right check
                        player.x = 151
                        player.y = 549
                        return False
                    elif lefty > 75 and righty < 225: #Top UI block check
                        player.x = 151
                        return False
                    elif lefty > 450 and righty < 600: #Bottom UI block check
                        player.x = 151
                        return False
                    elif lefty < 225: #Inside fence top check
                        player.y = 226
                        return False
                    elif righty > 450: #Inside fence bottom check
                        player.y = 399
                        return False
            else:
                player.x = 1
                return False
        else: #General edge check
            if leftx < 150:
                player.x = 151
                return False
            if lefty < 75:
                player.y = 76
                return False
            if rightx > 800:
                player.x = 800 - player.size - 1
                return False
            if righty > 600:
                player.y = 600 - player.size - 1
                return False
            return True

    #Checks if player is going off the edge
    #Returns true if still on legal board
    @classmethod
    def edgeCheck(klass, player):
        #Playing on a 800x600 px board.
        leftx = player.x
        lefty = player.y
        rightx = player.x + player.size
        righty = player.y + player.size
        onBoard = True
        #If goes off edge, reset value to 1 before that for a 'crashing' effect!
        if leftx < 150:
            player.x = 151
            onBoard = False
        if lefty < 75:
            player.y = 76
            onBoard = False
        if rightx > 800:
            player.x = 800 - player.size - 1
            onBoard = False
        if righty > 600:
            player.y = 600 - player.size - 1
            onBoard = False
        if onBoard: return True
        else: return False
    
    #Prevents monster edge bumping too much when chasing targets
    @classmethod
    def monsterEdgeBump(klass, monster):
        if monster.y + monster.size >= 599: #hit bottom edge
            monster.move_down = False
        if monster.y <= 51: #hit top edge
            monster.move_up = False
        if monster.x <= 151: #hit left edge
            monster.move_left = False
        if monster.x + monster.size >= 799: #hit right edge
            monster.move_right = False
    
    #Resets movement to NOT MOVING and negates any carryover frozen effects
    @classmethod
    def moveReset(klass, player, monster):
        player.move_left = False
        player.move_right = False
        player.move_down = False
        player.move_up = False
        monster.speed = monster.speedStore


class Managing(object):
    
    #Checks number of animals and spawns one animal if not correct amount.
    @classmethod
    def animalSpawner(klass, animals, time):
        while len(animals) < 5:
            locations = object_creator.Animal.animallocations(animals)
            animal = object_creator.Animal()
            animal.x = random.randint(200, 750)
            animal.y = random.randint(100, 550)
            print animal.x, animal.y
            if not Moving.animalCollision(animal, animals, locations):
                #You want to only append animal IF they are NOT colliding
                animals.append(animal)
            #animal.invulnTime = time
            #animal.invuln = True
    
    #levels up difficulty of game accordingly
    @classmethod
    def difficultyUp(klass, monster, score):
        monster.speed += .2
        monster.slowSpeed = monster.speed / 2.5
        monster.speedStore += .2
        monster.eatPower += 3
        monster.eatTime += 200


class Using(object):
    
    @classmethod
    def activatePower(klass, player, monster):
        if len(player.holding_powerUps) > 0:
            powerupObj = player.holding_powerUps.pop(0)
            powerType = powerupObj.power
            if powerType == "SPEED":
                player.speedStore = player.speed
                player.speed += 5
            elif powerType == "FREEZE":
                monster.speed = 0
                #NOTE: ADD CHANGING MONSTER IMAGE HERE WHEN FROZEN LATER.

    #resets values to default
    @classmethod
    def deactivatePower(klass, player, monster):
        player.speed = player.speedStore
        monster.speed = monster.speedStore
    
    #A check for what weapon used, and activate it
    @classmethod
    def attack(klass, player, weapon, monster, surface):
        if not Tossing.infence(player): #can't attack IF in fence area.
            if player.canAttack:
                if weapon.usingZap:
                    Using.zapAttack(player, weapon, monster, surface)
                elif weapon.usingFire:
                    Using.fireAttack(player, weapon, monster, surface)
                elif weapon.usingFood:
                    Using.foodDraw(weapon, surface)
    
    #Draws food IN ONE PLACE on board until food is eaten or gone.
    @classmethod
    def foodDraw(klass, weapon, surface):
        if weapon.foodNum >= 1:
            surface.blit(weapon.board_Food, (weapon.x, weapon.y))
    
    #Uses fire wall attack!
    @classmethod
    def fireAttack(klass, player, weapon, monster, surface):
        fireCost = weapon.fireCost
        if player.staimina >= fireCost:
            player.staimina -= fireCost
            Using.drawFire(surface, player, weapon)
    
    #draws graphics for the fire wall attack
    @classmethod
    def drawFire(klass, surface, player, weapon):
        if weapon.fireNum >=1:
            attackRect = (weapon.firex-75, weapon.firey-75, 200, 200)
            surface.blit(weapon.board_Fire, (weapon.firex-75, weapon.firey-75))
    
    #senses if monster is in fire wall attack and slows down accordingly
    @classmethod
    def fireSense(klass, weapon, monster):
        fire_leftx = weapon.firex - 75
        fire_lefty = weapon.firey - 75
        inCol = False
        inRow = False
        if (monster.x > fire_leftx) and (monster.x < fire_leftx+200):
            inCol = True
        if (monster.x+monster.size> fire_leftx) and (monster.x+monster.size < fire_leftx+200):
            inCol = True
        if (monster.y > fire_lefty) and (monster.y < fire_lefty+200):
            inRow = True
        if (monster.y+monster.size > fire_lefty) and (monster.y+monster.size < fire_lefty+200):
            inRow = True
        if inCol and inRow:
            return True
    
    #Removes the fire wall once a certain period of time has passed
    @classmethod
    def fireTimeCheck(klass, weapon, curtime):
        activeTime = curtime - weapon.fireStartTime
        if (activeTime > 5900) and (activeTime < 6000): #power lasts ~6 seconds
            Using.resetFire(weapon)
    
    @classmethod
    def resetFire(klass, weapon):
        weapon.fireNum = 0
        weapon.usingFire = False
        weapon.firex = 0
        weapon.firey = 0
    
    #Uses thunder attack!
    @classmethod
    def zapAttack(klass, player, weapon, monster, surface):
        zapCost = weapon.zapCost
        if player.staimina >= zapCost:
            player.staimina -= zapCost
            Using.drawZap(surface, player, monster)
    
    #Draw the graphics of the zap thunder attack
    @classmethod
    def drawZap(klass, surface, player, monster):
        colors = [(198,226,255), (28,134,238), (99,184,255), (58,95,205), (176,196,222)]
        color = random.choice(colors)
        attackRect = (0,0,0,0)
        if player.move_down:
            attackRect = (player.x, player.y+player.size, player.size, 600-player.y)
        elif player.move_up:
            attackRect = (player.x, 75, player.size, player.y-75)
        elif player.move_right:
            attackRect = (player.x+player.size, player.y, 800-player.x, player.size)
        elif player.move_left:
            attackRect = (150, player.y, player.x-150, player.size)
        else:
            attackRect = (player.x-75, player.y-75, 200, 200)
        pygame.draw.rect(surface, color, attackRect)
        Using.senseZap(monster, attackRect)
    
    #Senses collision of zap thunder attack for monster
    @classmethod
    def senseZap(klass, monster, attackRect):
        inCol = False
        inRow = False
        if (monster.x > attackRect[0]) and (monster.x < attackRect[0]+attackRect[2]):
            inCol = True
        if (monster.x+monster.size> attackRect[0]) and (monster.x+monster.size < attackRect[0]+attackRect[2]):
            inCol = True
        if (monster.y > attackRect[1]) and (monster.y < attackRect[1]+attackRect[3]):
            inRow = True
        if (monster.y+monster.size > attackRect[1]) and (monster.y+monster.size < attackRect[1]+attackRect[3]):
            inRow = True
        if inCol and inRow:
            monster.speed = 0


class Sprite(object):

    #Image management for when object is not moving
    @classmethod
    def spriteIdle(klass, thing, curtime):
        delay = thing.sprite_delay
        if (curtime / delay) % 2 == 0: #If divide by delay is even, switch to idle image 2
            if thing.facing == "RIGHT":
                thing.current_image = thing.r_idle
            else:
                thing.current_image = thing.l_idle
        else:
            if thing.facing == "RIGHT":
                thing.current_image = thing.r_image
            else:
                thing.current_image = thing.l_image
    
    #Image management for when object is moving
    @classmethod
    def spriteRun(klass, thing, curtime):
        delay = thing.sprite_delay
        if (curtime / delay) % 2 == 0: #If divide by delay is even, switch to idle image 2
            if thing.facing == "RIGHT":
                thing.current_image = thing.r_run
            else:
                thing.current_image = thing.l_run
        else:
            if thing.facing == "RIGHT":
                thing.current_image = thing.r_image
            else:
                thing.current_image = thing.l_image
    
    #Image management for point help arrow
    @classmethod
    def arrowSprite(klass, score, curtime):
        delay = score.arrowDelay
        if (curtime / delay) % 2 == 0:
            score.arrowImg = score.helpArrow1
        else:
            score.arrowImg = score.helpArrow2


class Points(object):
    
    #Resets time to FULL AMOUNT
    @classmethod
    def setTime(klass, score):
        score.timeBonus = 0
        score.timePenalty = 0
    
    #When crash occurs, reduce staimina by a certain amount AS WELL as time, and set invincibility
    @classmethod
    def crashPenalty(klass, monster, player, score):
        score.timePenalty += monster.eatTime #Lose 3 seconds of time.
        score.event = "Monster Player Collision"
        player.staimina -= monster.eatPower #Player losses attack energy for bumping into monster
        if player.staimina < 0:
            player.staimina = 0 #Can't let it become negative.
        player.invuln = True
    
    #upgrades fire attack
    @classmethod
    def upgradeFire(klass, weapon, score):
        score.transition = False
    
    #upgrades zap attack
    @classmethod
    def upgradeZap(klass, weapon, score):
        if weapon.zapCost != 1:
            weapon.zapCost -= 1
        score.transition = False
    
    #upgrades food attack
    @classmethod
    def upgradeFood(klass, weapon, score):
        if weapon.foodCost != 10:
            weapon.foodCost -= 10
        score.transition = False
    
    #upgrades speed
    @classmethod
    def upgradeSpeed(klass, player, score):
        player.speed += 1
        player.speedStore += 1
        score.transition = False
    
    #upgrades starting time
    @classmethod
    def upgradeTime(klass, score):
        score.initTime += 7000
        score.transition = False
    
    #upgrades total staimina
    @classmethod
    def upgradeEnergy(klass, player, score):
        player.staimina += 5
        score.transition = False
    