import pygame
import csv

pygame.init()                                                                               
clock = pygame.time.Clock()

font = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 20)
font_sub = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 50)
font_title = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 70)
font_titleL = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 100)
font_titleLarge = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 150)

backG = pygame.image.load("img/backgrounds/backgroundLarge.png")

nextB = pygame.image.load("img/buttons/nextB.png")

input_box = pygame.Rect(460, 700, 1000, 64)                                                  

black = (0,0,0)
darkGrey = (50,50,50)
white = (255,255,255)

def printLeaderboard(gameDisplay,fps):
    leaderboardArray = []
    leaderboard = open("csv/leaderboard.csv")
    check = csv.reader(leaderboard)
    for x in check:
        leaderboardArray.append(x[0])
        leaderboardArray.append(x[1])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 1280 <= mouse[0] <= 1510 and 790 <= mouse[1] <= 870:
                    return False
                
        d = {}
        for x in range(0,20,2):
            d["string{0}".format(x)] = leaderboardArray[x]
        d2 = {}
        for x in range(1,20,2):
            d2["string{0}".format(x)] = leaderboardArray[x]
                        
        gameDisplay.blit(backG, (0,0))
        lb1_text = font_title.render(d["string0"],True,white)
        lb2_text = font_title.render(d["string2"],True,white)
        lb3_text = font_title.render(d["string4"],True,white)
        lb4_text = font_title.render(d["string6"],True,white)
        lb5_text = font_title.render(d["string8"],True,white)
        lb6_text = font_title.render(d["string10"],True,white)
        lb7_text = font_title.render(d["string12"],True,white)
        lb8_text = font_title.render(d["string14"],True,white)
        lb9_text = font_title.render(d["string16"],True,white)
        lb10_text = font_title.render(d["string18"],True,white)

        lb11_text = font_title.render(d2["string1"],True,white)
        lb12_text = font_title.render(d2["string3"],True,white)
        lb13_text = font_title.render(d2["string5"],True,white)
        lb14_text = font_title.render(d2["string7"],True,white)
        lb15_text = font_title.render(d2["string9"],True,white)
        lb16_text = font_title.render(d2["string11"],True,white)
        lb17_text = font_title.render(d2["string13"],True,white)
        lb18_text = font_title.render(d2["string15"],True,white)
        lb19_text = font_title.render(d2["string17"],True,white)
        lb20_text = font_title.render(d2["string19"],True,white)

        gameDisplay.blit(lb1_text, (100,200))
        gameDisplay.blit(lb2_text, (100,275))
        gameDisplay.blit(lb3_text, (100,350))
        gameDisplay.blit(lb4_text, (100,425))
        gameDisplay.blit(lb5_text, (100,500))
        gameDisplay.blit(lb6_text, (100,575))
        gameDisplay.blit(lb7_text, (100,650))
        gameDisplay.blit(lb8_text, (100,725))
        gameDisplay.blit(lb9_text, (100,800))
        gameDisplay.blit(lb10_text, (100,875))

        gameDisplay.blit(lb11_text, (800,200))
        gameDisplay.blit(lb12_text, (800,275))
        gameDisplay.blit(lb13_text, (800,350))
        gameDisplay.blit(lb14_text, (800,425))
        gameDisplay.blit(lb15_text, (800,500))
        gameDisplay.blit(lb16_text, (800,575))
        gameDisplay.blit(lb17_text, (800,650))
        gameDisplay.blit(lb18_text, (800,725))
        gameDisplay.blit(lb19_text, (800,800))
        gameDisplay.blit(lb20_text, (800,875))
    
        menu_text7 = font_title.render("Return", True, white)
        pygame.draw.rect(gameDisplay, darkGrey, [1290, 800, 220 , 60])
        gameDisplay.blit(menu_text7, (1304,811))
        menu_text8 = font_titleLarge.render("LEADERBOARD",True,white)
        gameDisplay.blit(menu_text8, (50,30))
        pygame.display.update()                                                                 
        clock.tick(fps)

def writeScores(score,gameDisplay,fps,username):
    writeScore = True
    while writeScore is True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 0 <= mouse[0] <= 1920 and 0 <= mouse[1] <= 1080:
                        writeScore = False
                        break
        
        gameDisplay.blit(backG, (0,0))
        menu_text9 = font_titleLarge.render(" Your score has been saved",True,white)
        gameDisplay.blit(menu_text9, (50,50))
        gameDisplay.blit(nextB, (1600,800))
        pygame.display.update()                                                                 
        clock.tick(fps)
    
    leaderboard = open("csv/leaderboard.csv", "at")
    leaderboard.write(username+","+str(score)+"\n")
    leaderboard.close()
    
