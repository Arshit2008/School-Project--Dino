import mysql.connector
import pygame
import tkinter as tk
import pickle

DB_host = "localhost"
DB_user = "root"
DB_password = "computer"
DB_ = input("Database Name: ")

def connect():
    try:
        m = mysql.connector.connect (host = DB_host, user = DB_user, password = DB_password, database = DB_)
    except Exception as err:
        print("DATABASE CONNNECTION ERROR :",err)
    return m

def reset(DB_):
    try:    
        mycon = connect()
        c = mycon.cursor()
        a = DB_
    
        c.execute(f"DROP DATABASE IF EXISTS {a}")
        print("Database deleted !")
    except Exception as err:
        print(f"Database delete error: {err}")
    finally:
        mycon.close()

def Db():
    try:
        mycon = mysql.connector.connect (host = DB_host, user = DB_user, password = DB_password)
        c=mycon.cursor()
        
        c.execute("create database if not exists GAME")
        c.execute (f"use {DB_}")
        
        c.execute("""create table if not exists player(
            players_id int primary key auto_increment,
            username varchar(20) unique not null
        )""")
        
        c.execute("""create table if not exists highscores(
            score_id int primary key auto_increment,
            player_id int,
            score int not null,
            obstacles int not null,
            foreign key(player_id) references player(players_id) on delete cascade
            )""")
        
        mycon.commit()  
        mycon.close()
        print("All databases made")
    except Exception as err:
        print("Error is : ",err)
        
def register_player(username):
    try:
        mycon = connect()
        c = mycon.cursor()
        
        c.execute("select players_id from player where username = %s",(username,))
        check = c.fetchone()
        
        if check:
            player_id = check[0]
            print("player exists")
        else:
        
            c.execute (" insert into player(username) values(%s)", (username,) )
            player_id = c.lastrowid
        
            print("New Player")
            mycon.commit()
        mycon.close()
        return player_id
    
    except Exception as err:
            print("Error is : ",err)

def save_scores (player_id,score,obs):
    try:
        mycon = connect()
        c = mycon.cursor()
        
        c.execute(f"select score from highscores where player_id = {player_id}")
        result = c.fetchone()
        
        if result:
            score_old = result[0]
            if score_old>score:
                print(f"Old Score Higher :{score_old}")
                
            else:
                c.execute(f"""
                        UPDATE highscores
                        set score = {score} ,obstacles = {obs}
                        where player_id = {player_id}
                        """)
                print("New Highscore !")
        else:
            c.execute ("INSERT INTO highscores(player_id,score,obstacles) values(%s,%s,%s)",(player_id,score,obs))    
            
        mycon.commit()
        mycon.close()
        
    except Exception as err:
        print("Error is : ",err)
        
        
def show_stats():
    mycon = connect()
    c = mycon.cursor()

    c.execute("""
        SELECT username, score, obstacles
        FROM highscores h
        JOIN player p ON p.players_id = h.player_id
        ORDER BY score DESC
    """)

    results = c.fetchall()
    mycon.close()

    stats = tk.Toplevel(root)
    stats.title("High-Scores")
    stats.geometry("500x350")

    tk.Label(
        stats,
        text="HIGH-SCORES",
        font=("Arial", 20, "bold")
    ).pack(pady=15)
    
    heading = tk.Label(
        stats,
        text="Rank       Player          Score       Obstacles",
        font=("Arial", 12, "bold")
    )
    heading.pack(pady=5)

    tk.Label(
        stats,
        text="-" * 55,
        font=("Arial", 10)
    ).pack()

    if not results:
        tk.Label(
            stats,
            text="No scores recorded yet.",
            font=("Arial", 12)
        ).pack(pady=15)

    else:
        for i, row in enumerate(results, start=1):
            username = row[0]
            score = row[1]
            obstacles = row[2]

            text = (
                f"{i:<10}"
                f"{username:<15}"
                f"{score:<12}"
                f"{obstacles}"
            )

            tk.Label(
                stats,
                text=text,
                font=("Courier New", 11)
            ).pack(anchor="w", padx=30, pady=2)


def retry_game(window,player_id):
    window.destroy()
    final_score,obstacles = game(player_id)
    game_over_window(player_id,final_score,obstacles)
    


def exit_game(window):
    window.destroy()
    root.destroy()
    

def game_over_window(player_id,final_score,obstacles):
    window = tk.Toplevel()
    window.title("Game Over")
    window.geometry("350x250")
    
    tk.Label(
        window,
        text = "Game over",
        font = ("arial",20)
    ).pack(pady = 15)
    
    tk.Label(
        window,
        text = f"Final score: {final_score}",
        font = ("arial",14)
    ).pack()
    
    tk.Label(
        window,
        text = f"Obstacles cleared: {obstacles}",
        font = ("arial",14)
    ).pack(pady = 5)
    
    tk.Button(
        window,
        text = "Retry",
        command =lambda: retry_game (window,player_id)
    ).pack(pady = 10)
       
    tk.Button(
        window,
        text = "Main Menu",
        command = lambda : back_to_menu(window)
    ).pack(pady=5)
       
    tk.Button(
        window,
        text = "Exit",
        command =lambda: exit_game(window)
    ).pack()

def show_history():
    game_history_file = "game_history.pkl"
    try:
        with open(game_history_file,"rb") as file:
            history = pickle.load (file)
            
    except Exception as err:
        print("History Error:",err)
        history = []
    
    history_window = tk.Toplevel(root)
    history_window.title("Game History")
    history_window.geometry("450x300")
    
    tk.Label(
        history_window,
        text = "Game History",
        font = ("arial",20,"bold")
    ).pack(pady = 15)
    
    if not history:
        tk.Label(
            history_window,
            text = "No Games Played Yet.",
            font = ("arial",20)
        )
        
    temp_stack = []
    
    while game_history:
        game = game_history.pop()
        temp_stack.append(game)
        
    for i,game in enumerate(reversed(history),start = 1):
        final_score = game[0]
        obstacles = game[1]
        
        text = f"Game {i} :score = {final_score}   obstacles = {obstacles}"
        
        tk.Label(
            history_window,
            text = text,
            font = ("arial",12)            
            ).pack(pady=3)
        
    while temp_stack:
        game_history.append (temp_stack.pop())
        
        
def back_to_menu(window):
    
    window.destroy()
    root.deiconify()
    
game_history_file = "game_history.pkl"

try:
    with open(game_history_file,"rb")as f:
        game_history = pickle.load(f)
except:
    game_history = []    

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
            
            final_score = int(score)
            game_history.append((final_score,obstacle))
            print("Game History : ",game_history)
            
            with open(game_history_file,"wb") as file:
                pickle.dump(game_history, file)
            
            save_scores(player_id,final_score,obstacle)
            run = False
        
        clock.tick(60)             #refresh rate of the game
    pygame.quit()
    return final_score, obstacle
    
##############   DB-ON-LOADING  ############## 

reset(DB_)
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
    
    root.withdraw()
    final_score ,obstacle = game(player_id)
    game_over_window(player_id,final_score ,obstacle)

tk.Button(root, text = "Start Game", command = start_game).pack(pady = 3)
tk.Button(root ,text = "Game History",command = show_history).pack(pady = 3)
tk.Button(root, text = "Stat", command = show_stats).pack()

root.mainloop()

mycon = connect()
c = mycon.cursor()
c.execute("select * from player")
print(c.fetchall())

    
