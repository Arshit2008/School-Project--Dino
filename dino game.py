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
    
##############    MAIN _ GAME    ##############

pygame.init()
width = 800 
height = 400
 
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("game")
clock = pygame.time.Clock()
run = True

dino_h = 50
dino_w = 30
dino_x = 100
dino_y = 300

cac_x = 800
cac_y = 300
cac_w = 25
cac_h = 50


ground_y = 350

cac_speed = 8
velo = 0
gravity = 2
jump = -20

while run :
    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("SPACE PRESSED")
                    print(event.key)
                    if dino_y >= ground_y - dino_h:
                        velo = jump
        
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                try:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                except:
                    run = False

                
    velo = velo + gravity
    dino_y = dino_y + velo
    cac_x = cac_x - cac_speed
    print(velo,dino_y)
    
    if dino_y >= ground_y - dino_h:
        dino_y = ground_y - dino_h
        velo = 0
        
            
    screen.fill((255,255,255))
    pygame.draw.line(screen, (0,0,0), (0,ground_y), (width,ground_y), 2)
    pygame.draw.rect(screen, (0,0,0), (dino_x, dino_y, dino_w, dino_h))
    pygame.draw.rect(screen, (0,150,0),(cac_x,cac_y,cac_w,cac_h))
    
    pygame.display.update()
    clock.tick(25)
pygame.quit()

##########    DINO    ###########
