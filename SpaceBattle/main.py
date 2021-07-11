import pygame
import os
pygame.font.init()

SCREEN_WH = 900, 500 
WIN = pygame.display.set_mode(SCREEN_WH)
pygame.display.set_caption("Demo Game!")
FPS = 60
SHIP_VE = 5
BULLET_VE = 12
SPACESHIP_WH = 150, 100
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BORDER = pygame.Rect(SCREEN_WH[0]/2 - 5 , 0, 10, SCREEN_WH[1])
HEALTH_FONT = pygame.font.SysFont('impact', 40)
WINNER_FONT = pygame.font.SysFont('impact', 100)

#Federation Globals
FEDERATION_VE = 10
FEDERATION_HEALTH = 10
FEDERATION_BULLET = 4
FEDERATION_BULLET_VE = 12
FEDERATION_HIT = pygame.USEREVENT + 1

#Empire Globals
EMPIRE_VE = 6
EMPIRE_HEALTH = 10
EMPIRE_BULLET = 6
EMPIRE_BULLET_VE = 8
EMPIRE_HIT = pygame.USEREVENT + 2

#Assets
#Federation
ASSET_SHIP_FEDERATION = pygame.image.load(
    os.path.join('assets','federation.PNG'))
SPRITE_SHIP_FEDERATION = pygame.transform.scale(ASSET_SHIP_FEDERATION, SPACESHIP_WH)  
#Empire
ASSET_SHIP_EMPIRE = pygame.image.load(
    os.path.join('assets','empire.PNG'))
SPRITE_SHIP_EMPIRE = pygame.transform.rotate(pygame.transform.scale(ASSET_SHIP_EMPIRE, SPACESHIP_WH),180)      

#Background
ASSET_BACKGROUND = pygame.transform.scale(
    pygame.image.load(
        os.path.join('assets','background.PNG')
    ), SCREEN_WH)    

def draw_window(federation, empire, federation_bullet, empire_bullet, FEDERATION_HEALTH, EMPIRE_HEALTH):
    #Draw background
    WIN.blit(ASSET_BACKGROUND, (0,0))
    #Draw Boarder
    pygame.draw.rect(WIN, BLACK, BORDER)
    #Scores
    federation_health_text = HEALTH_FONT.render("Health: " + str(FEDERATION_HEALTH), 1, WHITE)
    empire_health_text = HEALTH_FONT.render("Health: " + str(EMPIRE_HEALTH), 1, WHITE)   
    WIN.blit(federation_health_text, (10, 10))
    WIN.blit(empire_health_text, (SCREEN_WH[0] - empire_health_text.get_width() - 10, 10))    
    #Draw Ships
    WIN.blit(SPRITE_SHIP_FEDERATION, (federation.x, federation.y))
    WIN.blit(SPRITE_SHIP_EMPIRE, (empire.x, empire.y))  

    for bullet in federation_bullet:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in empire_bullet:
        pygame.draw.rect(WIN, RED, bullet)        

    pygame.display.update()    

def movement_keys(name, faction, keys):
    keys_pressed = pygame.key.get_pressed()
    if name == 'federation':
        VE = FEDERATION_VE
    if name == 'empire':
        VE = EMPIRE_VE

    if keys == 'arrow':
        keys = pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
        borders = (faction.y - VE > 0, 
                   faction.y + VE + faction.height < SCREEN_WH[1],
                   faction.x - VE > BORDER.x + BORDER.width,                 
                   faction.x + VE + faction.width < SCREEN_WH[0])
    if keys == 'wasd':
        keys = pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d   
        borders = (faction.y - VE > 0, 
                   faction.y + VE + faction.height < SCREEN_WH[1],
                   faction.x - VE > 0, 
                   faction.x + VE + faction.width < BORDER.x)             
    #up,down,left,right   
    if keys_pressed[keys[0]] and borders[0]:
        faction.y -= VE
    if keys_pressed[keys[1]] and borders[1]:
        faction.y += VE
    if keys_pressed[keys[2]] and borders[2]:
        faction.x -= VE
    if keys_pressed[keys[3]] and borders[3]:
        faction.x += VE            

def handle_bullets(bullets, src, target, event):
    for bullet in bullets:
        #Fire bullet in direcion
        if src == 'federation':
            bullet.x += FEDERATION_BULLET_VE
            if bullet.x > SCREEN_WH[0]:
                bullets.remove(bullet)
        if src == 'empire':    
            bullet.x -= EMPIRE_BULLET_VE
            if bullet.x < 0:
                bullets.remove(bullet)
        #Hit target ship
        if target.colliderect(bullet):
            pygame.event.post(pygame.event.Event(event))
            bullets.remove(bullet)

def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(winner_text, (SCREEN_WH[0]/2 - winner_text.get_width()/2, SCREEN_WH[1]/2 - winner_text.get_height()/2 ))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    #init federation
    federation = pygame.Rect(SCREEN_WH[0]/4, SCREEN_WH[1]/2, SPACESHIP_WH[0], SPACESHIP_WH[1])    
    federation_bullet = []
    federation_controls = 'wasd'
    federation_health = FEDERATION_HEALTH
    #init empire
    empire = pygame.Rect(3*SCREEN_WH[0]/4, SCREEN_WH[1]/2, SPACESHIP_WH[0], SPACESHIP_WH[1]) 
    empire_bullet = []
    empire_controls = 'arrow'
    empire_health = EMPIRE_HEALTH
    #init other
    winner_text = ""

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        #Create bullets
            if event.type == pygame.KEYDOWN:
                print('here')
                if event.key == pygame.K_SPACE and len(federation_bullet) < 4: #federation shoot
                    bullet = pygame.Rect(federation.x + federation.width, federation.y + federation.height/2 - 3, 10, 6)
                    federation_bullet.append(bullet)

                if event.key == pygame.K_SLASH and len(empire_bullet) < 4:   #empire shoot
                  bullet1 = pygame.Rect(empire.x, empire.y + empire.height/4 - 3, 10, 6)
                  bullet2 = pygame.Rect(empire.x, empire.y + 3*empire.height/4 - 3, 10, 6)
                  empire_bullet.append(bullet1)
                  empire_bullet.append(bullet2)
            
            #Process on hit events
            if event.type == FEDERATION_HIT:
                federation_health -= 1
            if event.type == EMPIRE_HIT:
                empire_health -= 1    

        #WIN Scinerios
        if federation_health <= 0:
            winner_text = "Empire Wins!"
        if empire_health <= 0:
            winner_text = "Federation Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break


        #Empire events
        handle_bullets(empire_bullet, 'empire', federation, FEDERATION_HIT)
        movement_keys('empire', empire, empire_controls)

        #Federation events
        handle_bullets(federation_bullet, 'federation', empire, EMPIRE_HIT)
        movement_keys('federation', federation, federation_controls)

        #Draw
        draw_window(federation, empire, federation_bullet, empire_bullet, federation_health, empire_health)
    
    #restart if quit not called 
    main()

if __name__ == "__main__":
    main()


