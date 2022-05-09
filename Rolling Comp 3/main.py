### LIBS ###

import pygame                                                                                
import time                                                                                 
import csv
import random
import menu as m
import leaderboard as lb
import question as q

    
### INITIALISATION ###

pygame.init()                                                                               
clock = pygame.time.Clock()                                                                 

### GLOBALS ###

tile_size = 30
level = 1
end_level = 1
next_level = False
counter, timer_text = 60, "TIME: "
score, score_text = 0, "SCORE: 0"
input_box = pygame.Rect(460, 700, 1000, 64)
pygame.time.set_timer(pygame.USEREVENT, 1000)
text = ""
active = False
username = ""
qIndex = 0
aIndex = 0
health = 200


### COLOURS ###

color_inactive = pygame.Color("azure4")
color_active = pygame.Color("azure2")
color = color_inactive
darkGrey = (25,25,25)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)

### BACKGROUNDS ###

backG = pygame.image.load("img/backgrounds/background.png")
backG2 = pygame.image.load("img/backgrounds/backgroundLarge.png")
questionScreen = pygame.image.load("img/backgrounds/questionScreen.png")

### BUTTONS ###

pauseB = pygame.image.load("img/buttons/pauseB.png")
nextB = pygame.image.load("img/buttons/nextB.png")

### IMAGES ###

logo = pygame.image.load("img/misc/logo.png")

### FONTS ###

font = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 20)
font2 = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 50)
font3 = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 70)
font4 = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 150)

### SOUNDS ###

pygame.mixer.music.load("sounds/background_music.wav")
pygame.mixer.music.play(-1)
coin_sound = pygame.mixer.Sound("sounds/coin_collect.wav")
death_sound = pygame.mixer.Sound("sounds/death.wav")
nextLevel_sound = pygame.mixer.Sound("sounds/nextLevel.wav")
win_sound = pygame.mixer.Sound("sounds/win.wav")

### DISPLAY ###

height, width = 1080, 1920                                                                 
fps = 60
gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)                                      
pygame.display.set_caption("B A C K G R O U N D")                                                    

### FUNCTIONS ###

def reset(level,world_data,world,p1,spawnx,spawny):
    p1.reset(spawnx+30,spawny+30)                                                                           
    start_group.empty()
    exit_group.empty()
    enemy_group.empty()
    coin_group.empty()
    with open(f"levels/level_{level}.txt") as textFile:
        world_data = [line.split() for line in textFile]

    world = World(world_data)

    return world

    
### CLASSES ###

class World():
    def __init__(self,data):
        self.tile_list = []

        wall = pygame.image.load("img/world/TEXTURE1.png")                                            
        light_wall = pygame.image.load("img/world/TEXTURE2.png")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == "1":
                    img = pygame.transform.scale(wall, (tile_size + 1, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "2":
                    img = pygame.transform.scale(light_wall, (tile_size + 1, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size 
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "3":
                    start = Start((col_count * tile_size) + 1, row_count * tile_size)
                    start_group.add(start)
                if tile == "4":
                    exit = Exit(col_count * tile_size+1, row_count * tile_size)
                    exit_group.add(exit)
                if tile == "5":
                    enemy = Enemy(col_count * tile_size, row_count * tile_size)
                    enemy_group.add(enemy)
                if tile == "6":
                    coin = Coin(col_count * tile_size, row_count * tile_size)
                    coin_group.add(coin)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            gameDisplay.blit(tile[0], tile[1])

class Player:                                                                               
    def __init__(self,x,y):                                                                 
        self.player1_img = pygame.image.load("img/players/p1.png")                                  
        self.rect = self.player1_img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.player1_img.get_width()
        self.height = self.player1_img.get_height()
        self.pressed = False
	
    def update(self,next_level):                                                           

        dx,dy = 0,0                                                                         

        coolDown = 0

        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_a] is True:                                                 
            dx -= 3
        if key_pressed[pygame.K_d] is True:
            dx += 3
        if key_pressed[pygame.K_s] is True:                                                 
            dy += 3
        if key_pressed[pygame.K_w] is True:                                                 
            dy -= 3

        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy = 0

        if pygame.sprite.spritecollide(self,exit_group,False):
            nextLevel_sound.play()
            next_level = True

        if pygame.sprite.spritecollide(self,enemy_group,False):
            death_sound.play()
            reset(level,world_data,world,p1,spawnx,spawny)

        self.rect.x += dx
        self.rect.y += dy

        gameDisplay.blit(self.player1_img, self.rect)

        return next_level

    def reset(self,x,y):
        self.player1_img = pygame.image.load("img/players/p1.png")                              
        self.rect = self.player1_img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.player1_img.get_width()
        self.height = self.player1_img.get_height()
        self.pressed = False


class Start(pygame.sprite.Sprite):
    def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load("img/world/TEXTURE3.png")
            self.image = pygame.transform.scale(img, (tile_size+58, tile_size+60))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def getPos(self):
        return self.rect.x, self.rect.y
            

class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load("img/world/TEXTURE4.png")
            self.image = pygame.transform.scale(img, (tile_size +59, tile_size+60))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("img/world/TEXTURE5.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size - 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("img/world/TEXTURE6.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


### TILE MAP ###

with open(f"levels/level_{level}.txt") as textFile:
    world_data = [line.split() for line in textFile]


### INSTANCES ###

score = 0                                                                     

exit_group = pygame.sprite.Group()
start_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

world = World(world_data)

sprite = start_group.sprites()[0]
spawnx,spawny = sprite.getPos()

p1 = Player(spawnx + 30, spawny + 30)


### UPDATE LOOP ###

play = False                                                                                                                                           
running = True
question = False
menu1 = True
menu2 = False

while running:

    while menu1 is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                                               
                running = False
                pygame.quit()
                quit()
                                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 0 <= mouse[0] <= 1920 and 0 <= mouse[1] <= 1080:
                    menu1 = False
                    play = m.subMenu(gameDisplay,fps)
                    username = m.login(score,text,color,color_active,color_inactive,active,gameDisplay,fps)
                    qIndex, aIndex = m.difficulty(aIndex,qIndex,gameDisplay,fps)
                    if qIndex == 0:
                        diff_text = "DIFFICULTY: Easy"
                    elif qIndex == 1:
                        diff_text = "DIFFICULTY: Normal"
                    else:
                        diff_text = "DIFFICULTY: Hard"
                    break
                
        if play is True:
            break

        gameDisplay.blit(backG2, (0,0))
        pygame.draw.rect(gameDisplay, darkGrey, [575, 150, 770, 110])
        main_text = ("BACKGROUND")
        gameDisplay.blit(font4.render(main_text, True, (255, 255, 255)), (587, 165))
        pygame.draw.rect(gameDisplay, darkGrey ,[560, 780, 800, 60])
        menu_text2 = font3.render("CLICK ANYWHERE TO BEGIN...", True, white)
        gameDisplay.blit(menu_text2, (570,790))
        pygame.display.update()                                                                         
        clock.tick(fps)


    if play is True:                    
        if next_level is False and counter >= 0:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    counter -= 1
                    timer_text = ("TIME: "+str(counter))
                    
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 0 <= mouse[0] <= 1920 and 0 <= mouse[1] <= 1080:
                        print("Pause")
                        pause = m.pauseM(gameDisplay,fps)
                        if pause == "option":
                            m.optionsM(gameDisplay,fps)
                                                
            gameDisplay.blit(backG, (0,0))                                                              

            world.draw()                                                                                

            if pygame.sprite.spritecollide(p1, coin_group, True):
                coin_sound.play()
                question = True

            if pygame.sprite.spritecollide(p1 ,enemy_group,False):
                health -= 20
                if health == 0:
                    while True:                                                             
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse = pygame.mouse.get_pos()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if 0 <= mouse[0] <= 1920 and 0 <= mouse[1] <= 1080:
                                        lb.writeScores(score,gameDisplay,fps,username)
                                        m.endScreen(gameDisplay,fps)
                                        running = False
                                        break

                            if event.type == pygame.QUIT:                                                               
                                running = False
                                pygame.quit()
                                quit()
                                
                            break
                        
                        end_text = ("YOU HAVE DIED")
                        gameDisplay.blit(backG2 ,(0,0))
                        gameDisplay.blit(font4.render(end_text, True, (255, 255, 255)), (50, 50))
                        gameDisplay.blit(nextB, (1600, 800))
                        pygame.display.update()
                        clock.tick(fps)
                

            exit_group.draw(gameDisplay)
            start_group.draw(gameDisplay)
            enemy_group.draw(gameDisplay)
            coin_group.draw(gameDisplay)

            next_level = p1.update(next_level)
            username_text = ("PLAYER: "+username)
            health_text = ("HEALTH: "+str(health))
            timer_text = ("TIME: "+str(counter))
            pygame.draw.rect(gameDisplay,darkGrey,[0,900,1920,180])
            gameDisplay.blit(font2.render(timer_text, True, (255, 255, 255)), (700, 950))
            gameDisplay.blit(font2.render(score_text, True, (255, 255, 255)), (700, 920))
            gameDisplay.blit(font3.render(username_text, True, white), (15,930))
            gameDisplay.blit(font2.render(diff_text, True, (255, 255, 255)), (700, 1010))
            gameDisplay.blit(font2.render(health_text, True, white), (700, 980))
            gameDisplay.blit(pauseB, (1750,915))
            pygame.draw.rect(gameDisplay, red, [15,1000,200,50])
            pygame.draw.rect(gameDisplay, green, [15,1000,health,50])
            pygame.display.update()                                                                     
            clock.tick(fps)                                                                             

        elif next_level is True and counter >= 0:
            if level == end_level:
                win_sound.play()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse = pygame.mouse.get_pos()
                            if 725 <= mouse[0] <= 1070 and 690 <= mouse[1] <= 770:
                                lb.writeScores(score,gameDisplay,fps,username)
                                m.endScreen(gameDisplay,fps)
                                pygame.quit
                                quit()
                                
                        if event.type == pygame.QUIT:                                                       
                            running = False
                            pygame.quit()
                            quit()

                    endGame_text = ("YOU HAVE WON")
                    gameDisplay.blit(backG2, (0,0))
                    gameDisplay.blit(font4.render(endGame_text, True, (255, 255, 255)), (50, 50))
                    pygame.draw.rect(gameDisplay, darkGrey, [735, 700, 350 , 66])
                    scoreButton_text = font3.render("SAVE SCORE", True, white)
                    gameDisplay.blit(scoreButton_text, (745,715))
                    pygame.display.update()   
                        
            else:
                level += 1
                print(counter)
                world_data = []
                world = reset(level,world_data,world,p1,spawnx,spawny)
                next_level = False

        else:
            death_sound.play()
            while True:                                                             
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if 0 <= mouse[0] <= 600 and 0 <= mouse[1] <= 600:
                                lb.writeScores(score,gameDisplay,fps,username)

                    if event.type == pygame.QUIT:                                                               
                        running = False
                        pygame.quit()
                        quit()
                        
                    break
                
                end_text = ("O U T   O F   T I M E")
                gameDisplay.fill(black)
                gameDisplay.blit(font.render(end_text, True, (255, 255, 255)), (200, 280))
                pygame.display.update()
                clock.tick(fps)


    if next_level is False and question is True:
        question_text = q.getQuestion(qIndex)
        randNum = random.randint(0,5)                                                  
        question_text = str(question_text[randNum])
        questionAnswer = q.getAnswer(randNum,aIndex)
        questionAnswer = str(questionAnswer[randNum])
        print(questionAnswer)     
        while question is True:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    counter -= 1
                    timer_text = ("TIME: "+str(counter))
                    if counter == 0:
                        death_sound.play()
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:                                                               
                                    running = False
                                    pygame.quit()
                                    quit()
                                    break
                                
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse = pygame.mouse.get_pos()
                                    if 0 <= mouse[0] <= 1920 and 0 <= mouse[1] <= 1080:
                                        lb.writeScores(score,gameDisplay,fps,username)
                                        m.endScreen(gameDisplay,fps)
                                        pygame.quit()
                                        quit()
                                        break
                                                                
                            end_text = ("OUT OF TIME")
                            gameDisplay.blit(backG2, (0,0))
                            gameDisplay.blit(font4.render(end_text, True, (255, 255, 255)), (50, 50))
                            gameDisplay.blit(nextB, (1600,800))
                            pygame.display.update()
                            clock.tick(fps)

                    if event.type == pygame.QUIT:                                                                           
                        running = False
                        pygame.quit()
                        quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if 140 <= mouse[0] <= 400 and 690 <= mouse[1] <= 790:
                            score -= 1
                            score_text = ("SCORE: "+str(score))
                            active = False
                            text = ""
                            question = False
                            break
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active is True:
                        if event.key == pygame.K_RETURN:
                            print(text)
                            if text.lower() == questionAnswer.lower():
                                print("Correct")
                                score += 1
                                score_text = ("SCORE: "+str(score))
                                active = False
                                question = False
                                text = ""
                                color = color_inactive
                                break
                            else:
                                print("Incorrect")
                                score -= 1
                                active = False
                                text = ""
                                color = color_inactive
                                                            
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
                break

            
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
            gameDisplay.blit(questionScreen, (0,0))
            txt_surface = font3.render(text, True, color)                                        
            width = max(1000, txt_surface.get_width()+10)                                        
            input_box.w = width
            gameDisplay.blit(txt_surface, (input_box.x+5, input_box.y+5))                       
            pygame.draw.rect(gameDisplay, color, input_box, 3)                                  
            gameDisplay.blit(font3.render(question_text, True, (255, 255, 255)), (80, 70))
            pygame.draw.rect(gameDisplay, darkGrey, [150, 700, 250 , 50])
            button_text = font2.render("PASS (-1)", True, white)
            gameDisplay.blit(button_text, (167,710))
            pygame.draw.rect(gameDisplay,darkGrey,[0,900,1920,180])
            username_text = ("PLAYER: "+username)
            health_text = ("HEALTH: "+str(health))
            timer_text = ("TIME: "+str(counter))
            gameDisplay.blit(font2.render(timer_text, True, (255, 255, 255)), (700, 950))
            gameDisplay.blit(font2.render(score_text, True, (255, 255, 255)), (700, 920))
            gameDisplay.blit(font3.render(username_text, True, white), (15,930))
            gameDisplay.blit(font2.render(diff_text, True, (255, 255, 255)), (700, 1010))
            gameDisplay.blit(font2.render(health_text, True, white), (700, 980))
            pygame.draw.rect(gameDisplay, red, [15,1000,200,50])
            pygame.draw.rect(gameDisplay, green, [15,1000,health,50])
            pygame.display.update()                                                             
            clock.tick(fps)
                
        
    for event in pygame.event.get():
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:                                                           
            running = False
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 1760 <= mouse[0] <= 1920 and 900 <= mouse[1] <= 1080:
                pause = m.pauseM(gameDisplay,fps)
                if pause == "option":
                    m.optionsM(gameDisplay,fps)


pygame.quit()                                                                                   
quit()
