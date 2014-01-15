
# Initializes active objects and information stored inside

"""
CONTENTS:
    >Player
    >Animal
    >Monster
    >Powerups - Speed & Freeze powerups
    >Score - Player game score, tip/help images, and game checks
    >Weapon - Attack graphics, checks, and costs
"""

import pygame, random, sys, os
from pygame.locals import *

class Player(object):
    def __init__(self):
        l_herderIDLE1 = pygame.image.load(os.path.join("images", "herder_idle.png"))
        r_herderIDLE1 = pygame.transform.flip(l_herderIDLE1, True, False)
        
        l_herderIDLE2 = pygame.image.load(os.path.join("images", "herder_idle2.png"))
        r_herderIDLE2 = pygame.transform.flip(l_herderIDLE2, True, False)
        
        l_herderRUN = pygame.image.load(os.path.join("images", "herder_run.png"))
        r_herderRUN = pygame.transform.flip(l_herderRUN, True, False)
        
        self.facing = "RIGHT"
        self.current_image = r_herderIDLE1
        self.size = 50
        
        self.r_image = r_herderIDLE1
        self.l_image = l_herderIDLE1
        
        self.r_idle = r_herderIDLE2
        self.l_idle = l_herderIDLE2
        self.r_run = r_herderRUN
        self.l_run = l_herderRUN
        self.sprite_delay = 300 #300 ms between sprite images
        
        self.x = 200
        self.y = 250
        
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        
        self.speed = 5
        self.speedStore = 5
        self.holding_animal = "NONE"
        self.holding_powerUps = [ ]
        self.canAttack = True
        self.startTime = 0 #Later keeps track of start time of activation of powerup
        
        self.staimina = 100
        self.invuln = False
        self.invulnTime = 0 #Keeps track of start time of activation of invulnerability
        
        self.firelvl = 1
        self.zaplvl = 1
        self.foodlvl = 1
        self.speedlvl = 1
        self.timelvl = 1
        self.staiminalvl = 1


class Animal(object):
    animalList = []

    def __init__(self):
        l_animal_img = pygame.image.load(os.path.join("images", "animal_cow1.png"))
        r_animal_img = pygame.transform.flip(l_animal_img, True, False)
        
        l_animal_run = pygame.image.load(os.path.join("images", "animal_cow2.png"))
        r_animal_run = pygame.transform.flip(l_animal_run, True, False)
        
        facing = random.choice(("RIGHT", "LEFT")) #Randomly spawn facing random direction
        if facing == "RIGHT":
            self.facing = "RIGHT"
            self.move_right = True
            self.move_left = False
            self.current_image = r_animal_img
        else:
            self.facing = "LEFT"
            self.move_right = False
            self.move_left = True
            self.current_image = l_animal_img
        self.size = 40
        
        (self.r_image, self.r_idle) = (r_animal_img, r_animal_img)
        (self.l_image, self.l_idle) = (l_animal_img, l_animal_img)
        
        self.r_run = r_animal_run
        self.l_run = l_animal_run
        
        self.sprite_delay = random.randint(200,400)
        
        self.moving = True
        
        (self.x, self.y) = self.animalPlace()
        if random.choice((True, False)): #Choose initial moving direction for up/down
            self.move_up = True
            self.move_down = False
        else:
            self.move_up = False
            self.move_down = True
        self.wander_time = random.randint(700, 1500)#Selects random wandering time between .7 and 1.5 seconds
        self.speed = 2
        self.animalList += [self] #For future spawns of animals..
        
        self.invuln = False
        self.invulnTime = 0

    
    #We need to prevent animals from spawning on top of each other
    #Places animal where it will NOT overlap with others
    def animalPlace(self):
        locations = self.animallocations(Animal.animalList)
        while True:
            x = random.randint(1, 749) #spawn in random area on surface
            y = random.randint(1, 549)
            if not self.animalCollision(x, y, locations):
                break
        return (x, y)
    
    def animalCollision(self, x, y, locations):
        (topleft, botright) = ((x,y),(x+40, y+40))
        #We'll be checking to see if a neighbor lies in the same col / row. If both true, collision occured!
        for loc in xrange(len(locations)):
            inCol = False
            inRow = False
            (other_topleft, other_botright) = locations[loc]
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
    def animallocations(klass, animalList):
        location = []
        for animal in animalList:
            leftx = animal.x
            lefty = animal.y
            rightx = animal.x + 40
            righty = animal.y + 40
            topleft_corner = (leftx, lefty)
            botrig_corner = (rightx, righty)
            location.append( (topleft_corner, botrig_corner) )
        return location


class Monster(object):
    def __init__(self):

        l_monster_img = pygame.image.load(os.path.join("images", "monster_1.png"))
        r_monster_img = pygame.transform.flip(l_monster_img, True, False)
        
        l_monster_run = pygame.image.load(os.path.join("images", "monster_2.png"))
        r_monster_run = pygame.transform.flip(l_monster_run, True, False)
        
        l_monster_freeze = pygame.image.load(os.path.join("images", "monster_freeze.png"))
        r_monster_freeze = pygame.transform.flip(l_monster_freeze, True, False)
        
        self.facing = "LEFT"
        self.current_image = l_monster_img
        
        (self.r_image, self.r_idle) = (r_monster_img, r_monster_img)
        (self.l_image, self.l_idle) = (l_monster_img, l_monster_img)
        
        self.r_run = r_monster_run
        self.l_run = l_monster_run
        
        self.r_freeze = r_monster_freeze
        self.l_freeze = l_monster_freeze
        
        self.sprite_delay = 300
        
        self.size = 50
        self.r_image = r_monster_img
        self.l_image = l_monster_img
        self.x = 500
        self.y = 250
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.speed = 1.3
        self.slowSpeed = self.speed / 2.5
        self.speedStore = self.speed
        
        #Crash penalties when player bumps into monster
        self.eatPower = 40
        self.eatTime = 3000 #~3 seconds
        
        self.target = None
        self.targetdist_x = 0
        self.targetdist_y = 0


class Powerups(object):
    
    (speedimage, freezeimage) = (os.path.join("images", "powerup_speed.gif"),
        os.path.join("images", "powerup_freeze.gif"))
    
    def __init__(self, powerType):
        self.size = 25
        self.x = random.randint(151, 749) #spawn in random area on surface
        self.y = random.randint(76, 549)
        self.scaler = 0
        self.power = powerType
        if powerType == "SPEED":
            self.image = pygame.image.load(self.speedimage)
        elif powerType == "FREEZE":
            self.image = pygame.image.load(self.freezeimage)
    
    #Allows the 'growing onto board' effect in redrawing
    def rescaler(self):
        if self.scaler < 25:
            scale = self.scaler
            #print "scale=", scale
            self.image = pygame.transform.scale(self.image, (int(scale), int(scale)))
            #print "rescale!"
        else: #Reload the full res version
            if self.power == "SPEED":
                self.image = pygame.image.load(self.speedimage)
            elif self.power == "FREEZE":
                self.image = pygame.image.load(self.freezeimage)


class Score(object):
    
    def __init__(self):
        self.score = 0
        self.scoreGoal = 20
        self.scoreGoals = [20, 40, 70, 110, 160, 210, 280,
                           360, 450, 550, 660, 780, 900, 1030,
                           1170, 1320, 1480, 1650, 1830, 2020,
                           2220, 2430, 2650, 2880, 3120, 3370,
                           3630, 3900, 4180, 4470, 4770]
        
        self.gameStartedTime = 0
        self.initTime = 60000 #60 seconds - 1 minute
        self.time = 0
        self.timeRun = 0
        self.timeBonus = 0 #Accounts for time bonuses when animal picked up!
        self.timePenalty = 0
        self.event = None #Used to keep track of display of events later!
        
        self.gamelvl = 0
        
        self.transition = False
        self.gameOver = False
        self.selector = "none"
        
        self.helpArrow1 = pygame.image.load(os.path.join("images", "arrow1.png"))
        self.helpArrow2 = pygame.image.load(os.path.join("images", "arrow2.png"))
        self.arrowDelay = 200 #ms between icon change
        self.arrowImg = self.helpArrow1
        
        self.icon_Speed = pygame.image.load(os.path.join("images", "Icon_Speed.png"))
        self.icon_Energy = pygame.image.load(os.path.join("images", "Icon_Energy.png"))
        self.icon_Time = pygame.image.load(os.path.join("images", "Icon_Time.png"))
        
        tip_a = pygame.image.load(os.path.join("images", "tip_a.png"))
        tip_s = pygame.image.load(os.path.join("images", "tip_s.png"))
        tip_d = pygame.image.load(os.path.join("images", "tip_d.png"))
        tip_f = pygame.image.load(os.path.join("images", "tip_f.png"))
        tip_space = pygame.image.load(os.path.join("images", "tip_space.png"))
        tip_gen1 = pygame.image.load(os.path.join("images", "tip_gen1.png"))
        tip_gen2 = pygame.image.load(os.path.join("images", "tip_gen2.png"))
        tip_gen3 = pygame.image.load(os.path.join("images", "tip_gen3.png"))
        self.tipImgs = [tip_a, tip_s, tip_d, tip_f, tip_space, tip_gen1, tip_gen2, tip_gen3]
        self.curTip = 1
        
        
        #Maybe add upgrade info here as well


class Weapon(object):
    
    def __init__(self):
        
        self.icon_Fire = pygame.image.load(os.path.join("images", "Attack_Fire.png"))
        self.board_Fire = pygame.image.load(os.path.join("images", "Board_Fire.png"))
        self.usingFire = False
        self.fireStartTime = 0
        self.fireNum = 0
        self.firex = 0
        self.firey = 0
        self.fireCost = 55
        
        self.icon_Zap = pygame.image.load(os.path.join("images", "Attack_Zap.png"))
        self.usingZap = False
        self.zapCost = 7
        
        self.icon_Food = pygame.image.load(os.path.join("images", "Attack_Food.png"))
        self.board_Food = pygame.image.load(os.path.join("images", "Board_Food.png"))
        self.foodStart = 0
        self.foodNum = 0
        self.x = 0
        self.y = 0
        self.usingFood = False
        self.foodCost = 60