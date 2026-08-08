import mysql.connector
import pygame
import tkinter as tk


DB_host = "localhost"
DB_user = "root"
DB_password = "computer"
DB = input("Database Name: ")

def connect():
    m = mysql.connector.connect (host = DB_host, user = DB_user, password = DB_password, database = DB)
    return m

def reset(DB):
    mycon= connect()
    c = mycon.cursor()
    c.execute(f"drop database {DB}")
    print("Database deleted ! ")

def Db():
    mycon = mysql.connector.connect (host = DB_host, user = DB_user, password = DB_password)
    c=mycon.cursor()
    
    c.execute("create database if not exists GAME")
    c.execute (f"use {DB}")
    
    c.execute("""create table if not exists player(
        players_id int primary key auto_increment,
        username varchar(20) unique not null
    )""")
    
    c.execute("""create table if not exists highscores(
        score_id int primary key auto_increment,
        player_id int,
        score int not null,
        obstaces int not null,
        foreign key(player_id) references player(players_id) on delete cascade
        )""")
    
    mycon.commit()  
    mycon.close()
    print("All databases made")
    
def register_player(username):
    mycon = connect()
    c = mycon.cursor()
    a = username,
    
    c.execute (" insert into player(username) values(%s)",a )
    player_id = c.lastrowid
    
    
    mycon.commit()
    mycon.close()
    return player_id

def save_scores (player_id,score,obs):
    mycon = connect()
    c = mycon.cursor()
    
    c.execute ("INSERT INTO highscores(score_id,player_id,score,obstacles) values(%s,%s,%s,%s)",(1,player_id,score,obs))
    
    mycon.commit()
    mycon.close()
    
##############    MAIN _ GAME    ##############
def game(player_id):
    pygame.init()
    width = 800 
    height = 400
    
    screen = pygame.display.set_mode((width,height)) #window dimensions
    pygame.display.set_caption("game")
    clock = pygame.time.Clock()  #gamespeed
    run = True

    score = 0.001
    obstacle = 0

    dino_h = 50
    dino_w = 30           #dino dimensions and position
    dino_x = 100
    dino_y = 300

    cac_x = 800
    cac_y = 300
    cac_w = 25          #cactus dimensions and position
    cac_h = 50

    cactus_passed = False

    dino_rect = pygame.Rect(dino_x,dino_y,dino_w,dino_h)
    cactus_rect = pygame.Rect(cac_x,cac_y,cac_w,cac_h)


    ground_y = 350      #Ground level

    cac_speed = 8
    velo = 0            #velocity of all
    gravity = 1
    jump = -14

    font = pygame.font.Font(None, 36)

    while run :
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # print(event.key)
                        if dino_y >= ground_y - dino_h:
                            velo = jump
            
                if event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_ESCAPE:
                            run = False

                    
        velo = velo + gravity
        dino_y = dino_y + velo           #main-calculation for jump and gravity
        cac_x = cac_x - cac_speed
        
        
        #print ("dino jump position:",dino_y)

        score = score + 0.1
        if (cac_x + cac_w) < dino_x and cactus_passed == False:
            obstacle = obstacle + 1
            cactus_passed = True
        
        dino_rect.x= dino_x
        dino_rect.y= dino_y
        cactus_rect.x= cac_x
        cactus_rect.y= cac_y
        
        if dino_y >= ground_y - dino_h:
            dino_y = ground_y - dino_h
            velo = 0

        if cac_x < 0:
            cac_x = 800
            cactus_passed = False
        
        
                
        screen.fill((255,255,255))
        
        score_text = font.render ("score:" + str(int(score)), True, (0,0,0))
        screen.blit(score_text, (5,5))
        
        obstacles_text = font.render ("obstacles cleared:" + str(obstacle), True, (0,0,0))
        screen.blit(obstacles_text, (5,30))
        
        pygame.draw.line(screen, (0,0,0), (0,ground_y), (width,ground_y), 3)  #draw the ground
        pygame.draw.rect(screen, (0,0,0), (dino_x,dino_y,dino_w,dino_h))  #draw the dino
        pygame.draw.rect(screen, (0,150,0), (cac_x,cac_y,cac_w,cac_h))  #draw the cactus
        
        pygame.display.update()  #update the screen with the new drawings
        
        if dino_rect.colliderect(cactus_rect):
            print("Game Over")
            
            save_scores(player_id,int(score),obstacle)
            
            run = False
        
        clock.tick(30)             #refresh rate of the game
    pygame.quit()
    
    
    
##############   DB-ON-LOADING  ############## 
reset(DB)
Db()


##############   TKINTER-MENU   ##############
root = tk.Tk()
root.title("Dino Game")
root.geometry("400x250")

username_label = tk.Label(root , text = "Enter Username: ")    
username_label.pack()

username_entry = tk.Entry(root)
username_entry.pack()

def start_game():
    username = username_entry.get()
    print("Username:", username)
    player_id = register_player(username)
    print("player id : ",player_id)
    root.destroy()
    game(player_id)

start_button = tk.Button(root, text = "Start Game", command = start_game)
start_button.pack()

tk.Button(root, text = "Stat", command = root.quit).pack()

root.mainloop()


mycon = connect()
c = mycon.cursor()
c.execute("select * from player")
print(c.fetchall())