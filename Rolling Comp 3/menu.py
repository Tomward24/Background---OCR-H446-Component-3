import pygame
import leaderboard as lb
import csv

pygame.init()                                                                               
clock = pygame.time.Clock()

font = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 20)
font_sub = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 50)
font_title = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 70)
font_titleL = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 100)
font_titleLarge = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 150)

input_box = pygame.Rect(460, 700, 1000, 64)                                                  

backG = pygame.image.load("img/backgrounds/backgroundLarge.png")

black = (0,0,0)
darkGrey = (50,50,50)
white = (255,255,255)

def subMenu(gameDisplay,fps):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 735 <= mouse[0] <= 1175 and 540 <= mouse[1] <= 620:
                    leaderboard = lb.printLeaderboard(gameDisplay,fps)
                    if leaderboard is False:
                        break

                if 865 <= mouse[0] <= 1035 and 690 <= mouse[1] <= 770:
                    print("Quit")
                    pygame.quit()
                    quit()

                if 840 <= mouse[0] <= 1070 and 390 <= mouse[1] <= 470:
                    return True
                    break
            break

        gameDisplay.blit(backG, (0,0))
        menu_text3 = font_title.render("START", True, white)
        menu_text4 = font_title.render("LEADERBOARD", True, white)
        menu_text5 = font_title.render("QUIT", True, white)
        menu_text6 = font_titleLarge.render("MENU", True, white)
        pygame.draw.rect(gameDisplay, darkGrey, [850, 400, 220 , 60])
        pygame.draw.rect(gameDisplay, darkGrey, [745, 550, 430 , 60])
        pygame.draw.rect(gameDisplay, darkGrey, [875, 700, 170 , 60])
        gameDisplay.blit(menu_text3, (870,410))
        gameDisplay.blit(menu_text4, (765,560))
        gameDisplay.blit(menu_text5, (895,710))
        gameDisplay.blit(menu_text6, (50, 50))
        pygame.display.update()                                                                 
        clock.tick(fps)

def endScreen(gameDisplay,fps):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 0 <= mouse[0] <= 1600 and 0 <= mouse[1] <= 900:
                    pygame.quit()
                    quit()

        gameDisplay.blit(backG, (0,0))
        end_text2 = font_titleL.render("THANK YOU FOR PLAYING...", True, white)
        gameDisplay.blit(end_text2, (50,50))
        end_text3 = font_titleLarge.render("B A C K G R O U N D", True, white)
        gameDisplay.blit(end_text3, (500,325))
        end_text4 = font_title.render("CLICK ANYWHERE TO EXIT", True, white)
        gameDisplay.blit(end_text4, (660,900))
        pygame.display.update()                                                                     
        clock.tick(fps)

def difficulty(aIndex,qIndex,gameDisplay,fps):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 825 <= mouse[0] <= 1095 and 390 <= mouse[1] <= 470:
                    return 0,0
                if 825 <= mouse[0] <= 1095 and 590 <= mouse[1] <= 670:
                    return 1,1
                if 825 <= mouse[0] <= 1095 and 790 <= mouse[1] <= 870:
                    return 2,2

        gameDisplay.blit(backG, (0,0))  
        menu_text1 = font_titleLarge.render("SELECT A DIFFICULTY", True, white)
        gameDisplay.blit(menu_text1, (50,50))
        pygame.draw.rect(gameDisplay, darkGrey, [835, 400, 250 , 60])
        pygame.draw.rect(gameDisplay, darkGrey, [835, 600, 250 , 60])
        pygame.draw.rect(gameDisplay, darkGrey, [835, 800, 250 , 60])
        menu_text2 = font_title.render("EASY", True, white)
        gameDisplay.blit(menu_text2, (885,413))
        menu_text3 = font_title.render("NORMAL", True, white)
        gameDisplay.blit(menu_text3, (850,613))
        menu_text4 = font_title.render("HARD", True, white)
        gameDisplay.blit(menu_text4, (885,813))
        pygame.display.update()                                                                     
        clock.tick(fps)

def login(score,text,color,color_active,color_inactive,active,gameDisplay,fps):
    text = ""
    active = False
    login = True
    try_again = False
    found = False
    usernames = open("csv/usernames.csv")
    check_usernames = csv.reader(usernames)
    while login is True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 0 <= mouse[0] <= 100 and 0 <= mouse[1] <= 100:
                        login = False
                        break
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active is True and found is False:
                    if event.key == pygame.K_RETURN:
                        for x in check_usernames:
                            if text.lower() == x[0].lower():
                                print("F")
                                found = True
                                return text
                            
                        if found is False:
                            print("NF")
                            text = ""
                            try_again = True
                            usernames = open("csv/usernames.csv")
                            check_usernames = csv.reader(usernames)
                        
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            break
        
        gameDisplay.blit(backG, (0,0))
        txt_surface = font_titleL.render(text, True, color)                                        
        width = max(1000, txt_surface.get_width()+10)                                       
        input_box.w = width
        gameDisplay.blit(txt_surface, (input_box.x+10, input_box.y+5))                      
        pygame.draw.rect(gameDisplay, color, input_box, 3)
        menu_text9 = font_titleLarge.render("ENTER USERNAME",True,white)
        gameDisplay.blit(menu_text9, (50,30))
        menu_text10 = font_title.render("ENTER YOUR USERNAME",True,white)
        gameDisplay.blit(menu_text10, (640,630))
        if try_again == True:
            menu_text11 = font.render("USERNAME NOT FOUND, TRY AGAIN",True,white)
            gameDisplay.blit(menu_text11, (300,300))
        text = text
        pygame.display.update()                                                                 
        clock.tick(fps)

def pauseM(gameDisplay,fps):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 840 <= mouse[0] <= 1060 and 390 <= mouse[1] <= 470:
                    return "play"
                if 840 <= mouse[0] <= 1060 and 590 <= mouse[1] <= 670:
                    return "option"
                if 840 <= mouse[0] <= 1060 and 790 <= mouse[1] <= 870:
                    pygame.quit()
                    quit()

        gameDisplay.blit(backG, (0,0))  
        menu_text1 = font_titleLarge.render("PAUSE", True, white)
        gameDisplay.blit(menu_text1, (50,50))
        pygame.draw.rect(gameDisplay, darkGrey, [850, 400, 220 , 60])
        pygame.draw.rect(gameDisplay, darkGrey, [850, 600, 220 , 60])
        pygame.draw.rect(gameDisplay, darkGrey, [850, 800, 220 , 60])
        menu_text2 = font_sub.render("CONTINUE", True, white)
        gameDisplay.blit(menu_text2, (865,415))
        menu_text3 = font_sub.render("OPTIONS", True, white)
        gameDisplay.blit(menu_text3, (875,615))
        menu_text4 = font_sub.render("QUIT", True, white)
        gameDisplay.blit(menu_text4, (910,815))
        pygame.display.update()                                                                     
        clock.tick(fps)

def optionsM(gameDisplay,fps):
    print("options M")






    
     
