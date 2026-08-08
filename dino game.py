import mysql.connector
import pygame



DB_host = "localhost"
DB_user = "root"
DB_password = "computer"

def connect():
    mycon = mysql.connector.connect (host = DB_host, user = DB_user, password = DB_password)
    return mycon


def Db():
    mycon = connect()
    c=mycon.cursor()
    
    c.execute("create database if not exists GAME")
    c.execute ("use GAME")
    
    c.execute("""create table if not exists player(
        players_id int primary key,
        username varchar(20) unique not null
    )""")
    
    c.execute("""create table if not exists highscores(
        score_id int primary key,
        player_id int,
        score int not null,
        obstaces_cleared int not null,
        foreign key(player_id) references player(players_id) on delete cascade
        )""")
    
    mycon.commit()  
    mycon.close()
    print("All databases made")
    
    

##############   DB-ON-LOADING  ############## 

Db()

##############    MAIN _ GAME    ##############

pygame.init()
width = 800 
height = 400
 
screen = pygame.display.set_mode((width,height)) #window dimensions
pygame.display.set_caption("game")
clock = pygame.time.Clock()  #gamespeed
run = True

score = 0.001
obstacles_cleared = 0

dino_h = 50
dino_w = 30           #dino dimensions and position
dino_x = 100
dino_y = 300

cac_x = 800
cac_y = 300
cac_w = 25          #cactus dimensions and position
cac_h = 50

dino_rect = pygame.Rect(dino_x,dino_y,dino_w,dino_h)
cactus_rect = pygame.Rect(cac_x,cac_y,cac_w,cac_h)


ground_y = 350      #Ground level

cac_speed = 8
velo = 0            #velocity of all
gravity = .5
jump = -10

font = pygame.font.Font(None, 36)

while run :
    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # print(event.key)
                    if dino_y >= ground_y - dino_h:
                        velo = jump
        
            elif event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                try:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                except:
                    run = False

                
    velo = velo + gravity
    dino_y = dino_y + velo           #main-calculation for jump and gravity
    cac_x = cac_x - cac_speed
    #print ("dino jump position:",dino_y)

    score = score + 0.1
    if cac_x < dino_x and cac_x > dino_x - cac_speed:
        obstacles_cleared += 1
       
    dino_rect.x= dino_x
    dino_rect.y= dino_y
    cactus_rect.x= cac_x
    cactus_rect.y= cac_y
    
    if dino_y >= ground_y - dino_h:
        dino_y = ground_y - dino_h
        velo = 0
        
            
    screen.fill((255,255,255))
    
    score_text = font.render ("score:" + str(int(score)), False, (0,0,0))
    screen.blit(score_text, (20,20))
    
    pygame.draw.line(screen, (0,0,0), (0,ground_y), (width,ground_y), 3)  #draw the ground
    pygame.draw.rect(screen, (0,0,0), (dino_x,dino_y,dino_w,dino_h))  #draw the dino
    pygame.draw.rect(screen, (0,150,0), (cac_x,cac_y,cac_w,cac_h))  #draw the cactus
    
    pygame.display.update()  #update the screen with the new drawings
    
    if dino_rect.colliderect(cactus_rect):
        print("Game Over")
        run = False
    
    clock.tick(60)             #refresh rate of the game
pygame.quit()

