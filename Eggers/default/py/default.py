'''
Developed by: Jismanjeet Singh
Description: Game "Egger".
'''
import pygame
import pygame.time
import random
pygame.init()
GAME_TITLE = "EGGERS"
SCREEN_RESOLUTION = (800, 600)
SCREEN = pygame.display.set_mode(SCREEN_RESOLUTION)

def main():
    LEVEL = 0
    GAMEOVER = False
    PLAYING = False
    keepGoing = True
    loading = SCBACKGROUND(keepGoing)
    collectedEggs = Score(50,100,"Collected:")
    brokenEggs = Score(50,150,"Missed:")
    level = Score(50,200,"Level:")
    back = Back()
    plyr = Basket()
    activeSpriteGroup = pygame.sprite.Group()
    game_back = pygame.sprite.OrderedUpdates(loading)
    level1 = pygame.sprite.Group(Egg(),Egg())
    level2 = pygame.sprite.Group(Egg(),Egg(),Egg())
    level3 = pygame.sprite.Group(Egg(),Egg(),Egg(),Egg())
    level4 = pygame.sprite.Group(Egg(),Egg(),Egg(),Egg(),Egg())
    while keepGoing: 
        totalCollctdEggs = collectedEggs.getScore()
        totalBrknEggs = brokenEggs.getScore()
        if totalBrknEggs>=50:
            plyr.gameOver.play()
            back.changeBackImage("gameover.jpg")
            collectedEggs.changeDxDy(350, 185)
            brokenEggs.changeDxDy(350, 230)
            level.changeDxDy(350, 280)
            collectedEggs.changeText("")
            brokenEggs.changeText("")
            level.changeText("")
            PLAYING = False
            GAMEOVER = True
            game_back = pygame.sprite.OrderedUpdates(back,collectedEggs,brokenEggs,level)
        if LEVEL == 1:
            if totalCollctdEggs>=100 and totalCollctdEggs<200:
                game_back = pygame.sprite.OrderedUpdates(back,collectedEggs,
                                                             brokenEggs,level,plyr,
                                                             level2)
                activeSpriteGroup = level2
                plyr.changeBasket("level2.jpg")
                level.setScore(2)
                plyr.setMaxLR(130,590)
                plyr.levelUp.play()
                LEVEL=2
        if LEVEL == 2:
            if totalCollctdEggs>=200 and totalCollctdEggs<300:
                LEVEL=3
                game_back = pygame.sprite.OrderedUpdates(back,collectedEggs,
                                                             brokenEggs,level,plyr,
                                                             level3)
                activeSpriteGroup = level3
                plyr.changeBasket("level3.jpg")
                level.setScore(3)
                plyr.setMaxLR(130, 620)
                plyr.levelUp.play()
        if LEVEL == 3:
            if totalCollctdEggs>=300 and totalCollctdEggs<400:
                LEVEL=4
                game_back = pygame.sprite.OrderedUpdates(back,collectedEggs,
                                                             brokenEggs,level,plyr,
                                                             level4)
                activeSpriteGroup = level4
                plyr.changeBasket("level4.jpg")
                level.setScore(4)
                plyr.setMaxLR(130, 630)
                plyr.levelUp.play()
        if PLAYING:
            collision = pygame.sprite.spritecollide(plyr, activeSpriteGroup, False)
            if collision:
                for egg in collision:
                    collectedEggs.incr_score()
                    plyr.collect.play()
                    egg.reset()
            for egg in activeSpriteGroup:
                if egg.getEggDy()>608:
                    plyr.broken.play()
                    brokenEggs.incr_score()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing=False
            elif event.type == pygame.KEYDOWN:
                if LEVEL==0:
                    activeSpriteGroup = level1
                    game_back = pygame.sprite.OrderedUpdates(back,collectedEggs,
                                                             brokenEggs,level,plyr,
                                                             level1)
                    level.setScore(1)
                    LEVEL = 1
                    PLAYING = True
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                if (event.key == pygame.K_RETURN) and GAMEOVER:
                    if __name__ == "__main__": main()
        game_back.update()
        game_back.draw(SCREEN)
        pygame.display.flip()
    
class Egg(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        x=1
        self.imagePack = []
        self.touchGround = 0
        while x<=7:
            self.imagePack.append(pygame.image.load(str(x)+".jpg").convert()) 
            x+=1
        self.speed = 1
        self.reset()
    def reset(self):
        self.image = self.imagePack[random.randrange(0,6)]
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(130,640)
        self.rect.top = -random.randrange(300,900)
        
    def update(self):
        self.rect.top += self.speed
        if self.rect.top >=610:
            self.touchGround+=1
            self.reset()
    def getEggDy(self):
        return self.rect.top
            
class Basket(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("level1.jpg").convert()
        self.rect = self.image.get_rect()
        self.rect.left = 146
        self.rect.top = 530
        self.maxLeft = 130
        self.maxRight = 550
        self.myEvent = pygame.USEREVENT + 2
        if not pygame.mixer:
            print("problem with sound files")
        else:
            pygame.mixer.init()
            self.collect = pygame.mixer.Sound("audio/collect.wav")
            self.broken = pygame.mixer.Sound("audio/broken.wav")
            self.gameOver = pygame.mixer.Sound("audio/gameover.wav")
            self.back = pygame.mixer.Sound("audio/back.wav")
            self.back.play()
            pygame.time.set_timer(self.myEvent, 14000)
            self.levelUp = pygame.mixer.Sound("audio/levelUp.mp3")
    def update(self):
        keys = pygame.key.get_pressed()
        steps = 1
        if pygame.event.get(self.myEvent):
            self.back.play()
        if(keys):
            if keys[pygame.K_LEFT] and self.rect.left > self.maxLeft:
                self.rect.left -= steps
            elif keys[pygame.K_RIGHT] and self.rect.left < self.maxRight:
                self.rect.left += steps
    def setMaxLR(self,a,b):
        self.maxLeft = a
        self.maxRight = b
    def changeBasket(self,given):
        self.image = pygame.image.load(given).convert()
class Score(pygame.sprite.Sprite):
    def __init__(self,x,y,text):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.stat_text = text
        self.font = pygame.font.SysFont("Arial", 20)
        self.dx = x
        self.dy = y
    def update(self):
        self.text = "%d" % (self.score)
        self.image = self.font.render(self.stat_text+self.text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.dx,self.dy)
    def setScore(self,val):
        self.score = val
    def getScore(self):
        return self.score
    def incr_score(self):
        self.score += 1
    def changeDxDy(self,tempx,tempy):
        self.dx = tempx
        self.dy = tempy
    def changeText(self,temp):
        self.stat_text = temp

class Back(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("back.jpg")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.dy = 5
        self.reset()
    def reset(self):
        self.rect.bottom = SCREEN.get_height()
    def changeBackImage(self,img):
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()    
class SCBACKGROUND(pygame.sprite.Sprite):
    def __init__(self,keepGoing):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("default.jpg").convert()
        self.rect = self.image.get_rect()
        self.change = True
        self.MOVEUP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MOVEUP,50)
        self.speed = 0
        self.x = 0
        self.y = 0
        self.move = True
    def update(self):
        self.rect.top -= self.y
        if(pygame.event.get(self.MOVEUP) and self.move):
            self.y = 2
            self.moving = False
        if(self.rect.top == -620):
            self.y = 0
if __name__ == "__main__": main()