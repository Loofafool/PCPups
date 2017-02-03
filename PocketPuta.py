import random, pygame, sys, os, math
from pygame.locals import *

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
fpsClock = pygame.time.Clock()
scale = 3           ## change this value increment the display resolution, it being 480x270 when scale == 1
DISPLAYSURF = pygame.display.set_mode((480 * scale, 270 * scale))
pygame.display.set_caption('Pocket Chip Pups')
pygame.mouse.set_visible(False)
pygame.mouse.set_pos(150 * scale, 150 * scale)
rightEdge = 328 * scale
bottomEdge = 148 * scale

##jukebox = pygame.mixer.music
##jukebox.load('Fickle Sun III.mp3')
##jukebox.set_volume(1)
##jukebox.play(-1)
shootSound = pygame.mixer.Sound('bambu.ogg')
shootSound2 = pygame.mixer.Sound('bambu2.ogg')
shootSound3 = pygame.mixer.Sound('bambu3.ogg')
deadPupSound =  pygame.mixer.Sound('deadPup.ogg')

showCrosshair = True
mouseImage = pygame.image.load('crosshair.png').convert_alpha()
mouseImage = pygame.transform.scale(mouseImage, (16 * scale, 16 * scale)).convert_alpha()
stairsImage = pygame.image.load('stairs25.png').convert_alpha()
stairsImage = pygame.transform.scale(stairsImage, (56 * scale, 40 * scale))
shipImage = pygame.image.load('rocketship25.png').convert_alpha()
shipImage = pygame.transform.scale(shipImage, (96 * scale, 192 * scale))
if random.randint(0, 1) > 0:        ## randomizing the levels where stairs are located
    stairsLevel = 'cave2'
    if random.randint(0, 1) > 0:
        initStairsPos = [-220 * scale, -1220 * scale]
    else:
        initStairsPos = [-940 * scale, -740 * scale]
        stairsImage = pygame.transform.flip(stairsImage, 1, 0)
else:
    stairsLevel = 'cave3'
    initStairsPos = [610 * scale, -660 * scale]
stairsPos = [0, 0]
stairsPos[0] = initStairsPos[0]
stairsPos[1] = initStairsPos[1]
    
if random.randint(0, 1) > 0:
    stairsLevel2 = 'saturn2'
    if random.randint(0, 1) > 0:
        initStairsPos3 = [-80 * scale, 1420 * scale]
    else:
        initStairsPos3 = [940 * scale, 1420 * scale]
        stairsImage = pygame.transform.flip(stairsImage, 1, 0)
else:
    stairsLevel2 = 'saturn3'
    initStairsPos3 = [-1010 * scale, 100 * scale]
stairsPos3 = [0, 0]
stairsPos3[0] = initStairsPos3[0]
stairsPos3[1] = initStairsPos3[1]
    
stairsRect = Rect(0, 0, 0, 0)
stairsRect2 = Rect(0, 0, 0, 0)
stairsRect3 = Rect(0, 0, 0, 0)
stairsRect4 = Rect(0, 0, 0, 0)
stairsPos2 = [250 * scale, 0]
stairsPos4 = [10 * scale, 10 * scale]
lastBgPos = [0, 0]
lastBgPos2 = [-100 * scale, -100 * scale]
lastBgPos3 = [0, 0]
shipPos = [92 * scale, 242 * scale]
shipPos2 = [200 * scale, 100 * scale]
shipRect = Rect(0, 0, 0, 0)
font = pygame.font.Font('bit1.ttf', 10 * scale)

weaponList = []
heartList = []
grassList = []
rockList = []
pupList = []
goodPupList = []
dragonList = []
summonerList = []
brainList = []
shootGuyList = []
ghostList = []
badDudeList = []

mouse = [0, 0]
clickDest = [166 * scale, 166 * scale]
black = (0, 0, 0)
white = (255, 255, 255)
gold = (255, 205, 0)

def CheckTarget():
    i = 0
    for dragon in dragonList:
        if Rect(mouse[0] - (10 * scale), mouse[1] - (10 * scale), 20 * scale, 20 * scale).colliderect(dragon.rect):
            return(0, i)
            break
        i += 1
    i = 0
    for brain in brainList:
        if Rect(mouse[0] - (10 * scale), mouse[1] - (10 * scale), 20 * scale, 20 * scale).colliderect(brain.rect):
            return(1, i)
            break
        i += 1
    i = 0
    for guy in shootGuyList:
        if Rect(mouse[0] - (10 * scale), mouse[1] - (10 * scale), 20 * scale, 20 * scale).colliderect(guy.rect):
            return(2, i)
            break
        i += 1
    i = 0
    for ghost in ghostList:
        if Rect(mouse[0] - (10 * scale), mouse[1] - (10 * scale), 20 * scale, 20 * scale).colliderect(ghost.rect):
            return(3, i)
            break
        i += 1
    i = 0
    for summoner in summonerList:
        if Rect(mouse[0] - (10 * scale), mouse[1] - (10 * scale), 20 * scale, 20 * scale).colliderect(summoner.rect):
            return(4, i)
            break
        i += 1
    i = 0
    for dude in badDudeList:
        if Rect(mouse[0] - (10 * scale), mouse[1] - (10 * scale), 20 * scale, 20 * scale).colliderect(dude.rect):
            return(5, i)
            break
        i += 1
    return(-1, -1)

def ClearEnemyTarget():
    for dragon in dragonList:
        dragon.target = [-1, -1]
    for brain in brainList:
        brain.target = [-1, -1]
    for ghost in ghostList:
        ghost.target = [-1, -1]
    for guy in shootGuyList:
        guy.target = [-1, -1]
    for dude in badDudeList:
        dude.target = [-1, -1]

def ClearPupTarget(self):
    if princess.target[0] == self.target[0] and princess.target[1] == self.target[1]:
        princess.target = [-1, -1]
        princess.shooting = False
        princess.shootTimer = 0
    elif princess.target[0] == self.target[0] and princess.target[1] > self.target[1]:
        princess.target = [-1, -1]
        princess.shooting = False
        princess.shootTimer = 0
    if princess.target2[0] == self.target[0] and princess.target2[1] == self.target[1]:
        princess.target2 = [-1, -1]
    elif princess.target2[0] == self.target[0] and princess.target2[1] > self.target[1]:
        princess.target2 = [-1, -1]
    for pup in goodPupList:
        pup.showExp = True
        pup.expTimer = 0
        pup.exp += 16
        pup.target = [-1, -1]
    
def CheckEdge(self):
    for rect in bg.rectList:
        if rect[0] > -100 and rect[0] < 500 * scale and rect[1] > -100 and rect[1] < 300 * scale:
            if self.bottomRect.colliderect(rect) and self.speed[1] > 0:
                self.speed[1] =  0
            if self.topRect.colliderect(rect) and self.speed[1] < 0:
                self.speed[1] =  0
            if self.leftRect.colliderect(rect) and self.speed[0] < 0:
                self.speed[0] =  0
            if self.rightRect.colliderect(rect) and self.speed[0] > 0:
                self.speed[0] =  0
def EnemyTarget(self):
    if self.target == [-1, -1]:
        if self.aggroRect.colliderect(princess.rect):
            self.target = [0, 0]
    
    if self.target == [-1, -1] or self.target == [0, 0]:
        i = 0
        for pup in goodPupList:
            if self.aggroRect.colliderect(pup.rect):
                self.target = [1, i]
            i += 1
                
    if self.target[0] > -1:
        self.attacking = True
    else:
        self.attacking = False
        self.attackTimer = 0
    
def ShowHp(self):
    if self.showHp and self.hp > 0:
        self.hpImage = pygame.transform.scale(self.hpImage, (40 * self.hp / self.maxHp * (self.rect.width / (32 * scale)) * scale + 1, 10 * scale))
        DISPLAYSURF.blit(self.hpImage, [self.pos[0] - (4 * scale), self.pos[1] + self.rect.width])
        DISPLAYSURF.blit(self.borderImage, [self.pos[0]- (4 * scale), self.pos[1] + self.rect.width])
        self.hpTimer += timePassed
        if self.hpTimer > 600:
            self.showHp = False
            self.hpTimer = 0

def GameOver():
    princess.showHp = False
    princess.hpTimer = 0
    princess.hp = 60
    princess.maxHp = 60
    princess.accel = 4 * scale
    princess.walking = False
    princess.walkTimer = 0
    princess.shooting = False
    princess.shootTimer = 0
    princess.shot = False
    princess.idle = True
    princess.idleTimer = 0
    princess.hpTimer = 0
    princess.flying = False
    princess.target = [-1, -1]
    princess.target2 = [-1, -1]
    princess.arrowTimer = 0
    princess.arrowPos = [0, 0]
    princess.arrow2Pos = [0, 0]
    princess.arrows = 0
    princess.weapon = 0
    princess.dmg = 5
    princess.maxShootTimer = princess.initMaxShootTimer * 4
    princess.image = pygame.image.load('cowboy1.png').convert_alpha()
    princess.image = pygame.transform.scale(princess.image, (288 * scale, 32 * scale)).convert_alpha()
    princess.left = False
    princess.pos = [150 * scale, 150 * scale]
    stairsImage = pygame.image.load('stairs25.png').convert_alpha()
    stairsImage = pygame.transform.scale(stairsImage, (56 * scale, 40 * scale))
    del goodPupList[:]
    
    if random.randint(0, 1) > 0:
        stairsLevel = 'cave2'
        if random.randint(0, 1) > 0:
            initStairsPos = [-220 * scale, -1220 * scale]
        else:
            initStairsPos = [-940 * scale, -740 * scale]
            stairsImage = pygame.transform.flip(stairsImage, 1, 0)
    else:
        stairsLevel = 'cave3'
        initStairsPos = [610 * scale, -660 * scale]
    stairsPos = initStairsPos
        
    if random.randint(0, 1) > 0:
        stairsLevel2 = 'saturn2'
        if random.randint(0, 1) > 0:
            initStairsPos3 = [-80 * scale, 1420 * scale]
        else:
            initStairsPos3 = [940 * scale, 1420 * scale]
            stairsImage = pygame.transform.flip(stairsImage, 1, 0)
    else:
        stairsLevel2 = 'saturn3'
        initStairsPos3 = [-1010 * scale, 100 * scale]
    stairsPos3 = initStairsPos3
        
    stairsPos2 = [250 * scale, 0]
    stairsPos4 = [10 * scale, 10 * scale]
    lastBgPos = [0, 0]
    lastBgPos2 = [-100 * scale, -100 * scale]
    lastBgPos3 = [0, 0]
    shipPos = [92 * scale, 242 * scale]
    shipPos2 = [200 * scale, 100 * scale]


    clickDest = [166 * scale, 166 * scale]

    WhichLevel(bg, 'cave1', [-800 * scale, -800 * scale])
    
def WhichLevel(self, level, pos):   ## spawns enemies and pups and weapons and grasses and everything for each time you change levels
    if level == 'cave1' or level == 'cave2' or level == 'cave3':
        maxRand = 8
        minRand = 1
        maxDragon = 2
        minDragon = 0
        maxWidth = 1400 * scale
    elif level == 'saturn1' or level == 'saturn2' or level == 'saturn3':
        maxRand = 22
        minRand = 10
        maxDragon = 14
        minDragon = 8
        maxWidth = 1400 * scale
    elif level == 'beach':
        maxRand = 2
        minRand = 0
        maxDragon = 1
        minDragon = 0
        maxWidth = 400 * scale
    else:
        maxRand = 9
        minRand = 4
        maxDragon = 7
        minDragon = 2
        maxWidth = 600 * scale
    if len(goodPupList) == 0:
        maxPup = 2
        minPup = 1
    elif len(goodPupList) == 1:
        maxPup = 2
        minPup = 0
    elif len(goodPupList) == 2:
        maxPup = 2
        minPup = 0
    elif len(goodPupList) >= 3:
        maxPup = 0
        minPup = 0
    del self.posList[:]
    del self.rectList[:]
    del self.voidList[:]
    self.level = level
    self.pos[0] = pos[0]
    self.pos[1] = pos[1]
    lvlFile = []
    self.image = pygame.image.load(str(level) + '25.png').convert()
    self.image = pygame.transform.scale(self.image, (1600 * scale, 1600 * scale)).convert()
    r1 = open(str(level) + '.txt', 'r')
    q1 = r1.read()
    i = 0
    while i < 5098:
        if i % 2 == 0:
            lvlFile.append(q1[i])
        i += 1
    r1.close()
    i = 0
    p = 0
    k = 0
    while i < 2549:
        if str(lvlFile[i]) == '1':
            self.posList.append([(p * 32 * scale) + self.pos[0], (k * 32 * scale) + self.pos[1]])
            self.rectList.append(Rect((p * 32 * scale) + self.pos[0], (k * 32 * scale) + self.pos[1], 32 * scale, 32 * scale))
        if str(lvlFile[i]) == '2':
            self.voidList.append(Rect((p * 32 * scale) + self.pos[0], (k * 32 * scale) + self.pos[1], 32 * scale, 32 * scale))
        i += 1
        p += 1
        if p > 50:
            k += 1
            p = 0

    del weaponList[:]
    del princess.bulletList[:]
    del heartList[:]
    del grassList[:]
    del rockList[:]
    del badDudeList[:]
    del ghostList[:]
    del shootGuyList[:]
    del brainList[:]
    del dragonList[:]
    del summonerList[:]
    del pupList[:]
    for pup in goodPupList:
        pup.target = [-1, -1]
        pup.pos[0] = princess.pos[0]
        pup.pos[1] = princess.pos[1]

    i = 0
    while i < random.randint(1, 3):
        weaponList.append(Weapon([random.randint(self.pos[0], self.pos[0] + maxWidth), random.randint(self.pos[1], self.pos[1] + maxWidth)], random.randint(0, 3)))
        for rect in self.rectList:
            if weaponList[i].rect.colliderect(rect):
                weaponList.remove(weaponList[i])
                i -=1
                go = False
                break
            else:
                go = True
        if go:
            for rect in self.voidList:
                if weaponList[i].rect.colliderect(rect):
                    weaponList.remove(weaponList[i])
                    i -= 1
                    break
        i += 1
    i = 0
    while i < random.randint(0, 2):
        heartList.append(Heart([random.randint(self.pos[0], self.pos[0] + maxWidth), random.randint(self.pos[1], self.pos[1] + maxWidth)]))
        for rect in self.rectList:
            if heartList[i].rect.colliderect(rect):
                heartList.remove(heartList[i])
                i -=1
                go = False
                break
            else:
                go = True
        if go:
            for rect in self.voidList:
                if heartList[i].rect.colliderect(rect):
                    heartList.remove(heartList[i])
                    i -= 1
                    break
        i += 1
    
    i = 0
    while i < random.randint(14, 50):
        grassList.append(Grass([random.randint(self.pos[0], self.pos[0] + maxWidth), random.randint(self.pos[1], self.pos[1] + maxWidth)], random.randint(1, 8)))
        for rect in self.rectList:
            if grassList[i].rect.colliderect(rect):
                grassList.remove(grassList[i])
                i -= 1
                go = False
                break
            else:
                go = True
        if go:
            for rect in self.voidList:
                if grassList[i].rect.colliderect(rect):
                    grassList.remove(grassList[i])
                    i -=1
                    break
        i += 1
        
    i = 0    
    while i < random.randint(4, 14):
        rockList.append(Rock([random.randint(self.pos[0], self.pos[0] + maxWidth), random.randint(self.pos[1], self.pos[1] + maxWidth)], random.randint(0, 3)))
        for rect in self.rectList:
            if rockList[i].rect.colliderect(rect):
                rockList.remove(rockList[i])
                i -= 1
                go = False
                break
            else:
                go = True
        if go:
            for rect in self.voidList:
                if rockList[i].rect.colliderect(rect):
                    rockList.remove(rockList[i])
                    i -=1
                    break
        i += 1

    i = 0
    while i < random.randint(minPup, maxPup):
        pupList.append(Pup([random.randint(self.pos[0], self.pos[0] + maxWidth), random.randint(self.pos[1], self.pos[1] + maxWidth)], random.randint(0, 9), False))
        for rect in self.rectList:
            if pupList[i].rect.colliderect(rect):
                pupList.remove(pupList[i])
                i -= 1
                go = False
                break
            else:
                go = True
        if go:
            for rect in self.voidList:
                if pupList[i].rect.colliderect(rect):
                    pupList.remove(pupList[i])
                    i -=1
                    break
        i += 1
        
    i = 0
    while i < random.randint(minDragon, maxDragon):
        summonerList.append(DragonSummoner([random.randint(self.pos[0], self.pos[0] + maxWidth), random.randint(self.pos[1], self.pos[1] + maxWidth)]))
        for rect in self.rectList:
            if summonerList[i].rect.colliderect(rect):
                summonerList.remove(summonerList[i])
                i -=1
                go = False
                break
            else:
                go = True
        if go:
            for rect in self.voidList:
                if summonerList[i].rect.colliderect(rect):
                    summonerList.remove(summonerList[i])
                    i -=1
                    break
        i += 1

    i = 0
    while i < random.randint(minRand, maxRand):
        brainList.append(Brain([random.randint(self.pos[0], self.pos[0] + maxWidth), random.randint(self.pos[1], self.pos[1] + maxWidth)]))
        for rect in self.rectList:
            if brainList[i].rect.colliderect(rect):
                brainList.remove(brainList[i])
                i -= 1
                go = False
                break
            else:
                go = True
        if go:
            for rect in self.voidList:
                if brainList[i].rect.colliderect(rect):
                    brainList.remove(brainList[i])
                    i -=1
                    break
        i += 1

    i = 0
    while i < random.randint(minRand, maxRand):
        shootGuyList.append(ShootingGuy([random.randint(self.pos[0], self.pos[0] + maxWidth), random.randint(self.pos[1], self.pos[1] + maxWidth)]))
        for rect in self.rectList:
            if shootGuyList[i].rect.colliderect(rect):
                shootGuyList.remove(shootGuyList[i])
                i -=1
                go = False
                break
            else:
                go = True
        if go:
            for rect in self.voidList:
                if shootGuyList[i].rect.colliderect(rect):
                    shootGuyList.remove(shootGuyList[i])
                    i -=1
                    break
        i += 1

    i = 0
    while i < random.randint(minRand, maxRand):
        ghostList.append(Ghost([random.randint(self.pos[0], self.pos[0] + maxWidth), random.randint(self.pos[1], self.pos[1] + maxWidth)]))
        for rect in self.rectList:
            if ghostList[i].rect.colliderect(rect):
                ghostList.remove(ghostList[i])
                i -=1
                go = False
                break
            else:
                go = True
        if go:
            for rect in self.voidList:
                if ghostList[i].rect.colliderect(rect):
                    ghostList.remove(ghostList[i])
                    i -=1
                    break
        i += 1

    i = 0
    while i < random.randint(minRand, maxRand):
        badDudeList.append(BadDude([random.randint(self.pos[0], self.pos[0] + maxWidth), random.randint(self.pos[1], self.pos[1] + maxWidth)]))
        for rect in self.rectList:
            if badDudeList[i].rect.colliderect(rect):
                badDudeList.remove(badDudeList[i])
                i -=1
                go = False
                break
            else:
                go = True
        if go:
            for rect in self.voidList:
                if badDudeList[i].rect.colliderect(rect):
                    badDudeList.remove(badDudeList[i])
                    i -=1
                    break
        i += 1
    

class BG():
    def __init__(self):
        self.image = pygame.image.load('cave125.png').convert()
        self.image = pygame.transform.scale(self.image, (1600 * scale, 1600 * scale)).convert()
        self.pos = [0, 0]
        self.posList = []
        self.rectList = []
        self.voidList = []
        self.level = 'cave1'

        WhichLevel(self, self.level, [-800 * scale, -800 * scale])

    def update(self):
        if self.pos[0] > 0:
            self.pos[0] = 0
        if self.pos[0] < -1120 * scale:
            self.pos[0] = -1120 * scale
        if self.pos[1] > 0:
            self.pos[1] = 0
        if self.pos[1] < -1328 * scale:
            self.pos[1] = -1328 * scale
        i = 0
        for pos in self.posList:
            self.rectList[i] = Rect(pos[0], pos[1], 32 * scale, 32 * scale)
            i += 1

        if self.level == 'cave1' and self.pos[1] >= 0 and princess.pos[1] <= 30 * scale:    ## default positions for each level
            WhichLevel(self, 'cave2', [-1120 * scale, -1328 * scale])                   ## depending on which level you are coming from
            princess.pos = [200 * scale, 200 * scale]
            if stairsLevel == 'cave2':
                stairsPos[0] = initStairsPos[0]
                stairsPos[1] = initStairsPos[1]
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'cave1' and self.pos[0] <= -1120 and princess.pos[0] >= 400 * scale:
            WhichLevel(self, 'cave3', [0, -800 * scale])
            if stairsLevel == 'cave3':
                stairsPos[0] = initStairsPos[0]
                stairsPos[1] = initStairsPos[1]
            princess.pos = [50 * scale, 200 * scale]
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'cave2' and self.pos[1] <= -1328 and princess.pos[1] >= 230 * scale:
            WhichLevel(self, 'cave1', [-460 * scale, 0])
            princess.pos = [50 * scale, 50 * scale]
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'cave3' and self.pos[0] >= 0 and princess.pos[0] <= 30 * scale:
            WhichLevel(self, 'cave1', [-1120 * scale, -500 * scale])
            princess.pos = [350 * scale, 200 * scale]
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == stairsLevel and princess.rect.colliderect(stairsRect):
            lastBgPos[0] = bg.pos[0]
            lastBgPos[1] = bg.pos[1]
            stairsPos2[0] = 250 * scale
            stairsPos2[1] = -20 * scale
            princess.pos[0] = stairsPos2[0] - (100 * scale)
            princess.pos[1] = stairsPos2[1] + (140 * scale)
            WhichLevel(self, 'beach', [-100 * scale, -100 * scale])
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'beach' and princess.rect.colliderect(stairsRect2):
            WhichLevel(self, stairsLevel, [int(lastBgPos[0]), int(lastBgPos[1])])
            princess.pos = [stairsPos[0], stairsPos[1] + (84 * scale)]
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'beach' and princess.pos[1] < -92 * scale:
            shipPos2[0] = 200 * scale
            shipPos2[1] = 100 * scale
            WhichLevel(self, 'saturn1', [-820 * scale, -100 * scale])
            princess.flying = False
            princess.pos = [100 * scale, 150 * scale]
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'saturn1' and princess.pos[1] > 300 * scale:
            stairsPos2[0] = 250 * scale
            stairsPos2[1] = -20 * scale
            shipPos[0] = 92 * scale
            shipPos[1] = 242 * scale
            princess.flying = False
            princess.pos[0] = 100 * scale
            princess.pos[1] = 100 * scale
            WhichLevel(self, 'beach', [-100 * scale, -100 * scale])
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'saturn1' and self.pos[0] >= 0 and princess.pos[0] < 32 * scale:
            WhichLevel(self, 'saturn3', [-1120 * scale, - 500 * scale])
            if stairsLevel2 == 'saturn3':
                stairsPos3[0] = initStairsPos3[0]
                stairsPos3[1] = initStairsPos3[1]
            princess.pos[0] = 300 * scale
            princess.pos[1] = 100 * scale
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'saturn1' and self.pos[1] <= -1328 and princess.pos[1] > 220 * scale:
            WhichLevel(self, 'saturn2', [-220 * scale, 0])
            if stairsLevel2 == 'saturn2':
                stairsPos3[0] = initStairsPos3[0]
                stairsPos3[1] = initStairsPos3[1]
            princess.pos = [200 * scale, 80 * scale]
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'saturn2' and self.pos[1] >= 0 and princess.pos[1] < 40 * scale:
            WhichLevel(self, 'saturn1', [-420 * scale, -1328 * scale])
            princess.pos = [200 * scale, 180 * scale]
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'saturn3' and self.pos[0] <= -1120 and princess.pos[0] > 400 * scale:
            WhichLevel(self, 'saturn1', [0, -400 * scale])
            princess.pos = [80 * scale, 180 * scale]
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == stairsLevel2 and princess.rect.colliderect(stairsRect3):
            lastBgPos2[0] = bg.pos[0]
            lastBgPos2[1] = bg.pos[1]
            stairsPos4[0] = 10 * scale
            stairsPos4[1] = 10 * scale
            princess.pos[0] = stairsPos4[0] + (80 * scale)
            princess.pos[1] = stairsPos4[1] + (20 * scale)
            WhichLevel(self, 'desert1', [-100 * scale, -100 * scale])
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'desert1' and princess.rect.colliderect(stairsRect4):
            WhichLevel(self, stairsLevel2, [int(lastBgPos2[0]), int(lastBgPos2[1])])
            princess.pos = [stairsPos3[0] + (74 * scale), stairsPos3[1]]
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'desert1' and self.pos[1] <= -570 * scale:
            lastBgPos3[0] = bg.pos[0]
            lastBgPos3[1] = bg.pos[1]
            WhichLevel(self, 'desert2', [0, 0])
            princess.pos = [110 * scale, 110 * scale]
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'desert1' and self.pos[0] <= -450 * scale:
            lastBgPos3[0] = bg.pos[0]
            lastBgPos3[1] = bg.pos[1]
            WhichLevel(self, 'desert3', [-10 * scale, -190 * scale])
            princess.pos = [190 * scale, 200 * scale]
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'desert2' and princess.pos[1] < 40 * scale:
            WhichLevel(self, 'desert1', [int(lastBgPos3[0]), int(lastBgPos3[1]) + (20 * scale)])
            stairsPos4[1] += 20
            princess.pos = [110 * scale, 180 * scale]
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        if self.level == 'desert3' and self.pos[1] <= -250 * scale:
            WhichLevel(self, 'desert1', [int(lastBgPos3[0]) + (20 * scale), int(lastBgPos3[1])])
            stairsPos4[0] += 20
            princess.pos = [260 * scale, 120 * scale]
            princess.walking = False
            princess.target = [-1, -1]
            princess.target2 = [-1, -1]
            for pup in goodPupList:
                pup.target = [-1, -1]
                pup.pos[0] = princess.pos[0]
                pup.pos[1] = princess.pos[1]
        
        
        DISPLAYSURF.blit(self.image, self.pos)
        
class Heart():
    def __init__(self, pos):
        self.image = pygame.image.load('heart.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20 * scale, 20 * scale)).convert_alpha()
        self.pos = pos
        self.rect = Rect(self.pos[0], self.pos[1], 20 * scale, 20 * scale)
        self.remove = False
    def update(self):
        self.rect = Rect(self.pos[0], self.pos[1], 20 * scale, 20 * scale)
        if self.pos[0] > -80 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale:
            DISPLAYSURF.blit(self.image, self.pos)
        
class Rock():
    def __init__(self, pos, rock):
        self.rock = rock
        self.image = pygame.image.load('cactus.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (128 * scale, 32 * scale)).convert_alpha()
        self.pos = pos
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
    def update(self):
        if self.pos[0] > -80 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale:
            DISPLAYSURF.blit(self.image, self.pos, (self.rock * 32 * scale, 0, 32 * scale, 32 * scale))

        
class Grass():
    def __init__(self, pos, grass):
        self.grass = grass
        if self.grass == 1:     ## all the pretty grasses
            self.image = pygame.image.load('wheat.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (128 * scale, 32 * scale)).convert_alpha()
        if self.grass == 2:
            self.image = pygame.image.load('wheat2.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (64 * scale, 32 * scale)).convert_alpha()
        if self.grass == 3:
            self.image = pygame.image.load('wheat3.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (128 * scale, 32 * scale)).convert_alpha()
        if self.grass == 4:
            self.image = pygame.image.load('wheat4.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (64 * scale, 32 * scale)).convert_alpha()
        if self.grass == 5:
            self.image = pygame.image.load('wheat5.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (128 * scale, 32 * scale)).convert_alpha()
        if self.grass == 6:
            self.image = pygame.image.load('wheat6.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (64 * scale, 32 * scale)).convert_alpha()
        if self.grass == 7:
            self.image = pygame.image.load('wheat7.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (128 * scale, 32 * scale)).convert_alpha()
        if self.grass == 8:
            self.image = pygame.image.load('wheat8.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (64 * scale, 32 * scale)).convert_alpha()
        self.pos = pos
        self.frame = 0
        self.timer = 0
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
    def update(self):
        if self.pos[0] > -80 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale:
            self.timer += timePassed
            if self.timer > 400:
                self.timer = 0
            if self.grass % 2 != 0:
                if self.timer < 100:    ## grass in the wind!
                    self.frame = 0
                elif self.timer >= 100 and self.timer < 200:
                    self.frame = 1
                elif self.timer >= 200 and self.timer < 300:
                    self.frame = 2
                elif self.timer >= 300:
                    self.frame = 3
            else:                       ## 2 frame grass
                if self.timer < 200:
                    self.frame = 0
                elif self.timer >= 200:
                    self.frame = 1
    def draw(self):
        if self.pos[0] > -80 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale:
            DISPLAYSURF.blit(self.image, self.pos, (self.frame * 32 * scale, 0, 32 * scale, 32 * scale))


            
class Bullet():
    def __init__(self, pos, bullet, angle):
        if bullet <= 3:
            self.image = pygame.image.load('cowboybullets.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (112 * scale, 14 * scale)).convert_alpha()
        elif bullet == 4:
            self.image = pygame.image.load('purplebullet.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (56 * scale, 14 * scale)).convert_alpha()
        elif bullet == 5:
            self.image = pygame.image.load('redbullet.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (56 * scale, 14 * scale)).convert_alpha()
        self.pos = pos
        self.angle = angle
        self.bullet = bullet
        self.frame = 0
        if self.bullet == 0:
            self.accel = 15 * scale
        elif self.bullet == 1:
            self.accel = 5 * scale
        elif self.bullet == 2:
            self.accel = 17 * scale
        elif self.bullet == 3:
            self.accel = 20 * scale
        elif self.bullet == 4:
            self.accel = 2 * scale
        elif self.bullet == 5:
            self.accel = 9 * scale
        self.speed = [math.sin(math.radians(self.angle)) * -self.accel, math.cos(math.radians(self.angle)) * -self.accel]
        self.timer = 0
        self.remove = False

        self.rect = Rect(self.pos[0], self.pos[1], 14 * scale, 14 * scale)
    def update(self):
        self.rect = Rect(self.pos[0], self.pos[1], 14 * scale, 14 * scale)

        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.timer += timePassed

        if self.pos[0] < -100 * scale or self.pos[0] > 600 * scale or self.pos[1] < -100 * scale or self.pos[1] > 400 * scale:
            self.remove = True
        else:
            for rect in bg.rectList:
                if self.rect.colliderect(rect):
                    self.remove = True

        if self.bullet == 1:            ## player target angles
            if princess.target[0] == 0:
                self.angle = math.degrees(math.atan2(self.pos[0] + (7 * scale) - dragonList[princess.target[1]].pos[0] - (34 * scale), self.pos[1] + (7 * scale) - dragonList[princess.target[1]].pos[1] - (34 * scale)))
            if princess.target[0] == 1:
                self.angle = math.degrees(math.atan2(self.pos[0] + (7 * scale) - brainList[princess.target[1]].pos[0] - (18 * scale), self.pos[1] + (7 * scale) - brainList[princess.target[1]].pos[1] - (18 * scale)))
            if princess.target[0] == 2:
                self.angle = math.degrees(math.atan2(self.pos[0] + (7 * scale) - shootGuyList[princess.target[1]].pos[0] - (18 * scale), self.pos[1] + (7 * scale) - shootGuyList[princess.target[1]].pos[1] - (18 * scale)))
            if princess.target[0] == 3:
                self.angle = math.degrees(math.atan2(self.pos[0] + (7 * scale) - ghostList[princess.target[1]].pos[0] - (18 * scale), self.pos[1] + (7 * scale) - ghostList[princess.target[1]].pos[1] - (18 * scale)))
            if princess.target[0] == 4:
                self.angle = math.degrees(math.atan2(self.pos[0] + (7 * scale) - summonerList[princess.target[1]].pos[0] - (18 * scale), self.pos[1] + (7 * scale) - summonerList[princess.target[1]].pos[1] - (18 * scale)))
            if princess.target[0] == 5:
                self.angle = math.degrees(math.atan2(self.pos[0] + (7 * scale) - badDudeList[princess.target[1]].pos[0] - (18 * scale), self.pos[1] + (7 * scale) - badDudeList[princess.target[1]].pos[1] - (18 * scale)))
            
            self.speed = [math.sin(math.radians(self.angle)) * -self.accel, math.cos(math.radians(self.angle)) * -self.accel]
            
            
        if self.bullet <= 3:
            if self.timer > 30:
                self.timer = 0
            if self.bullet == 0:
                if self.timer < 15:
                    self.frame = 0
                else:
                    self.frame = 1
            elif self.bullet == 1:
                if self.timer < 15:
                    self.frame = 6
                else:
                    self.frame = 7
            elif self.bullet == 2:
                if self.timer < 15:
                    self.frame = 4
                else:
                    self.frame = 5
            elif self.bullet == 3:
                if self.timer < 15:
                    self.frame = 2
                else:
                    self.frame = 3
        else:
            if self.timer > 60:
                self.timer = 0
            if self.timer < 15:
                self.frame = 0
            elif self.timer >= 15 and self.timer < 30:
                self.frame = 1
            elif self.timer >= 30 and self.timer < 45:
                self.frame = 2
            elif self.timer >= 45:
                self.frame = 3
            


        DISPLAYSURF.blit(self.image, self.pos, (self.frame * 14 * scale, 0, 14 * scale, 14 * scale))
     
class Princess():       ## player class
    def __init__(self):
        self.image = pygame.image.load('cowboy1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (288 * scale, 32 * scale)).convert_alpha()
        self.arrowImage = pygame.image.load('arrow.png').convert_alpha()
        self.arrowImage = pygame.transform.scale(self.arrowImage, (64 * scale, 14 * scale)).convert_alpha()
        self.arrowImage2 = pygame.image.load('arrowblue.png').convert_alpha()
        self.arrowImage2 = pygame.transform.scale(self.arrowImage2, (64 * scale, 14 * scale)).convert_alpha()
        self.hpImage = pygame.image.load('health.png').convert_alpha()
        self.hpImage = pygame.transform.scale(self.hpImage, (40 * scale, 10 * scale)).convert_alpha()
        self.borderImage = pygame.image.load('border2.png').convert_alpha()
        self.borderImage = pygame.transform.scale(self.borderImage, (40 * scale, 10 * scale)).convert_alpha()
        self.pos = [150 * scale, 150 * scale]
        self.speed = [0, 0]
        self.frame = 0
        self.arrowFrame = 0
        self.left = False
        self.showHp = False
        self.hpTimer = 0
        self.hp = 60
        self.maxHp = 60
        self.accel = 4 * scale
        self.angle = 0
        self.walking = False
        self.walkTimer = 0
        self.shooting = False
        self.shootTimer = 0
        self.shot = False
        self.idle = True
        self.idleTimer = 0
        self.dmg = 5
        self.hpTimer = 0
        self.flying = False
        self.middle = 16 * scale
        self.target = [-1, -1]
        self.target2 = [-1, -1]
        self.arrowTimer = 0
        self.arrowPos = [0, 0]
        self.arrow2Pos = [0, 0]
        self.arrows = 0
        self.bulletList = []
        self.weapon = 0
        self.initMaxShootTimer = float(100)
        self.maxShootTimer = float(400)
        
        self.rect = Rect(0, 0, 0, 0)    
    def update(self):
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
        self.bottomRect = Rect(self.pos[0] + (12 * scale), self.pos[1] + (30 * scale), 8 * scale, 4 * scale)
        self.topRect = Rect(self.pos[0] + (12 * scale), self.pos[1] + (8 * scale), 8 * scale, 4 * scale) 
        self.rightRect = Rect(self.pos[0] + (20 * scale), self.pos[1] + (18 * scale), 4 * scale, 6 * scale)
        self.leftRect = Rect(self.pos[0] + (4 * scale), self.pos[1] + (18 * scale), 4 * scale, 6 * scale)
        if self.walking == False and self.shooting == False:
            self.walkTimer = 0
            self.shootTimer = 0
            self.shot = False
            self.idle = True
        else:
            self.idle = False
        if self.idle:
            self.idleTimer += timePassed
            if self.idleTimer > 400:
                self.idleTimer = 0

        if self.hp <= 0:
            GameOver()
        for heart in heartList:     ## health pickup if missing enough health
            if self.rect.colliderect(heart.rect) and self.hp < self.maxHp - 20:
                self.hp = self.maxHp
                self.showHp = True
                self.hpTimer = 0
                heart.remove = True
                break
        
        if self.rect.colliderect(shipRect):
            self.flying = True
        if self.flying:         ## space ship!
            if bg.level == 'beach':
                self.pos[0] = shipPos[0] + (32 * scale)
                self.pos[1] = shipPos[1] + (32 * scale)
                i = 0
                for pup in goodPupList:
                    pup.pos[0] = shipPos[0] + (42 * scale)
                    pup.pos[1] = shipPos[1] + (32 * i * scale)
                    i += 1
                shipPos[1] -= 3 * scale
            if bg.level == 'saturn1':
                self.pos[0] = shipPos2[0] + (42 * scale)
                self.pos[1] = shipPos2[1] + (32 * scale)
                i = 0
                for pup in goodPupList:
                    pup.pos[0] = shipPos2[0] + (42 * scale)
                    pup.pos[1] = shipPos2[1] + (32 * i * scale)
                    i += 1
                shipPos2[1] += 3 * scale
        if self.walking == False and self.target[0] >= 0:
            self.shooting = True
        if self.shooting:
            self.shootTimer += timePassed
            if self.shootTimer > self.maxShootTimer:
                self.shot = False
                self.shootTimer = 0
            if self.shootTimer >= self.maxShootTimer - 50 and self.shot == False:
                self.shot = True
                if self.weapon == 0 or self.weapon == 3:
                    shootSound2.play()
                elif self.weapon == 1:
                    shootSound.play()
                elif self.weapon == 2:
                    shootSound3.play()
                if self.left:               ## makin bullets
                    if self.target[0] == 0:
                        self.bulletList.append(Bullet([self.pos[0], self.pos[1] + (16 * scale)], self.weapon, math.degrees(math.atan2(self.pos[0] - dragonList[self.target[1]].pos[0] - (34 * scale), self.pos[1] + self.middle - dragonList[self.target[1]].pos[1] - (34 * scale)))))
                        if self.pos[0] < dragonList[self.target[1]].pos[0]:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = False
                    if self.target[0] == 1:
                        self.bulletList.append(Bullet([self.pos[0], self.pos[1] + (16 * scale)], self.weapon, math.degrees(math.atan2(self.pos[0] - brainList[self.target[1]].pos[0] - (18 * scale), self.pos[1] + self.middle - brainList[self.target[1]].pos[1] - 18 * scale))))
                        if self.pos[0] < brainList[self.target[1]].pos[0]:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = False
                    if self.target[0] == 2:
                        self.bulletList.append(Bullet([self.pos[0], self.pos[1] + (16 * scale)], self.weapon, math.degrees(math.atan2(self.pos[0] - shootGuyList[self.target[1]].pos[0] - (18 * scale), self.pos[1] + self.middle - shootGuyList[self.target[1]].pos[1] - (18 * scale)))))
                        if self.pos[0] < shootGuyList[self.target[1]].pos[0]:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = False
                    if self.target[0] == 3:
                        self.bulletList.append(Bullet([self.pos[0], self.pos[1] + (16 * scale)], self.weapon, math.degrees(math.atan2(self.pos[0] - ghostList[self.target[1]].pos[0] - (18 * scale), self.pos[1] + self.middle - ghostList[self.target[1]].pos[1] - (18 * scale)))))
                        if self.pos[0] < ghostList[self.target[1]].pos[0]:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = False
                    if self.target[0] == 4:
                        self.bulletList.append(Bullet([self.pos[0], self.pos[1] + (16 * scale)], self.weapon, math.degrees(math.atan2(self.pos[0] - summonerList[self.target[1]].pos[0] - (18 * scale), self.pos[1] + self.middle - summonerList[self.target[1]].pos[1] - (18 * scale)))))
                        if self.pos[0] < summonerList[self.target[1]].pos[0]:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = False
                    if self.target[0] == 5:
                        self.bulletList.append(Bullet([self.pos[0], self.pos[1] + (16 * scale)], self.weapon, math.degrees(math.atan2(self.pos[0] - badDudeList[self.target[1]].pos[0] - (18 * scale), self.pos[1] + self.middle - badDudeList[self.target[1]].pos[1] - (18 * scale)))))
                        if self.pos[0] < badDudeList[self.target[1]].pos[0]:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = False

                else:               ## makin bullets from the right
                    if self.target[0] == 0:
                        self.bulletList.append(Bullet([self.pos[0] + (32 * scale), self.pos[1] + (16 * scale)], self.weapon, math.degrees(math.atan2(self.pos[0] + (32 * scale) - dragonList[self.target[1]].pos[0] - (34 * scale), self.pos[1] + self.middle - dragonList[self.target[1]].pos[1] - (34 * scale)))))
                        if self.pos[0] > dragonList[self.target[1]].pos[0]:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = True
                    if self.target[0] == 1:
                        self.bulletList.append(Bullet([self.pos[0] + (32 * scale), self.pos[1] + (16 * scale)], self.weapon, math.degrees(math.atan2(self.pos[0] + (32 * scale) - brainList[self.target[1]].pos[0] - (18 * scale), self.pos[1] + self.middle - brainList[self.target[1]].pos[1] - 18 * scale))))
                        if self.pos[0] > brainList[self.target[1]].pos[0]:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = True
                    if self.target[0] == 2:
                        self.bulletList.append(Bullet([self.pos[0] + (32 * scale), self.pos[1] + (16 * scale)], self.weapon, math.degrees(math.atan2(self.pos[0] + (32 * scale) - shootGuyList[self.target[1]].pos[0] - (18 * scale), self.pos[1] + self.middle - shootGuyList[self.target[1]].pos[1] - (18 * scale)))))
                        if self.pos[0] > shootGuyList[self.target[1]].pos[0]:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = True
                    if self.target[0] == 3:
                        self.bulletList.append(Bullet([self.pos[0] + (32 * scale), self.pos[1] + (16 * scale)], self.weapon, math.degrees(math.atan2(self.pos[0] + (32 * scale) - ghostList[self.target[1]].pos[0] - (18 * scale), self.pos[1] + self.middle - ghostList[self.target[1]].pos[1] - (18 * scale)))))
                        if self.pos[0] > ghostList[self.target[1]].pos[0]:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = True
                    if self.target[0] == 4:
                        self.bulletList.append(Bullet([self.pos[0] + (32 * scale), self.pos[1] + (16 * scale)], self.weapon, math.degrees(math.atan2(self.pos[0] + (32 * scale) - summonerList[self.target[1]].pos[0] - (18 * scale), self.pos[1] + self.middle - summonerList[self.target[1]].pos[1] - (18 * scale)))))
                        if self.pos[0] > summonerList[self.target[1]].pos[0]:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = True
                    if self.target[0] == 5:
                        self.bulletList.append(Bullet([self.pos[0] + (32 * scale), self.pos[1] + (16 * scale)], self.weapon, math.degrees(math.atan2(self.pos[0] + (32 * scale) - badDudeList[self.target[1]].pos[0] - (18 * scale), self.pos[1] + self.middle - badDudeList[self.target[1]].pos[1] - (18 * scale)))))
                        if self.pos[0] > badDudeList[self.target[1]].pos[0]:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = True

        for rect in bg.rectList:        ## collision detection for solid blocks
            if rect[0] > -100 and rect[0] < 500 * scale and rect[1] > -100 and rect[1] < 300 * scale:
                if self.bottomRect.colliderect(rect):
                    if self.speed[1] > 0:
                        self.speed = [0, 0]
                        self.walking = False
                        self.walkTimer = 0
                if self.topRect.colliderect(rect):
                    if self.speed[1] < 0:
                        self.speed = [0, 0]
                        self.walking = False
                        self.walkTimer = 0
                if self.rightRect.colliderect(rect):
                    if self.speed[0] > 0:
                        self.speed = [0, 0]
                        self.walking = False
                        self.walkTimer = 0
                if self.leftRect.colliderect(rect):
                    if self.speed[0] < 0:
                        self.speed = [0, 0]
                        self.walking = False
                        self.walkTimer = 0
        if self.walking:
            self.idleTimer = 0
            self.walkTimer += timePassed
            if self.walkTimer > 280:
                self.walkTimer = 0
            xx = CheckTarget()
            if click == (1, 0, 0) and xx != self.target:                
                self.angle = math.degrees(math.atan2(self.pos[0] + self.middle - mouse[0], self.pos[1] + self.middle - mouse[1]))
                self.speed[0] = math.sin(math.radians(self.angle)) * -self.accel
                self.speed[1] = math.cos(math.radians(self.angle)) * -self.accel
                clickDest[0] = mouse[0]
                clickDest[1] = mouse[1]
                self.walking = True
                if self.left == False and self.speed[0] < 0:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.left = True
                if self.left and self.speed[0] > 0:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.left = False
            if self.pos[0] < rightEdge and self.pos[0] > 120 * scale:   ## player movement (x axis)
                self.pos[0] += self.speed[0]
            elif self.pos[0] > rightEdge and self.speed[0] < 0:
                self.pos[0] += self.speed[0]
            elif self.pos[0] < 120 * scale and self.speed[0] > 0:
                self.pos[0] += self.speed[0]
            elif bg.pos[0] >= 0  and self.speed[0] < 0:
                self.pos[0] += self.speed[0]
            elif bg.pos[0] <= -1120 * scale and self.speed[0] > 0:
                self.pos[0] += self.speed[0]
            else:                           ## scrolling BG and everything else... 
                bg.pos[0] -= self.speed[0]      ## when player moving near edge
                clickDest[0] -= self.speed[0]       ## (x axis)
                for pos in bg.posList:
                    pos[0] -= self.speed[0]
                for heart in heartList:
                    heart.pos[0] -= self.speed[0]
                for grass in grassList:
                    grass.pos[0] -= self.speed[0]
                for rock in rockList:
                    rock.pos[0] -= self.speed[0]
                for weapon in weaponList:
                    weapon.pos[0] -= self.speed[0]
                for bullet in self.bulletList:
                    bullet.pos[0] -= self.speed[0]
                for guy in shootGuyList:
                    guy.pos[0] -= self.speed[0]
                    for bullet in guy.bulletList:
                        bullet.pos[0] -= self.speed[0]
                for brain in brainList:
                    brain.pos[0] -= self.speed[0]
                    for bullet in brain.bulletList:
                        bullet.pos[0] -= self.speed[0]
                for summoner in summonerList:
                    summoner.pos[0] -= self.speed[0]
                for dragon in dragonList:
                    dragon.pos[0] -= self.speed[0]
                    if dragon.flame:
                        dragon.flamePos[0] -= self.speed[0]
                for ghost in ghostList:
                    ghost.pos[0] -= self.speed[0]
                    if ghost.skull:
                        ghost.skullPos[0] -= self.speed[0]
                for dude in badDudeList:
                    dude.pos[0] -= self.speed[0]
                for pup in pupList:
                    pup.pos[0] -= self.speed[0]
                for pup in goodPupList:
                    pup.pos[0] -= self.speed[0]
                if bg.level == stairsLevel:
                    stairsPos[0] -= self.speed[0]
                if bg.level == 'beach':
                    shipPos[0] -= self.speed[0]
                    stairsPos2[0] -= self.speed[0]
                if bg.level == 'saturn1':
                    shipPos2[0] -= self.speed[0]
                if bg.level == stairsLevel2:
                    stairsPos3[0] -= self.speed[0]
                if bg.level == 'desert1':
                    stairsPos4[0] -= self.speed[0]
            if self.pos[1] < bottomEdge and self.pos[1] > 90 * scale:       ## player movement (y axis)
                self.pos[1] += self.speed[1]
            elif self.pos[1] > bottomEdge and self.speed[1] < 0:
                self.pos[1] += self.speed[1]
            elif self.pos[1] < 90 * scale and self.speed[1] > 0:
                self.pos[1] += self.speed[1]
            elif bg.pos[1] >= 0 and self.speed[1] < 0:
                self.pos[1] += self.speed[1]
            elif bg.pos[1] <= -1328 * scale and self.speed[1] > 0:
                self.pos[1] += self.speed[1]
            else:                                   ## scrolling movement (y axis)
                bg.pos[1] -= self.speed[1]
                clickDest[1] -= self.speed[1]
                for pos in bg.posList:
                    pos[1] -= self.speed[1]
                for heart in heartList:
                    heart.pos[1] -= self.speed[1]
                for grass in grassList:
                    grass.pos[1] -= self.speed[1]
                for rock in rockList:
                    rock.pos[1] -= self.speed[1]
                for weapon in weaponList:
                    weapon.pos[1] -= self.speed[1]
                for bullet in self.bulletList:
                    bullet.pos[1] -= self.speed[1]
                for guy in shootGuyList:
                    guy.pos[1] -= self.speed[1]
                    for bullet in guy.bulletList:
                        bullet.pos[1] -= self.speed[1]
                for brain in brainList:
                    brain.pos[1] -= self.speed[1]
                    for bullet in brain.bulletList:
                        bullet.pos[1] -= self.speed[1]
                for summoner in summonerList:
                    summoner.pos[1] -= self.speed[1]
                for dragon in dragonList:
                    dragon.pos[1] -= self.speed[1]
                    if dragon.flame:
                        dragon.flamePos[1] -= self.speed[1]
                for ghost in ghostList:
                    ghost.pos[1] -= self.speed[1]
                    if ghost.skull:
                        ghost.skullPos[1] -= self.speed[1]
                for dude in badDudeList:
                    dude.pos[1] -= self.speed[1]
                for pup in pupList:
                    pup.pos[1] -= self.speed[1]
                for pup in goodPupList:
                    pup.pos[1] -= self.speed[1]
                if bg.level == stairsLevel:
                    stairsPos[1] -= self.speed[1]
                if bg.level == 'beach':
                    shipPos[1] -= self.speed[1]
                    stairsPos2[1] -= self.speed[1]
                if bg.level == 'saturn1':
                    shipPos2[1] -= self.speed[1]
                if bg.level == stairsLevel2:
                    stairsPos3[1] -= self.speed[1]
                if bg.level == 'desert1':
                    stairsPos4[1] -= self.speed[1]
            if abs(self.pos[0] + self.middle - clickDest[0]) < 4 * scale and abs(self.pos[1] + self.middle - clickDest[1]) < 4 * scale:
                self.walking = False        ## stopping player movement when within range of click destination
                self.walkTimer = 0
                self.speed[0] = 0
                self.speed[1] = 0

        if self.left:                       ## frame selection when facing left
            if self.walking and self.walkTimer < 140:
                self.frame = 8
            elif self.idle and self.idleTimer < 200:
                self.frame = 8
            elif self.idle and self.idleTimer >= 200:
                self.frame = 7
            elif self.walking and self.walkTimer >= 140:
                self.frame = 6
            if self.shooting:
                if self.weapon != 2:
                    if self.shootTimer < self.maxShootTimer - 250:
                        self.frame = 5
                    elif self.shootTimer >= self.maxShootTimer - 250 and self.shootTimer < self.maxShootTimer - 200:
                        self.frame = 4
                    elif self.shootTimer >= self.maxShootTimer - 200 and self.shootTimer < self.maxShootTimer - 150:
                        self.frame = 3
                    elif self.shootTimer >= self.maxShootTimer - 150 and self.shootTimer < self.maxShootTimer - 100:
                        self.frame = 2
                    elif self.shootTimer >= self.maxShootTimer - 100 and self.shootTimer < self.maxShootTimer - 50:
                        self.frame = 1
                    elif self.shootTimer >= self.maxShootTimer - 50:
                        self.frame = 0
                else:
                    if self.shootTimer < self.maxShootTimer - 80:
                        self.frame = 5
                    elif self.shootTimer >= self.maxShootTimer - 80 and self.shootTimer < self.maxShootTimer - 65:
                        self.frame = 4
                    elif self.shootTimer >= self.maxShootTimer - 65 and self.shootTimer < self.maxShootTimer - 45:
                        self.frame = 3
                    elif self.shootTimer >= self.maxShootTimer - 45 and self.shootTimer < self.maxShootTimer - 30:
                        self.frame = 2
                    elif self.shootTimer >= self.maxShootTimer - 30 and self.shootTimer < self.maxShootTimer - 15:
                        self.frame = 1
                    elif self.shootTimer >= self.maxShootTimer - 15:
                        self.frame = 0
        else:                           ## frame selection when facing right
            if self.walking and self.walkTimer < 140:
                self.frame = 0
            elif self.idle and self.idleTimer < 200:
                self.frame = 0
            elif self.idle and self.idleTimer >= 200:
                self.frame = 1
            elif self.walking and self.walkTimer >= 140:
                self.frame = 2
            if self.shooting:
                if self.weapon != 2:
                    if self.shootTimer < self.maxShootTimer - 250:
                        self.frame = 3
                    elif self.shootTimer >= self.maxShootTimer - 250 and self.shootTimer < self.maxShootTimer - 200:
                        self.frame = 4
                    elif self.shootTimer >= self.maxShootTimer - 200 and self.shootTimer < self.maxShootTimer - 150:
                        self.frame = 5
                    elif self.shootTimer >= self.maxShootTimer - 150 and self.shootTimer < self.maxShootTimer - 100:
                        self.frame = 6
                    elif self.shootTimer >= self.maxShootTimer - 100 and self.shootTimer < self.maxShootTimer - 50:
                        self.frame = 7
                    elif self.shootTimer >= self.maxShootTimer - 50:
                        self.frame = 8
                else:
                    if self.shootTimer < self.maxShootTimer - 80:
                        self.frame = 3
                    elif self.shootTimer >= self.maxShootTimer - 80 and self.shootTimer < self.maxShootTimer - 65:
                        self.frame = 4
                    elif self.shootTimer >= self.maxShootTimer - 65 and self.shootTimer < self.maxShootTimer - 45:
                        self.frame = 5
                    elif self.shootTimer >= self.maxShootTimer - 45 and self.shootTimer < self.maxShootTimer - 30:
                        self.frame = 6
                    elif self.shootTimer >= self.maxShootTimer - 30 and self.shootTimer < self.maxShootTimer - 15:
                        self.frame = 7
                    elif self.shootTimer >= self.maxShootTimer - 15:
                        self.frame = 8
        
        DISPLAYSURF.blit(self.image, self.pos, (self.frame * 32 * scale, 0, 32 * scale, 32 * scale))  ## drawing player
        
        for bullet in self.bulletList:          ## updating players bullets
            bullet.update()
            if bullet.remove:
                self.bulletList.remove(bullet)
                break
        ShowHp(self)
        if self.target2[0] > -1:            ## player's target positioning and drawing
            if self.target2[0] == 0:
                self.arrow2Pos = [dragonList[self.target2[1]].pos[0] + (30 * scale), dragonList[self.target2[1]].pos[1] - 12 * scale]
            if self.target2[0] == 1:
                self.arrow2Pos = [brainList[self.target2[1]].pos[0] + (8 * scale), brainList[self.target2[1]].pos[1] - 12 * scale]
            if self.target2[0] == 2:
                self.arrow2Pos = [shootGuyList[self.target2[1]].pos[0] + (8 * scale), shootGuyList[self.target2[1]].pos[1] - 12 * scale]
            if self.target2[0] == 3:
                self.arrow2Pos = [ghostList[self.target2[1]].pos[0] + (8 * scale), ghostList[self.target2[1]].pos[1] - 12 * scale]
            if self.target2[0] == 4:
                self.arrow2Pos = [summonerList[self.target2[1]].pos[0] + (8 * scale), summonerList[self.target2[1]].pos[1] - 12 * scale]
            if self.target2[0] == 5:
                self.arrow2Pos = [badDudeList[self.target2[1]].pos[0] + (8 * scale), badDudeList[self.target2[1]].pos[1] - 12 * scale]
            DISPLAYSURF.blit(self.arrowImage2, self.arrow2Pos, (self.arrowFrame * 16 * scale, 0, 16 * scale, 14 * scale))

        if self.target[0] > -1:
            self.arrowTimer += timePassed
            if self.arrowTimer > 200:
                self.arrowTimer = 0
            if self.arrowTimer < 50:
                self.arrowFrame = 0
            elif self.arrowTimer >= 50 and self.arrowTimer < 100:
                self.arrowFrame = 1
            elif self.arrowTimer >= 100 and self.arrowTimer < 150:
                self.arrowFrame = 2
            elif self.arrowTimer >= 150:
                self.arrowFrame = 3
            if self.target[0] == 0:
                self.arrowPos = [dragonList[self.target[1]].pos[0] + (30 * scale), dragonList[self.target[1]].pos[1] - 12 * scale]
            if self.target[0] == 1:
                self.arrowPos = [brainList[self.target[1]].pos[0] + (8 * scale), brainList[self.target[1]].pos[1] - 12 * scale]
            if self.target[0] == 2:
                self.arrowPos = [shootGuyList[self.target[1]].pos[0] + (8 * scale), shootGuyList[self.target[1]].pos[1] - 12 * scale]
            if self.target[0] == 3:
                self.arrowPos = [ghostList[self.target[1]].pos[0] + (8 * scale), ghostList[self.target[1]].pos[1] - 12 * scale]
            if self.target[0] == 4:
                self.arrowPos = [summonerList[self.target[1]].pos[0] + (8 * scale), summonerList[self.target[1]].pos[1] - 12 * scale]
            if self.target[0] == 5:
                self.arrowPos = [badDudeList[self.target[1]].pos[0] + (8 * scale), badDudeList[self.target[1]].pos[1] - 12 * scale]
            DISPLAYSURF.blit(self.arrowImage, self.arrowPos, (self.arrowFrame * 16 * scale, 0, 16 * scale, 14 * scale))

princess = Princess()  ## create instance of player

class Weapon():
    def __init__(self, pos, weapon):
        self.image = pygame.image.load('weaponboxes.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (128 * scale, 32 * scale))
        self.pos = pos
        self.weapon = weapon
        self.wasWeapon = weapon
        self.canPickup = True
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
    def update(self):
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
        if self.rect.colliderect(princess.rect):
            if self.canPickup:
                self.weapon = princess.weapon
                princess.weapon = self.wasWeapon
                self.canPickup = False
                princess.image = pygame.image.load('cowboy' + str(princess.weapon + 1) + '.png').convert_alpha()
                princess.image = pygame.transform.scale(princess.image, (288 * scale, 32 * scale)).convert_alpha()
                if princess.weapon == 0:        ## different damages and fire rates of different player guns
                    princess.dmg = 5
                    princess.maxShootTimer = princess.initMaxShootTimer * 4
                elif princess.weapon == 1:
                    princess.dmg = 16
                    princess.maxShootTimer = princess.initMaxShootTimer * 8
                elif princess.weapon == 2:
                    princess.dmg = 2
                    princess.maxShootTimer = princess.initMaxShootTimer
                elif princess.weapon == 3:
                    princess.dmg = 8
                    princess.maxShootTimer = princess.initMaxShootTimer * 6
                if princess.left:
                    princess.image = pygame.transform.flip(princess.image, 1, 0)
        else:
            self.canPickup = True
            self.wasWeapon = self.weapon

        DISPLAYSURF.blit(self.image, self.pos, (self.weapon * 32 * scale, 0, 32 * scale, 32 * scale))
        
class Pup():
    def __init__(self, pos, color, following):
        self.image = pygame.image.load('Dog.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (160 * scale, 320 * scale)).convert_alpha()
        self.hpImage = pygame.image.load('health.png').convert_alpha()
        self.hpImage = pygame.transform.scale(self.hpImage, (40 * scale, 10 * scale)).convert_alpha()
        self.expImage = pygame.image.load('exp.png').convert_alpha()
        self.expImage = pygame.transform.scale(self.expImage, (40 * scale, 10 * scale)).convert_alpha()
        self.borderImage = pygame.image.load('border2.png').convert_alpha()
        self.borderImage = pygame.transform.scale(self.borderImage, (40 * scale, 10 * scale)).convert_alpha()
        self.pos = pos
        self.attacking = False
        self.attacked = False
        self.following = following
        self.walking = False
        self.left = False
        self.level = 1
        self.exp = 0
        self.showExp = False
        self.lvlSound =  pygame.mixer.Sound('lvlUp.ogg')
        self.expTimer = 0
        self.walkTimer = 0
        self.attackTimer = 0
        self.attackSound = pygame.mixer.Sound('pupAttack.ogg')
        self.attackSound.set_volume(0.6)
        self.attackSound2 = pygame.mixer.Sound('pupAttack2.ogg')
        self.attackSound2.set_volume(0.6)
        self.speed = [0, 0]
        self.color = color
        self.accel = 3 * scale
        self.frame = 0
        self.hp = 70
        self.maxHp = 70
        self.showHp = False
        self.hpTimer = 0
        self.dmg = 4
        self.target = [-1, -1]
        self.remove = False
        self.removeTimer = 0
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
    def update(self):
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
        self.bottomRect = Rect(self.pos[0] + (12 * scale), self.pos[1] + (30 * scale), 8 * scale, 4 * scale)
        self.topRect = Rect(self.pos[0] + (12 * scale), self.pos[1] + (8 * scale), 8 * scale, 4 * scale) 
        self.rightRect = Rect(self.pos[0] + (20 * scale), self.pos[1] + (18 * scale), 4 * scale, 6 * scale)
        self.leftRect = Rect(self.pos[0] + (2 * scale), self.pos[1] + (18 * scale), 4 * scale, 6 * scale)
        
        self.agroRect = Rect(self.pos[0] - 80 * scale, self.pos[1] - 80 * scale, 180 * scale, 180 * scale)

        if self.left == False and self.speed[0] < 0:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.left = True
        if self.left and self.speed[0] > 0:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.left = False
        if self.rect.colliderect(princess.rect):
            self.following = True
            self.walking = True
        if self.walking:
            self.walkTimer += timePassed
            if self.walkTimer > 240:
                self.walkTimer = 0
        self.pos[0] += self.speed[0]        ## pup movement
        self.pos[1] += self.speed[1]

        if self.speed[0] != 0 or self.speed[1] != 0:
            CheckEdge(self)
        
        for heart in heartList:     ## pups pick up health if health is low enough
            if self.rect.colliderect(heart.rect) and self.hp < self.maxHp - 20:
                self.hp = self.maxHp
                self.showHp = True
                self.hpTimer = 0
                heart.remove = True
                break

        if self.attacking:
            self.attackTimer += timePassed
            self.speed[0] = 0
            self.speed[1] = 0
            if self.attackTimer > 200:
                self.attackTimer = 0
                self.attacking = False
                self.attacked = True
        if self.following:      ## pups after being retrieved, in their following state
            if princess.target[0] > -1 and princess.target2[0] == -1:
                    self.target[0] = princess.target[0]
                    self.target[1] = princess.target[1]
            elif princess.target2[0] > -1:
                    self.target[0] = princess.target2[0]
                    self.target[1] = princess.target2[1]
                    
            if self.target[1] == -1:  ## movement when pups have no target
                if self.speed[0] == 0 and random.randint(1, 99) > 30:
                    self.speed[0] = random.randint(-2 * scale, 2 * scale)
                if self.speed[1] == 0 and random.randint(1, 99) > 30:
                    self.speed[1] = random.randint(-2 * scale, 2 * scale)
                    
                if self.pos[0] < princess.pos[0] - (40 * scale):
                    self.speed[0] = random.randint(1 * scale, 3 * scale)
                elif self.pos[0] > princess.pos[0] + (40 * scale):
                    self.speed[0] = random.randint(-3 * scale, -1 * scale)
                if self.pos[1] < princess.pos[1] - (40 * scale):
                    self.speed[1] = random.randint(1 * scale, 3 * scale)
                elif self.pos[1] > princess.pos[1] + (40 * scale):
                    self.speed[1] = random.randint(-3 * scale, -1 * scale)
                if abs(self.pos[0] - princess.pos[0]) < 40 * scale:
                    if random.randint(1, 99) > 66:
                        self.speed[0] = 0
                if abs(self.pos[1] - princess.pos[1]) < 40 * scale:
                    if random.randint(1, 99) > 66:
                        self.speed[1] = 0
                
                if princess.target[0] == -1 and princess.target2[0] == -1:       ## pup automatic targeting when player and pup 
                        i = 0                                                   ## have no target
                        for dragon in dragonList:
                                if self.agroRect.colliderect(dragon.rect):
                                        self.target = [0, i]
                                i += 1
                        i = 0
                        for brain in brainList:
                                if self.agroRect.colliderect(brain.rect):
                                        self.target = [1, i]
                                i += 1
                        i = 0
                        for guy in shootGuyList:
                                if self.agroRect.colliderect(guy.rect):
                                        self.target = [2, i]
                                i += 1
                        i = 0
                        for ghost in ghostList:
                                if self.agroRect.colliderect(ghost.rect):
                                        self.target = [3, i]
                                i += 1
                        i = 0
                        for summoner in summonerList:
                                if self.agroRect.colliderect(summoner.rect):
                                        self.target = [4, i]
                                i += 1
                        
                        i = 0
                        for dude in badDudeList:
                                if self.agroRect.colliderect(dude.rect):
                                        self.target = [5, i]
                                i += 1
            else:                       ## pup movement when they have a target
                if self.speed[0] == 0 and self.attacking == False:
                    self.speed[0] = random.randint(-3 * scale, 3 * scale)
                if self.speed[1] == 0 and self.attacking == False:
                    self.speed[1] = random.randint(-3 * scale, 3 * scale)
                    
                if self.target[0] == 0:     ## attacking, flipping, killing when health below 0, and moving for each different enemy type
                    if self.rect.colliderect(dragonList[self.target[1]].rect):      ## could use function to clean this up...
                        self.attacking = True
                        if self.left and self.pos[0] < dragonList[self.target[1]].pos[0] + 32 * scale:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = False
                        if self.left == False and self.pos[0] > dragonList[self.target[1]].pos[0] + 32 * scale:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = True
                        if self.attacked:
                            if random.randint(1, 2) == 1:
                                self.attackSound.play()
                            else:
                                self.attackSound2.play()
                            dragonList[self.target[1]].hp -= self.dmg
                            self.attacked = False
                            dragonList[self.target[1]].showHp = True
                            dragonList[self.target[1]].hpTimer = 0
                        if dragonList[self.target[1]].hp <= 0:
                            dragonList.remove(dragonList[self.target[1]])
                            ClearPupTarget(self)
                            self.target = [-1, -1]
                    else:
                        if self.pos[0] < dragonList[self.target[1]].pos[0] - 32 * scale:
                            self.speed[0] = self.accel
                        elif self.pos[0] > dragonList[self.target[1]].pos[0] + 64 * scale:
                            self.speed[0] = -self.accel
                        if self.pos[1] < dragonList[self.target[1]].pos[1] - 32 * scale:
                            self.speed[1] = self.accel
                        elif self.pos[1] > dragonList[self.target[1]].pos[1] + 64 * scale:
                            self.speed[1] = -self.accel
                elif self.target[0] == 1:
                    if self.rect.colliderect(brainList[self.target[1]].rect):
                        self.attacking = True
                        if self.left and self.pos[0] < brainList[self.target[1]].pos[0] + 16 * scale:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = False
                        if self.left == False and self.pos[0] > brainList[self.target[1]].pos[0] + 16 * scale:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = True
                        if self.attacked:
                            if random.randint(1, 2) == 1:
                                self.attackSound.play()
                            else:
                                self.attackSound2.play()
                            brainList[self.target[1]].hp -= self.dmg
                            self.attacked = False
                            brainList[self.target[1]].showHp = True
                            brainList[self.target[1]].hpTimer = 0
                        if brainList[self.target[1]].hp <= 0:
                            brainList.remove(brainList[self.target[1]])
                            ClearPupTarget(self)
                            self.target = [-1, -1]
                    else:
                        if self.pos[0] < brainList[self.target[1]].pos[0] - 32 * scale:
                            self.speed[0] = self.accel
                        elif self.pos[0] > brainList[self.target[1]].pos[0] + 64 * scale:
                            self.speed[0] = -self.accel
                        if self.pos[1] < brainList[self.target[1]].pos[1] - 32 * scale:
                            self.speed[1] = self.accel
                        elif self.pos[1] > brainList[self.target[1]].pos[1] + 64 * scale:
                            self.speed[1] = -self.accel
                if self.target[0] == 2:
                    if self.rect.colliderect(shootGuyList[self.target[1]].rect):
                        self.attacking = True
                        if self.left and self.pos[0] < shootGuyList[self.target[1]].pos[0] + 16 * scale:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = False
                        if self.left == False and self.pos[0] > shootGuyList[self.target[1]].pos[0] + 16 * scale:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = True
                        if self.attacked:
                            if random.randint(1, 2) == 1:
                                self.attackSound.play()
                            else:
                                self.attackSound2.play()
                            shootGuyList[self.target[1]].hp -= self.dmg
                            self.attacked = False
                            shootGuyList[self.target[1]].showHp = True
                            shootGuyList[self.target[1]].hpTimer = 0
                        if shootGuyList[self.target[1]].hp <= 0:
                            shootGuyList.remove(shootGuyList[self.target[1]])
                            ClearPupTarget(self)
                            self.target = [-1, -1]
                    
                    else:
                        if self.pos[0] < shootGuyList[self.target[1]].pos[0] - 32 * scale:
                            self.speed[0] = self.accel
                        elif self.pos[0] > shootGuyList[self.target[1]].pos[0] + 64 * scale:
                            self.speed[0] = -self.accel
                        if self.pos[1] < shootGuyList[self.target[1]].pos[1] - 32 * scale:
                            self.speed[1] = self.accel
                        elif self.pos[1] > shootGuyList[self.target[1]].pos[1] + 64 * scale:
                            self.speed[1] = -self.accel
   
                if self.target[0] == 3:
                    if self.rect.colliderect(ghostList[self.target[1]].rect):
                        self.attacking = True
                        if self.left and self.pos[0] < ghostList[self.target[1]].pos[0] + 16 * scale:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = False
                        if self.left == False and self.pos[0] > ghostList[self.target[1]].pos[0] + 16 * scale:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = True
                        if self.attacked:
                            if random.randint(1, 2) == 1:
                                self.attackSound.play()
                            else:
                                self.attackSound2.play()
                            ghostList[self.target[1]].hp -= self.dmg
                            self.attacked = False
                            ghostList[self.target[1]].showHp = True
                            ghostList[self.target[1]].hpTimer = 0
                        if ghostList[self.target[1]].hp <= 0:
                            ghostList.remove(ghostList[self.target[1]])
                            ClearPupTarget(self)
                            self.target = [-1, -1]
                    else:
                        if self.pos[0] < ghostList[self.target[1]].pos[0] - 32 * scale:
                            self.speed[0] = self.accel
                        elif self.pos[0] > ghostList[self.target[1]].pos[0] + 64 * scale:
                            self.speed[0] = -self.accel
                        if self.pos[1] < ghostList[self.target[1]].pos[1] - 32 * scale:
                            self.speed[1] = self.accel
                        elif self.pos[1] > ghostList[self.target[1]].pos[1] + 64 * scale:
                            self.speed[1] = -self.accel
                
                if self.target[0] == 4:
                    if self.rect.colliderect(summonerList[self.target[1]].rect):
                        self.attacking = True
                        if self.left and self.pos[0] < summonerList[self.target[1]].pos[0] + 16 * scale:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = False
                        if self.left == False and self.pos[0] > summonerList[self.target[1]].pos[0] + 16 * scale:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = True
                        if self.attacked:
                            if random.randint(1, 2) == 1:
                                self.attackSound.play()
                            else:
                                self.attackSound2.play()
                            summonerList[self.target[1]].hp -= self.dmg
                            self.attacked = False
                            summonerList[self.target[1]].showHp = True
                            summonerList[self.target[1]].hpTimer = 0
                        if summonerList[self.target[1]].hp <= 0:
                            summonerList.remove(summonerList[self.target[1]])
                            ClearPupTarget(self)
                            self.target = [-1, -1]
                    else:
                        if self.pos[0] < summonerList[self.target[1]].pos[0] - 32 * scale:
                            self.speed[0] = self.accel
                        elif self.pos[0] > summonerList[self.target[1]].pos[0] + 64 * scale:
                            self.speed[0] = -self.accel
                        if self.pos[1] < summonerList[self.target[1]].pos[1] - 32 * scale:
                            self.speed[1] = self.accel
                        elif self.pos[1] > summonerList[self.target[1]].pos[1] + 64 * scale:
                            self.speed[1] = -self.accel  

                if self.target[0] == 5:
                    if self.rect.colliderect(badDudeList[self.target[1]].rect):
                        self.attacking = True
                        if self.left and self.pos[0] < badDudeList[self.target[1]].pos[0] + 16 * scale:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = False
                        if self.left == False and self.pos[0] > badDudeList[self.target[1]].pos[0] + 16 * scale:
                            self.image = pygame.transform.flip(self.image, 1, 0)
                            self.left = True
                        if self.attacked:
                            if random.randint(1, 2) == 1:
                                self.attackSound.play()
                            else:
                                self.attackSound2.play()
                            badDudeList[self.target[1]].hp -= self.dmg
                            self.attacked = False
                            badDudeList[self.target[1]].showHp = True
                            badDudeList[self.target[1]].hpTimer = 0
                        if badDudeList[self.target[1]].hp <= 0:
                            badDudeList.remove(badDudeList[self.target[1]])
                            ClearPupTarget(self)
                            self.target = [-1, -1]
                    else:
                        if self.pos[0] < badDudeList[self.target[1]].pos[0] - 32 * scale:
                            self.speed[0] = self.accel
                        elif self.pos[0] > badDudeList[self.target[1]].pos[0] + 64 * scale:
                            self.speed[0] = -self.accel
                        if self.pos[1] < badDudeList[self.target[1]].pos[1] - 32 * scale:
                            self.speed[1] = self.accel
                        elif self.pos[1] > badDudeList[self.target[1]].pos[1] + 64 * scale:
                            self.speed[1] = -self.accel
   
        if self.showExp:
            self.expTimer += timePassed
        if self.expTimer > 600:         ## showing experience bar and leveling up, for pups!
            self.expTimer = 0
            self.showExp = False
        if self.exp > self.level * 100 and not self.remove:
            self.level += 1
            self.exp = 0
            self.maxHp += 5
            self.hp = self.maxHp
            self.showHp = True
            self.hpTimer = 0
            self.showExp = True
            self.expTimer = 0
            self.dmg += 1
            self.lvlSound.play()
        if self.left:           ## frame selection
            if self.attacking == False:
                if self.walkTimer < 120:
                    self.frame = 4
                if self.walkTimer >= 120:
                    self.frame = 3
            else:
                if self.attackTimer < 100:
                    self.frame = 2
                if self.attackTimer >= 100 and self.attackTimer < 150:
                    self.frame = 1
                if self.attackTimer >= 150:
                    self.frame = 0

        else:
            if self.attacking == False:
                if self.walkTimer < 120:
                    self.frame = 0
                if self.walkTimer >= 120:
                    self.frame = 1
            else:
                if self.attackTimer < 100:
                    self.frame = 2
                if self.attackTimer >= 100 and self.attackTimer < 150:
                    self.frame = 3
                if self.attackTimer >= 150:
                    self.frame = 4
        
        if self.remove:
            self.removeTimer += timePassed
        if self.pos[0] > -80 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale and not self.remove:
            DISPLAYSURF.blit(self.image, self.pos, (self.frame * 32 * scale, self.color * 32 * scale, 32 * scale, 32 * scale))
        ShowHp(self)
        if self.showExp and not self.remove:
            if self.exp > 0:
                self.expImage = pygame.transform.scale(self.expImage, ((self.exp / (self.level * 3) * scale + (4 * scale)) + 1, 10 * scale)).convert_alpha()
                DISPLAYSURF.blit(self.expImage, [self.pos[0] - (4 * scale), self.pos[1] - (6 * scale)])
            DISPLAYSURF.blit(self.borderImage, [self.pos[0] - (4 * scale), self.pos[1] - (6 * scale)])
            text = font.render(str(self.level), 1, white)
            DISPLAYSURF.blit(text, [self.pos[0] - (12 * scale), self.pos[1] - (6 * scale)])
class DragonSummoner():
    def __init__(self, pos):
        self.image = pygame.image.load('dragon summoner.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (160 * scale, 32 * scale)).convert_alpha()
        self.hpImage = pygame.image.load('health.png').convert_alpha()
        self.hpImage = pygame.transform.scale(self.hpImage, (40 * scale, 10 * scale)).convert_alpha()
        self.borderImage = pygame.image.load('border2.png').convert_alpha()
        self.borderImage = pygame.transform.scale(self.borderImage, (40 * scale, 10 * scale)).convert_alpha()
        self.pos = pos
        self.frame = 0
        self.hp = 30
        self.maxHp = 30
        self.dmg = 4
        self.idle = True
        self.idleTimer = 0
        self.attacking = False
        self.summonTimer = 0
        self.summoned = False
        self.showHp = False
        self.hpTimer = 0
        self.target = [-1, -1]
        self.remove = False
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
    def update(self):
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
        self.aggroRect = Rect(self.pos[0] - 64, self.pos[1] - 64, 192 * scale, 192 * scale)
        if self.idle:
            self.idleTimer += timePassed
            if self.idleTimer > 500:
                self.idleTimer = 0
        EnemyTarget(self)
        if self.attacking:
            self.idle = False
            self.idleTimer = 0
            self.summonTimer += timePassed
            if self.summonTimer > 300 and self.summoned == False:
                self.summoned = True
                dragonList.append(Dragon([random.randrange(int(self.pos[0] - (140 * scale)), int(self.pos[0] + (50 * scale)), 40 * scale), random.randrange(int(self.pos[1] - (140 * scale)), int(self.pos[1] + (50 * scale)), 90 * scale)]))
            if self.summonTimer > 1100:
                self.summonTimer = 0
                self.attacking = False
                self.summoned = False
                self.idle = True
                self.target = [-1, -1]
            
        if self.attacking == False:
            if self.idleTimer < 250:
                self.frame = 0
            elif self.idleTimer >= 250:
                self.frame = 1
        else:
            if self.summonTimer < 240 or self.summonTimer >= 390:
                self.frame = 0
            elif self.summonTimer >= 240 and self.summonTimer < 290:
                self.frame = 2
            elif self.summonTimer >= 290 and self.summonTimer < 340:
                self.frame = 3
            elif self.summonTimer >= 340 and self.summonTimer < 390:
                self.frame = 4

        if self.pos[0] > -100 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale:
            DISPLAYSURF.blit(self.image, self.pos, (self.frame * 32 * scale, 0, 32 * scale, 32 * scale))
        ShowHp(self)

class Dragon():
    def __init__(self, pos):
        self.image = pygame.image.load('dragon.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (256 * scale, 64 * scale)).convert_alpha()
        self.hpImage = pygame.image.load('health.png').convert_alpha()
        self.hpImage = pygame.transform.scale(self.hpImage, (40 * scale, 10 * scale)).convert_alpha()
        self.borderImage = pygame.image.load('border2.png').convert_alpha()
        self.borderImage = pygame.transform.scale(self.borderImage, (80 * scale, 10 * scale)).convert_alpha()
        self.pos = pos
        self.frame = 0
        self.hp = 40
        self.maxHp = 40
        self.dmg = 3
        self.left = False
        self.idle = True
        self.idleTimer = 0
        self.showHp = False
        self.hpTimer = 0
        self.flame = False
        self.flameSound = pygame.mixer.Sound('dragonFire.ogg')
        self.attacking = False
        self.attackTimer = 0
        self.attacked = False
        self.flamePos = [0, 0]
        self.flameSpeed = [0, 0]
        self.target = [-1, -1]
        self.angle = 0
        self.remove = False
        self.rect = Rect(self.pos[0], self.pos[1], 64 * scale, 64 * scale)
    def update(self):
        self.rect = Rect(self.pos[0] + (4 * scale), self.pos[1] + (4 * scale), 56 * scale, 56 * scale)
        self.aggroRect = Rect(self.pos[0] - (64 * scale), self.pos[1] - (64 * scale), 192 * scale, 192 * scale)

              
        EnemyTarget(self)
        if self.flame:
            if self.left:
                if self.target[0] == 0:
                    self.angle = math.degrees(math.atan2(self.pos[0] - (16 * scale) - princess.pos[0] - (16 * scale), self.pos[1] - princess.pos[1]))
                elif self.target[0] == 1:
                    self.angle = math.degrees(math.atan2(self.pos[0] - (16 * scale) - goodPupList[self.target[1]].pos[0] - (16 * scale), self.pos[1] - goodPupList[self.target[1]].pos[1]))
            else:
                if self.target[0] == 0:
                    self.angle = math.degrees(math.atan2(self.pos[0] + (48 * scale) - princess.pos[0] - (16 * scale), self.pos[1] - princess.pos[1]))
                elif self.target[0] == 1:
                    self.angle = math.degrees(math.atan2(self.pos[0] + (48 * scale) - goodPupList[self.target[1]].pos[0] - (16 * scale), self.pos[1] - goodPupList[self.target[1]].pos[1]))
            self.flameSpeed = [math.sin(math.radians(self.angle)) * -2 * scale, math.cos(math.radians(self.angle)) * -2 * scale]
            self.attackTimer += timePassed
            self.speed = [0, 0]
            self.flamePos[0] += self.flameSpeed[0]
            self.flamePos[1] += self.flameSpeed[1]
        else:
            if self.left:
                self.flamePos[0] = self.pos[0] - (32 * scale)
                self.flamePos[1] = self.pos[1]
            else:
                self.flamePos[0] = self.pos[0] + (32 * scale)
                self.flamePos[1] = self.pos[1]
        if self.attackTimer > 400:
            if self.left:
                self.flamePos[0] = self.pos[0] - (32 * scale)
                self.flamePos[1] = self.pos[1]
            else:
                self.flamePos[0] = self.pos[0] + (32 * scale)
                self.flamePos[1] = self.pos[1]
            self.attackTimer = 0
            self.flame = False
            self.attacked = True
        if self.target[0] == 0:
            if self.aggroRect.colliderect(princess.rect):
                self.flame = True
                if self.left and self.pos[0] < princess.pos[0]:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.left = False
                if self.left == False and self.pos[0] > princess.pos[0]:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.left = True
                if self.attacked:
                    self.flameSound.play()
                    princess.hp -= self.dmg
                    self.attacked = False
                    princess.showHp = True
                    princess.hpTimer = 0
                if  princess.hp <= 0:
                    self.target = [-1, -1]
        elif self.target[0] == 1:
            if self.aggroRect.colliderect(goodPupList[self.target[1]].rect):
                self.flame = True
                if self.left and self.pos[0] < goodPupList[self.target[1]].pos[0]:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.left = False
                if self.left == False and self.pos[0] > goodPupList[self.target[1]].pos[0]:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.left = True
                if self.attacked:
                    self.flameSound.play()
                    goodPupList[self.target[1]].hp -= self.dmg
                    self.attacked = False
                    goodPupList[self.target[1]].showHp = True
                    goodPupList[self.target[1]].hpTimer = 0
                if  goodPupList[self.target[1]].hp <= 0:
                    goodPupList[self.target[1]].remove = True

        if self.attackTimer == 0:
            self.idle = True
        else:
            self.idle = False
            self.idleTimer = 0
        if self.idle:
            self.idleTimer += timePassed
            if self.idleTimer > 800:
                self.idleTimer = 0

        if self.left:
            if self.idle:
                if self.idleTimer < 400:
                    self.frame = 3
                elif self.idleTimer >= 400:
                    self.frame = 2
            else:
                self.frame = 1
        else:
            if self.idle:
                if self.idleTimer < 400:
                    self.frame = 0
                elif self.idleTimer >= 400:
                    self.frame = 1
            else:
                self.frame = 2
            
        if self.pos[0] > -100 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale:
            DISPLAYSURF.blit(self.image, self.pos, (self.frame * 64 * scale, 0, 64 * scale, 64 * scale))
        if self.flame:
            if self.left:
                DISPLAYSURF.blit(self.image, self.flamePos, (0, 0, 64 * scale, 64 * scale))
            else:
                DISPLAYSURF.blit(self.image, self.flamePos, (3 * 64 * scale, 0, 64 * scale, 64 * scale))
        ShowHp(self)

class Brain():
    def __init__(self, pos):
        self.image = pygame.image.load('brain.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (96 * scale, 32 * scale)).convert_alpha()
        self.hpImage = pygame.image.load('health.png').convert_alpha()
        self.hpImage = pygame.transform.scale(self.hpImage, (40 * scale, 10 * scale)).convert_alpha()
        self.borderImage = pygame.image.load('border2.png').convert_alpha()
        self.borderImage = pygame.transform.scale(self.borderImage, (40 * scale, 10 * scale)).convert_alpha()
        self.pos = pos
        self.frame = 1
        self.hp = 30
        self.maxHp = 30
        self.dmg = 2
        self.showHp = False
        self.hpTimer = 0
        self.speed = [0, 0]
        self.target = [-1, -1]
        self.attacking = False
        self.attackTimer = 0
        self.bulletSound = pygame.mixer.Sound('brainBullet.ogg')
        self.winking = False
        self.winkTimer = 0
        self.bulletList = []
        self.remove = False

        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
    def update(self):
        self.middle = [self.pos[0] + (16 * scale), self.pos[1] + (16 * scale)]
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
        self.aggroRect = Rect(self.pos[0] - (32 * scale), self.pos[1] - (32 * scale), 96 * scale, 96 * scale)
        self.bottomRect = Rect(self.pos[0] + (12 * scale), self.pos[1] + (30 * scale), 8 * scale, 4 * scale)
        self.topRect = Rect(self.pos[0] + (12 * scale), self.pos[1] + (8 * scale), 8 * scale, 4 * scale) 
        self.rightRect = Rect(self.pos[0] + (20 * scale), self.pos[1] + (18 * scale), 4 * scale, 6 * scale)
        self.leftRect = Rect(self.pos[0] + (2 * scale), self.pos[1] + (18 * scale), 4 * scale, 6 * scale)
        EnemyTarget(self)
        if self.attacking:
            self.attackTimer += timePassed
        if self.attackTimer >= 450:
            if self.target[0] == 0:
                if self.pos[0] > -100 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale: 
                    self.bulletSound.play()
                self.bulletList.append(Bullet([self.pos[0] + (16 * scale), self.pos[1] + (16 * scale)], 4, math.degrees(math.atan2(self.pos[0] + (16 * scale) - princess.pos[0] - (16 * scale), self.pos[1] + (16 * scale) - princess.pos[1] - (16 * scale)))))
            elif self.target[0] == 1:
                if self.pos[0] > -100 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale: 
                    self.bulletSound.play()
                self.bulletList.append(Bullet([self.pos[0] + (16 * scale), self.pos[1] + (16 * scale)], 4, math.degrees(math.atan2(self.pos[0] + (16 * scale) - goodPupList[self.target[1]].pos[0] - (16 * scale), self.pos[1] + (16 * scale) - goodPupList[self.target[1]].pos[1] - (16 * scale))))) 
            self.attackTimer = 0
        for bullet in self.bulletList:
            if bullet.rect.colliderect(princess.rect):
                princess.showHp = True
                princess.hpTimer = 0
                princess.hp -= self.dmg
                bullet.remove = True
                break
        for bullet in self.bulletList:
            for pup in goodPupList:
                if bullet.rect.colliderect(pup.rect):
                    pup.showHp = True
                    pup.hpTimer = 0
                    pup.hp -= self.dmg
                    bullet.remove = True
                    if pup.hp <= 0:
                        pup.remove = True
                    break
                
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        if self.speed[0] != 0 or self.speed[1] != 0:
            CheckEdge(self)
        if self.pos[0] < -100 * scale or self.pos[0] > 600 * scale or self.pos[1] < -100 * scale or self.pos[1] > 500 * scale:
            self.speed = [0, 0]
        else:
            if random.randint(1, 100) > 87:
                self.speed[0] = random.randint(-3 * scale, 3 * scale)
            if random.randint(1, 100) > 87:
                self.speed[1] = random.randint(-3 * scale, 3 * scale)
        
        if self.attacking == False and self.winking == False:
            self.frame = 0
            if random.randint(1, 200) > 199:
                self.winking = True
                self.winkTimer = random.randint(1, 400)
        elif self.winking or self.attacking and self.attackTimer <= 200:
            self.frame = 1
            self.winkTimer += timePassed
        elif self.attacking and self.attackTimer > 200:
            self.frame = 2
        if self.winkTimer > 500:
            self.winkTimer = False
            self.winking = False
        if self.pos[0] > -100 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale: 
            DISPLAYSURF.blit(self.image, self.pos, (self.frame * 32 * scale, 0, 32 * scale, 32 * scale))
        ShowHp(self)
        for bullet in self.bulletList:
            bullet.update()
            if bullet.remove:
                self.bulletList.remove(bullet)
                break
class ShootingGuy():
    def __init__(self, pos):
        self.image = pygame.image.load('shooting guy.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (128 * scale, 32 * scale)).convert_alpha()
        self.hpImage = pygame.image.load('health.png').convert_alpha()
        self.hpImage = pygame.transform.scale(self.hpImage, (40 * scale, 10 * scale)).convert_alpha()
        self.borderImage = pygame.image.load('border2.png').convert_alpha()
        self.borderImage = pygame.transform.scale(self.borderImage, (40 * scale, 10 * scale)).convert_alpha()
        self.pos = pos
        self.frame = 0
        self.hp = 30
        self.maxHp = 30
        self.dmg = 3
        self.left = False
        self.shooting = False
        self.shootTimer = 0
        self.bulletSound = pygame.mixer.Sound('enemyBullet.ogg')
        self.showHp = False
        self.hpTimer = 0
        self.attacking = False
        self.attackTimer = 0
        self.shot = False
        self.target = [-1, -1]
        self.bulletList = []
        self.remove = False
        
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
    def update(self):
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
        self.aggroRect = Rect(self.pos[0] - (64 * scale), self.pos[1] - (64 * scale), 192 * scale, 192 * scale)
        self.bottomRect = Rect(self.pos[0] + (12 * scale), self.pos[1] + (30 * scale), 8 * scale, 4 * scale)
        self.topRect = Rect(self.pos[0] + (12 * scale), self.pos[1] + (8 * scale), 8 * scale, 4 * scale) 
        self.rightRect = Rect(self.pos[0] + (20 * scale), self.pos[1] + (18 * scale), 4 * scale, 6 * scale)
        self.leftRect = Rect(self.pos[0] + (2 * scale), self.pos[1] + (18 * scale), 4 * scale, 6 * scale)
        EnemyTarget(self)
        if self.attacking:
            self.attackTimer += timePassed
            if self.left:
                if self.target[0] == 0:
                    if self.pos[0] < princess.pos[0]:
                        self.image = pygame.transform.flip(self.image, 1, 0)
                        self.left = False
                if self.target[0] == 1:
                    if self.pos[0] < goodPupList[self.target[1]].pos[0]:
                        self.image = pygame.transform.flip(self.image, 1, 0)
                        self.left = False
            else:
                if self.target[0] == 0:
                    if self.pos[0] > princess.pos[0]:
                        self.image = pygame.transform.flip(self.image, 1, 0)
                        self.left = True
                if self.target[0] == 1:
                    if self.pos[0] > goodPupList[self.target[1]].pos[0]:
                        self.image = pygame.transform.flip(self.image, 1, 0)
                        self.left = True
        if self.attackTimer >= 200 and self.shot == False:
            if self.target[0] == 0:
                if self.pos[0] > -100 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale: 
                    self.bulletSound.play()
                self.bulletList.append(Bullet([self.pos[0] + (16 * scale), self.pos[1] + (16 * scale)], 5, math.degrees(math.atan2(self.pos[0] + (16 * scale) - princess.pos[0] - (16 * scale), self.pos[1] + (16 * scale) - princess.pos[1] - (16 * scale)))))
            elif self.target[0] == 1:
                if self.pos[0] > -100 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale: 
                    self.bulletSound.play()
                self.bulletList.append(Bullet([self.pos[0] + (16 * scale), self.pos[1] + (16 * scale)], 5, math.degrees(math.atan2(self.pos[0] + (16 * scale) - goodPupList[self.target[1]].pos[0] - (16 * scale), self.pos[1] + (16 * scale) - goodPupList[self.target[1]].pos[1] - (16 * scale))))) 
            self.shot = True
        if self.attackTimer > 800:
            self.shot = False
            self.attackTimer = 0
        for bullet in self.bulletList:
            if bullet.rect.colliderect(princess.rect):
                princess.showHp = True
                princess.hpTimer = 0
                princess.hp -= self.dmg
                bullet.remove = True
                break
        for bullet in self.bulletList:
            for pup in goodPupList:
                if bullet.rect.colliderect(pup.rect) and pup.following:
                    pup.showHp = True
                    pup.hpTimer = 0
                    pup.hp -= self.dmg
                    bullet.remove = True
                    if pup.hp <= 0:
                        pup.remove = True
                    break
        
        
        if self.attacking == False:
            self.frame = 0
            self.shot = False
            self.attackTimer = 0
        elif self.attacking:
            if self.attackTimer < 100:
                self.frame = 1
            elif self.attackTimer >= 100 and self.attackTimer < 200:
                self.frame = 2
            elif self.attackTimer >= 200:
                self.frame = 3
        if self.pos[0] > -100 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale:
            DISPLAYSURF.blit(self.image, self.pos, (self.frame * 32 * scale, 0, 32 * scale, 32 * scale))
        ShowHp(self)
        for bullet in self.bulletList:
            bullet.update()
            if bullet.remove:
                self.bulletList.remove(bullet)
                break

class Ghost():
    def __init__(self, pos):
        self.image = pygame.image.load('ghost.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (96 * scale, 32 * scale)).convert_alpha()
        self.skullImage = pygame.image.load('skull.png').convert_alpha()
        self.skullImage = pygame.transform.scale(self.skullImage, (64 * scale, 19 * scale)).convert_alpha()
        self.skullPos = [0, 0]
        self.skullFrame = 0
        self.pos = pos
        self.hpImage = pygame.image.load('health.png').convert_alpha()
        self.hpImage = pygame.transform.scale(self.hpImage, (40 * scale, 10 * scale)).convert_alpha()
        self.borderImage = pygame.image.load('border2.png').convert_alpha()
        self.borderImage = pygame.transform.scale(self.borderImage, (40 * scale, 10 * scale)).convert_alpha()
        self.frame = 0
        self.left = True
        self.hp = 40
        self.maxHp = 40
        self.dmg = 3
        self.showHp = False
        self.hpTimer = 0
        self.speed = [0, 0]
        self.accel = 2 * scale
        self.floatTimer = 0
        self.attacking = False
        self.attackTimer = 0
        self.skull = False
        self.skullSound = pygame.mixer.Sound('ghostSkull.ogg')
        self.attacked = False
        self.target = [-1, -1]
        self.angle = 0
        self.skullSpeed = [math.sin(math.radians(self.angle)) * -self.accel, math.cos(math.radians(self.angle)) * -self.accel]
        self.remove = False
        
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
    def update(self):
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
        self.aggroRect = Rect(self.pos[0] - (32 * scale), self.pos[1] - (32 * scale), 96 * scale, 96 * scale)
        self.bottomRect = Rect(self.pos[0] + (12 * scale), self.pos[1] + (30 * scale), 8 * scale, 4 * scale)
        self.topRect = Rect(self.pos[0] + (12 * scale), self.pos[1] + (8 * scale), 8 * scale, 4 * scale) 
        self.rightRect = Rect(self.pos[0] + (20 * scale), self.pos[1] + (18 * scale), 4 * scale, 6 * scale)
        self.leftRect = Rect(self.pos[0] + (2 * scale), self.pos[1] + (18 * scale), 4 * scale, 6 * scale)
        
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        if self.speed[0] != 0 or self.speed[1] != 0:
            CheckEdge(self)
        if self.left == False and self.speed[0] < 0:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.skullImage = pygame.transform.flip(self.skullImage, 1, 0)
            self.left = True
        if self.left and self.speed[0] > 0:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.skullImage = pygame.transform.flip(self.skullImage, 1, 0)
            self.left = False
            
        EnemyTarget(self)
        if self.skull:
            if self.target[0] == 0:
                self.angle = math.degrees(math.atan2(self.pos[0] + (16 * scale) - princess.pos[0] - (16 * scale), self.pos[1] + (16 * scale) - princess.pos[1] - (16 * scale)))
            elif self.target[0] == 1:
                self.angle = math.degrees(math.atan2(self.pos[0] + (16 * scale) - goodPupList[self.target[1]].pos[0] - (16 * scale), self.pos[1] + (16 * scale) - goodPupList[self.target[1]].pos[1] - (16 * scale)))
            self.skullSpeed = [math.sin(math.radians(self.angle)) * -2 * scale, math.cos(math.radians(self.angle)) * -2 * scale]
            self.attackTimer += timePassed
            self.speed = [0, 0]
            self.skullPos[0] += self.skullSpeed[0]
            self.skullPos[1] += self.skullSpeed[1]
        else:
            self.skullPos[0] = self.pos[0] + (8 * scale)
            self.skullPos[1] = self.pos[1] + (8 * scale)
        if self.attackTimer > 200:
            self.skullSound.play()
            self.attackTimer = 0
            self.skullPos[0] = self.pos[0] + (8 * scale)
            self.skullPos[1] = self.pos[1] + (8 * scale)
            self.skull = False
            self.attacked = True
        if self.target[0] == 0:
            if self.rect.colliderect(princess.rect):
                self.skull = True
                if self.left and self.pos[0] < princess.pos[0]:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.skullImage = pygame.transform.flip(self.skullImage, 1, 0)
                    self.left = False
                if self.left == False and self.pos[0] > princess.pos[0]:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.skullImage = pygame.transform.flip(self.skullImage, 1, 0)
                    self.left = True
                if self.attacked:
                    princess.hp -= self.dmg
                    self.attacked = False
                    princess.showHp = True
                    princess.hpTimer = 0
                if  princess.hp <= 0:
                    self.target = [-1, -1]
            else:
                if self.pos[0] < princess.pos[0] - 32 * scale:
                    self.speed[0] = self.accel
                elif self.pos[0] > princess.pos[0] + 64 * scale:
                    self.speed[0] = -self.accel
                if self.pos[1] < princess.pos[1] - 32 * scale:
                    self.speed[1] = self.accel
                elif self.pos[1] > princess.pos[1] + 64 * scale:
                    self.speed[1] = -self.accel
        elif self.target[0] == 1:
            if self.rect.colliderect(goodPupList[self.target[1]].rect):
                self.skull = True
                if self.left and self.pos[0] < goodPupList[self.target[1]].pos[0]:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.skullImage = pygame.transform.flip(self.skullImage, 1, 0)
                    self.left = False
                if self.left == False and self.pos[0] > goodPupList[self.target[1]].pos[0]:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.skullImage = pygame.transform.flip(self.skullImage, 1, 0)
                    self.left = True
                if self.attacked:
                    goodPupList[self.target[1]].hp -= self.dmg
                    self.attacked = False
                    goodPupList[self.target[1]].showHp = True
                    goodPupList[self.target[1]].hpTimer = 0
                if  goodPupList[self.target[1]].hp <= 0:
                    goodPupList[self.target[1]].remove = True
            else:
                if self.pos[0] < goodPupList[self.target[1]].pos[0] - 32 * scale:
                    self.speed[0] = self.accel
                elif self.pos[0] > goodPupList[self.target[1]].pos[0] + 64 * scale:
                    self.speed[0] = -self.accel
                if self.pos[1] < goodPupList[self.target[1]].pos[1] - 32 * scale:
                    self.speed[1] = self.accel
                elif self.pos[1] > goodPupList[self.target[1]].pos[1] + 64 * scale:
                    self.speed[1] = -self.accel
        if self.pos[0] < -100 * scale or self.pos[0] > 600 * scale or self.pos[1] < -100 * scale or self.pos[1] > 500 * scale:
            self.speed = [0, 0]
        elif self.target == [-1, -1]:
            if random.randint(1, 100) > 87:
                self.speed[0] = random.randint(-self.accel, self.accel)
            if random.randint(1, 100) > 87:
                self.speed[1] = random.randint(-self.accel, self.accel)
        elif self.target != [-1, -1]:
            if self.speed[0] == 0:
                if random.randint(1, 100) > 87:
                    self.speed[0] = random.randint(-self.accel, self.accel)
            if self.speed[1] == 0:
                if random.randint(1, 100) > 87:
                    self.speed[1] = random.randint(-self.accel, self.accel)
        
        self.floatTimer += timePassed
        if self.floatTimer > 150:
            self.floatTimer = 0

        if self.left:
            if self.floatTimer < 50:
                self.frame = 0
            if self.floatTimer >= 50 and self.floatTimer < 100:
                self.frame = 1
            if self.floatTimer >= 100:
                self.frame = 2
            if self.attackTimer < 50:
                self.skullFrame = 0
            elif self.attackTimer >= 50 and self.attackTimer < 100:
                self.skullFrame = 1
            elif self.attackTimer >= 100 and self.attackTimer < 150:
                self.skullFrame = 2
            elif self.attackTimer >= 150:
                self.skullFrame = 3
            
        else:
            if self.floatTimer < 50:
                self.frame = 2
            if self.floatTimer >= 50 and self.floatTimer < 100:
                self.frame = 1
            if self.floatTimer >= 100:
                self.frame = 0
            if self.attackTimer < 50:
                self.skullFrame = 3
            elif self.attackTimer >= 50 and self.attackTimer < 100:
                self.skullFrame = 2
            elif self.attackTimer >= 100 and self.attackTimer < 150:
                self.skullFrame = 1
            elif self.attackTimer >= 150:
                self.skullFrame = 0
        if self.pos[0] > -100 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale: 
            DISPLAYSURF.blit(self.image, self.pos, (self.frame * 32 * scale, 0, 32 * scale, 32 * scale))
        if self.skull:
            DISPLAYSURF.blit(self.skullImage, self.skullPos, (self.skullFrame * 16 * scale, 0, 16 * scale, 16 * scale))
        ShowHp(self)        
class BadDude():
    def __init__(self, pos):
        self.image = pygame.image.load('bad dude.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (192 * scale, 32 * scale)).convert_alpha()
        self.hpImage = pygame.image.load('health.png').convert_alpha()
        self.hpImage = pygame.transform.scale(self.hpImage, (40 * scale, 10 * scale)).convert_alpha()
        self.borderImage = pygame.image.load('border2.png').convert_alpha()
        self.borderImage = pygame.transform.scale(self.borderImage, (40 * scale, 10 * scale)).convert_alpha()
        self.pos = pos
        self.frame = 0
        self.left = False
        self.hp = 60
        self.maxHp = 60
        self.dmg = 3
        self.showHp = False
        self.hpTimer = 0
        self.speed = [0, 0]
        self.accel = 2 * scale
        self.walking = False
        self.walkTimer = 0
        self.idle = True
        self.idleTimer = 0
        self.attacking = False
        self.attackTimer = 0
        self.attacked = False
        self.attackSound = pygame.mixer.Sound('enemyAttack.ogg')
        self.attackSound.set_volume(0.5)
        self.swinging = False
        self.target = [-1, -1]
        self.remove = False

        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
    def update(self):
        self.rect = Rect(self.pos[0], self.pos[1], 32 * scale, 32 * scale)
        self.aggroRect = Rect(self.pos[0] - (32 * scale), self.pos[1] - (32 * scale), 96 * scale, 96 * scale)
        self.bottomRect = Rect(self.pos[0] + (12 * scale), self.pos[1] + (30 * scale), 8 * scale, 4 * scale)
        self.topRect = Rect(self.pos[0] + (12 * scale), self.pos[1] + (8 * scale), 8 * scale, 4 * scale) 
        self.rightRect = Rect(self.pos[0] + (20 * scale), self.pos[1] + (18 * scale), 4 * scale, 6 * scale)
        self.leftRect = Rect(self.pos[0] + (2 * scale), self.pos[1] + (18 * scale), 4 * scale, 6 * scale)

        if self.left == False and self.speed[0] < 0:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.left = True
        if self.left and self.speed[0] > 0:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.left = False
        EnemyTarget(self)
        if self.swinging:
            self.attackTimer += timePassed
            self.speed = [0, 0]
        if self.attackTimer > 300:
            self.attackTimer = 0
            self.swinging = False
            self.attacked = True
        if self.target[0] == 0:
            if self.rect.colliderect(princess.rect):
                self.swinging = True
                if self.left and self.pos[0] < princess.pos[0]:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.left = False
                if self.left == False and self.pos[0] > princess.pos[0]:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.left = True
                if self.attacked:
                    self.attackSound.play()
                    princess.hp -= self.dmg
                    self.attacked = False
                    princess.showHp = True
                    princess.hpTimer = 0
                if  princess.hp <= 0:
                    self.target = [-1, -1]
            else:
                if self.pos[0] < princess.pos[0] - 32 * scale:
                    self.speed[0] = self.accel
                elif self.pos[0] > princess.pos[0] + 64 * scale:
                    self.speed[0] = -self.accel
                if self.pos[1] < princess.pos[1] - 32 * scale:
                    self.speed[1] = self.accel
                elif self.pos[1] > princess.pos[1] + 64 * scale:
                    self.speed[1] = -self.accel
        elif self.target[0] == 1:
            if self.rect.colliderect(goodPupList[self.target[1]].rect):
                self.swinging = True
                if self.left and self.pos[0] < goodPupList[self.target[1]].pos[0]:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.left = False
                if self.left == False and self.pos[0] > goodPupList[self.target[1]].pos[0]:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                    self.left = True
                if self.attacked:
                    self.attackSound.play()
                    goodPupList[self.target[1]].hp -= self.dmg
                    self.attacked = False
                    goodPupList[self.target[1]].showHp = True
                    goodPupList[self.target[1]].hpTimer = 0
                if  goodPupList[self.target[1]].hp <= 0:
                    goodPupList[self.target[1]].remove = True
            else:
                if self.pos[0] < goodPupList[self.target[1]].pos[0] - 32 * scale:
                    self.speed[0] = self.accel
                elif self.pos[0] > goodPupList[self.target[1]].pos[0] + 64 * scale:
                    self.speed[0] = -self.accel
                if self.pos[1] < goodPupList[self.target[1]].pos[1] - 32 * scale:
                    self.speed[1] = self.accel
                elif self.pos[1] > goodPupList[self.target[1]].pos[1] + 64 * scale:
                    self.speed[1] = -self.accel
        if self.speed[0] != 0 or self.speed[1] != 0:
            CheckEdge(self)
        if self.pos[0] < -100 * scale or self.pos[0] > 600 * scale or self.pos[1] < -100 * scale or self.pos[1] > 500 * scale:
            self.speed = [0, 0]
        elif self.target == [-1, -1]:
            if random.randint(1, 100) > 87:
                self.speed[0] = random.randint(-self.accel, self.accel)
            if random.randint(1, 100) > 87:
                self.speed[1] = random.randint(-self.accel, self.accel)
        elif self.target != [-1, -1]:
            if self.speed[0] == 0:
                if random.randint(1, 100) > 87:
                    self.speed[0] = random.randint(-self.accel, self.accel)
            if self.speed[1] == 0:
                if random.randint(1, 100) > 87:
                    self.speed[1] = random.randint(-self.accel, self.accel)
                
        if self.speed != [0, 0]:
            self.walking = True
        else:
            self.walking = False
            
        if self.walking:
            self.idle = False
            self.idleTimer = 0
            self.walkTimer += timePassed
            self.pos[0] += self.speed[0]
            self.pos[1] += self.speed[1]
            if self.walkTimer > 160:
                self.walkTimer = 0
        elif self.attacking:
            self.idle = False
            self.idleTimer = 0
        else:
            self.idle = True
            self.idleTimer += timePassed
            if self.idleTimer > 200:
                self.idleTimer = 0
        if self.left:
            if self.swinging == False:
                if self.walking and self.walkTimer < 80:
                    self.frame = 5
                elif self.walking and self.walkTimer >= 80:
                    self.frame = 3
                elif self.idle and self.idleTimer < 100:
                    self.frame = 5
                elif self.idle and self.idleTimer >= 100:
                    self.frame = 4
            else:
                if self.attackTimer < 100:
                    self.frame = 2
                elif self.attackTimer >= 100 and self.attackTimer < 200:
                    self.frame = 1
                elif self.attackTimer >= 200:
                    self.frame = 0

        else:
            if self.swinging == False:
                if self.walking and self.walkTimer < 80:
                    self.frame = 0
                elif self.walking and self.walkTimer >= 80:
                    self.frame = 2
                elif self.idle and self.idleTimer < 100:
                    self.frame = 0
                elif self.idle and self.idleTimer >= 100:
                    self.frame = 1
            else:
                if self.attackTimer < 100:
                    self.frame = 3
                elif self.attackTimer >= 100 and self.attackTimer < 200:
                    self.frame = 4
                elif self.attackTimer >= 200:
                    self.frame = 5
            
        if self.pos[0] > -100 * scale and self.pos[0] < 500 * scale and self.pos[1] > -100 * scale and self.pos[1] < 400 * scale: 
            DISPLAYSURF.blit(self.image, self.pos, (self.frame * 32 * scale, 0, 32 * scale, 32 * scale))
        ShowHp(self)

bg = BG()    


while True: # main game loop
    pressed = pygame.key.get_pressed()
    timePassed = fpsClock.tick(60)
    click = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()
    if bg.level == stairsLevel:
        stairsRect = Rect(stairsPos[0] + (10 * scale), stairsPos[1] + (10 * scale), 30 * scale, 20 * scale)
    if bg.level == 'beach':
        shipRect = Rect(shipPos[0], shipPos[1], 96 * scale, 192 * scale)
        stairsRect2 = Rect(stairsPos2[0] + (10 * scale), stairsPos2[1] + (10 * scale), 30 * scale, 20 * scale)
    if bg.level == 'saturn1':
        shipRect = Rect(shipPos2[0], shipPos2[1], 96 * scale, 192 * scale)
    if bg.level == stairsLevel2:
        stairsRect3 = Rect(stairsPos3[0] + (10 * scale), stairsPos3[1] + (10 * scale), 30 * scale, 20 * scale)
    if bg.level == 'desert1':
        stairsRect4 = Rect(stairsPos4[0] + (10 * scale), stairsPos4[1] + (10 * scale), 30 * scale, 20 * scale)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key in [K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if CheckTarget()[0] >= 0:
                princess.walking = False
                princess.speed = [0, 0]
                princess.target2 = princess.target
                princess.target = CheckTarget()
                if princess.target2 == princess.target:
                    princess.target2 = [-1, -1]
            else:
                clickDest[0] = mouse[0]
                clickDest[1] = mouse[1]
                princess.angle = math.degrees(math.atan2(princess.pos[0] + princess.middle - mouse[0], princess.pos[1] + princess.middle - mouse[1]))
                princess.speed[0] = math.sin(math.radians(princess.angle)) * -princess.accel
                princess.speed[1] = math.cos(math.radians(princess.angle)) * -princess.accel
                princess.walking = True            
                if princess.left == False and princess.speed[0] < 0:
                    princess.image = pygame.transform.flip(princess.image, 1, 0)
                    princess.left = True
                if princess.left and princess.speed[0] > 0:
                    princess.image = pygame.transform.flip(princess.image, 1, 0)
                    princess.left = False
                princess.shooting = False
                princess.shootTimer = 0

    for bullet in princess.bulletList:          ## player bullets colliding with all enemy types
        for dragon in dragonList:               ## could clean this up with function too
            if bullet.rect.colliderect(dragon.rect):
                dragon.hp -= princess.dmg
                dragon.showHp = True
                dragon.hpTimer = 0
                if dragon.hp <= 0:
                    for pup in goodPupList:
                        pup.target = [-1, -1]
                        pup.showExp = True
                        pup.exp += 16
                    princess.target = [-1, -1]
                    princess.target2 = [-1, -1]
                    princess.shooting = False
                    princess.shootTimer = 0
                    dragon.remove = True
                bullet.remove = True
                break
    for bullet in princess.bulletList:
        for brain in brainList:
            if bullet.rect.colliderect(brain.rect):
                brain.hp -= princess.dmg
                brain.showHp = True
                brain.hpTimer = 0
                if brain.hp <= 0:
                    for pup in goodPupList:
                        pup.target = [-1, -1]
                        pup.showExp = True
                        pup.exp += 16
                    princess.target = [-1, -1]
                    princess.target2 = [-1, -1]
                    princess.shooting = False
                    princess.shootTimer = 0
                    brain.remove = True
                bullet.remove = True
                break
    for bullet in princess.bulletList:
        for guy in shootGuyList:
            if bullet.rect.colliderect(guy.rect):
                guy.hp -= princess.dmg
                guy.showHp = True
                guy.hpTimer = 0
                if guy.hp <= 0:
                    for pup in goodPupList:
                        pup.target = [-1, -1]
                        pup.showExp = True
                        pup.exp += 16
                    princess.target = [-1, -1]
                    princess.target2 = [-1, -1]
                    princess.shooting = False
                    princess.shootTimer = 0
                    guy.remove = True
                bullet.remove = True
                break
    for bullet in princess.bulletList:
        for ghost in ghostList:
            if bullet.rect.colliderect(ghost.rect):
                ghost.hp -= princess.dmg
                ghost.showHp = True
                ghost.hpTimer = 0
                if ghost.hp <= 0:
                    for pup in goodPupList:
                        pup.target = [-1, -1]
                        pup.showExp = True
                        pup.exp += 16
                    princess.target = [-1, -1]
                    princess.target2 = [-1, -1]
                    princess.shooting = False
                    princess.shootTimer = 0
                    ghost.remove = True
                bullet.remove = True
                break
    for bullet in princess.bulletList:
        for summoner in summonerList:
            if bullet.rect.colliderect(summoner.rect):
                summoner.hp -= princess.dmg
                summoner.showHp = True
                summoner.hpTimer = 0
                if summoner.hp <= 0:
                    for pup in goodPupList:
                        pup.target = [-1, -1]
                        pup.showExp = True
                        pup.exp += 16
                    princess.target = [-1, -1]
                    princess.target2 = [-1, -1]
                    princess.shooting = False
                    princess.shootTimer = 0
                    summoner.remove = True
                bullet.remove = True
                break
    for bullet in princess.bulletList:
        for dude in badDudeList:
            if bullet.rect.colliderect(dude.rect):
                dude.hp -= princess.dmg
                dude.showHp = True
                dude.hpTimer = 0
                if dude.hp <= 0:
                    for pup in goodPupList:
                        pup.target = [-1, -1]
                        pup.showExp = True
                        pup.exp += 16
                    princess.target = [-1, -1]
                    princess.target2 = [-1, -1]
                    princess.shooting = False
                    princess.shootTimer = 0
                    dude.remove = True
                bullet.remove = True
                break
    bg.update()                 ## drawing and updating everything
    if bg.level == stairsLevel:
        DISPLAYSURF.blit(stairsImage, stairsPos)
    if bg.level == 'beach':
        DISPLAYSURF.blit(shipImage, shipPos)
        DISPLAYSURF.blit(stairsImage, stairsPos2)
    if bg.level == 'saturn1':
        DISPLAYSURF.blit(shipImage, shipPos2)
    if bg.level == stairsLevel2:
        DISPLAYSURF.blit(stairsImage, stairsPos3)
    if bg.level == 'desert1':
        DISPLAYSURF.blit(stairsImage, stairsPos4)
    for weapon in weaponList:
        weapon.update()
    for rock in rockList:
        rock.update()
    for guy in shootGuyList:
        guy.update()
        if guy.remove:
            shootGuyList.remove(guy)
            break
    for summoner in summonerList:
        summoner.update()
        if summoner.remove:
            summonerList.remove(summoner)
            break
    for dragon in dragonList:
        dragon.update()
        if dragon.remove:
            dragonList.remove(dragon)
            break
    for brain in brainList:
        brain.update()
        if brain.remove:
            brainList.remove(brain)
            break
    for ghost in ghostList:
        ghost.update()
        if ghost.remove:
            ghostList.remove(ghost)
            break
    for dude in badDudeList:
        dude.update()
        if dude.remove:
            badDudeList.remove(dude)
            break
    for pup in pupList:
        pup.update()
        if pup.following:
            goodPupList.append(Pup([pup.pos[0], pup.pos[1]], pup.color, True))
            pupList.remove(pup)
            break
    for pup in goodPupList:
        pup.update()
        if pup.remove and pup.removeTimer > 80:
            ClearEnemyTarget()
            deadPupSound.play()
            goodPupList.remove(pup)
            break
    princess.update()
    for grass in grassList:
        grass.update()
        grass.draw()
    for heart in heartList:
        heart.update()
        if heart.remove:
            heartList.remove(heart)
            break
    if showCrosshair:
        DISPLAYSURF.blit(mouseImage, [mouse[0] - (8 * scale), mouse[1] - (8 * scale)])
    pygame.display.flip()
    fpsClock.tick(60)
