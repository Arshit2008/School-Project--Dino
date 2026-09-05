import random
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import pygame

DB_host = "localhost"
DB_user = "root"
DB_password = "computer"
DB_ = input("Database Name: ").strip()


def connect():
    """Connect to the selected MySQL database and return the connection."""
    try:
        m = mysql.connector.connect(
            host=DB_host, user=DB_user, password=DB_password, database=DB_
        )
        return m
    except Exception as err:
        print("DATABASE CONNECTION ERROR:", err)
        return None


def reset(db_name):
    """Delete the selected database and close the MySQL connection."""
    mycon = None
    try:
        mycon = mysql.connector.connect(
            host=DB_host, user=DB_user, password=DB_password
        )
        c = mycon.cursor()
        c.execute(f"DROP DATABASE IF EXISTS `{db_name}`")
        print("Database deleted!")
    except Exception as err:
        print(f"Database delete error: {err}")
    finally:
        if mycon:
            mycon.close()


def Db():
    """Create the database and initialize the player, score, and history tables."""
    mycon = None
    try:
        mycon = mysql.connector.connect(
            host=DB_host, user=DB_user, password=DB_password
        )
        c = mycon.cursor()
        c.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_}`")
        c.execute(f"USE `{DB_}`")

        c.execute("""
            CREATE TABLE IF NOT EXISTS player(
                players_id INT PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(20) UNIQUE NOT NULL
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS highscores(
                score_id INT PRIMARY KEY AUTO_INCREMENT,
                player_id INT UNIQUE,
                score INT NOT NULL,
                obstacles INT NOT NULL,
                FOREIGN KEY(player_id)
                REFERENCES player(players_id)
                ON DELETE CASCADE
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS game_history(
                history_id INT PRIMARY KEY AUTO_INCREMENT,
                player_id INT,
                score INT NOT NULL,
                obstacles INT NOT NULL,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(player_id)
                REFERENCES player(players_id)
                ON DELETE CASCADE
            )
        """)
        mycon.commit()
        print("All tables initialized successfully.")
    except Exception as err:
        print("Error creating tables:", err)
    finally:
        if mycon:
            mycon.close()


def register_player(username):
    """Find or create a player by username and return the player's ID."""
    mycon = None
    try:
        mycon = connect()
        if mycon is None:
            return None
        c = mycon.cursor()
        c.execute("SELECT players_id FROM player WHERE username = %s", (username,))
        check = c.fetchone()

        if check:
            player_id = check[0]
            print("Player exists")
        else:
            c.execute("INSERT INTO player(username) VALUES(%s)", (username,))
            player_id = c.lastrowid
            print("New Player created")
            mycon.commit()

        return player_id
    except Exception as err:
        print("Registration error:", err)
        return None
    finally:
        if mycon:
            mycon.close()


def save_history(player_id, score, obs):
    """Store one completed game in the player's game history."""
    mycon = None
    try:
        mycon = connect()
        if mycon is None:
            return
        c = mycon.cursor()
        c.execute("""
            INSERT INTO game_history(player_id, score, obstacles)
            VALUES(%s, %s, %s)
        """, (player_id, score, obs))
        mycon.commit()
    except Exception as err:
        print("History save error:", err)
    finally:
        if mycon:
            mycon.close()


def save_scores(player_id, score, obs):
    """Save a player's score when it is their first or highest score."""
    mycon = None
    try:
        mycon = connect()
        if mycon is None:
            return
        c = mycon.cursor()
        c.execute("SELECT score FROM highscores WHERE player_id = %s", (player_id,))
        result = c.fetchone()

        if result:
            score_old = result[0]
            if score > score_old:
                c.execute("""
                    UPDATE highscores
                    SET score = %s, obstacles = %s
                    WHERE player_id = %s
                """, (score, obs, player_id))
                print("New Highscore updated!")
        else:
            c.execute("""
                INSERT INTO highscores(player_id, score, obstacles)
                VALUES(%s, %s, %s)
            """, (player_id, score, obs))
        mycon.commit()
    except Exception as err:
        print("Score save error:", err)
    finally:
        if mycon:
            mycon.close()


def show_stats():
    """Display the saved high scores in a Tkinter window."""
    mycon = connect()
    if mycon is None:
        return
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
    tk.Label(stats, text="HIGH-SCORES", font=("Arial", 20, "bold")).pack(pady=15)

    heading = tk.Label(
        stats,
        text="Rank      Player          Score       Obstacles",
        font=("Arial", 12, "bold"),
    )
    heading.pack(pady=5)
    tk.Label(stats, text="-" * 55, font=("Arial", 10)).pack()

    if not results:
        tk.Label(stats, text="No scores recorded yet.", font=("Arial", 12)).pack(pady=15)
    else:
        for i, row in enumerate(results, start=1):
            username, score, obstacles = row[0], row[1], row[2]
            text = f"{i:<10}{username:<15}{score:<12}{obstacles}"
            tk.Label(stats, text=text, font=("Courier New", 11)).pack(
                anchor="w", padx=30, pady=2
            )


def show_history():
    """Display the 20 most recent games in a Tkinter window."""
    mycon = connect()
    if mycon is None:
        return
    c = mycon.cursor()
    c.execute("""
        SELECT p.username, g.score, g.obstacles, g.played_at
        FROM game_history g
        JOIN player p ON p.players_id = g.player_id
        ORDER BY g.history_id DESC
        LIMIT 20
    """)
    history = c.fetchall()
    mycon.close()

    history_window = tk.Toplevel(root)
    history_window.title("Game History")
    history_window.geometry("520x350")
    tk.Label(history_window, text="Recent Games", font=("Arial", 18, "bold")).pack(pady=10)

    if not history:
        tk.Label(history_window, text="No Games Played Yet.", font=("Arial", 12)).pack(pady=15)
        return

    for i, row in enumerate(history, start=1):
        username, final_score, obstacles, played_at = row
        time_str = played_at.strftime("%Y-%m-%d %H:%M:%S") if played_at else ""
        text = f"{i:<3} {username:<10} Score: {final_score:<6} Obs: {obstacles:<4} [{time_str}]"
        tk.Label(history_window, text=text, font=("Courier New", 10)).pack(
            anchor="w", padx=20, pady=2
        )


def retry_game(window, player_id):
    """Close the game-over window and start another game for the player."""
    window.destroy()
    final_score, obstacles = game(player_id)
    game_over_window(player_id, final_score, obstacles)


def exit_game(window):
    """Close the current window and exit the application."""
    window.destroy()
    root.destroy()


def back_to_menu(window):
    """Close the current window and show the main menu again."""
    window.destroy()
    root.deiconify()


def game_over_window(player_id, final_score, obstacles):
    """Create the game-over window with score details and action buttons."""
    window = tk.Toplevel(root)
    window.title("Game Over")
    window.geometry("350x250")

    tk.Label(window, text="Game Over", font=("Arial", 20, "bold")).pack(pady=15)
    tk.Label(window, text=f"Final score: {final_score}", font=("Arial", 13)).pack()
    tk.Label(window, text=f"Obstacles cleared: {obstacles}", font=("Arial", 13)).pack(pady=5)
    tk.Button(window, text="Retry", command=lambda: retry_game(window, player_id), width=12).pack(pady=5)
    tk.Button(window, text="Main Menu", command=lambda: back_to_menu(window), width=12).pack(pady=5)
    tk.Button(window, text="Exit", command=lambda: exit_game(window), width=12).pack(pady=5)


def game(player_id):
    """Run the Dino game and return the final score and cleared obstacles."""
    pygame.init()
    width, height = 800, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dino Game")
    clock = pygame.time.Clock()
    run = True

    obstacle = 0
    dino_h, dino_w = 50, 30
    dino_x, dino_y = 100, 300
    dino_rect = pygame.Rect(dino_x, dino_y, dino_w, dino_h)

    cac_speed = 6
    max_speed = 30
    speed_increase_every = 5
    speed_increase_amount = 2

    ground_y = 350
    cactus_list = []

    spawn_timer = 0
    next_spawn_time = random.randint(60, 110)

    velo = 0
    gravity = 1
    jump = -15
    font = pygame.font.Font(None, 36)
    final_score = 0

    def get_next_spawn_interval(current_speed):
        min_frame = max(28, int(450 / current_speed))
        max_frame = max(45, int(750 / current_speed))
        return random.randint(min_frame, max_frame)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and dino_y >= ground_y - dino_h:
                    velo = jump
                if event.key == pygame.K_ESCAPE:
                    run = False

        velo += gravity
        dino_y += velo
        if dino_y >= ground_y - dino_h:
            dino_y = ground_y - dino_h
            velo = 0

        score = obstacle * 5
        dino_rect.y = dino_y

        screen.fill((255, 255, 255))
        score_text = font.render(f"Score: {int(score)}", True, (0, 0, 0))
        screen.blit(score_text, (5, 5))
        speed_text = font.render(f"Speed: {cac_speed}", True, (0, 0, 0))
        screen.blit(speed_text, (5, 40))

        pygame.draw.line(screen, (0, 0, 0), (0, ground_y), (width, ground_y), 3)
        pygame.draw.rect(screen, (0, 0, 0), (dino_x, dino_y, dino_w, dino_h))

        for c in cactus_list:
            pygame.draw.rect(screen, (0, 150, 0), c[0])
        pygame.display.update()

        spawn_timer += 1
        if spawn_timer >= next_spawn_time:
            c_type = random.randint(1, 3)
            if c_type == 1:
                cac_width, cac_height = 15, 25
            elif c_type == 2:
                cac_width, cac_height = 25, 60
            else:
                cac_width, cac_height = 45, 40

            new_cactus = pygame.Rect(width, ground_y - cac_height, cac_width, cac_height)
            cactus_list.append([new_cactus, False])
            spawn_timer = 0
            next_spawn_time = get_next_spawn_interval(cac_speed)

        # Move and check collisions
        for c in cactus_list:
            c_rect = c[0]
            c_rect.x -= cac_speed

            if c_rect.right < dino_x and not c[1]:
                obstacle += 1
                c[1] = True
                if obstacle % speed_increase_every == 0 and cac_speed < max_speed:
                    cac_speed += speed_increase_amount

            if dino_rect.colliderect(c_rect):
                final_score = obstacle * 5
                save_history(player_id, final_score, obstacle)
                save_scores(player_id, final_score, obstacle)
                run = False
                break

        # Safely prune offscreen cacti
        cactus_list = [c for c in cactus_list if c[0].right >= 0]

        clock.tick(60)

    pygame.quit()
    return final_score, obstacle


Db()
root = tk.Tk()
root.title("Dino Game")
root.geometry("400x250")

username_label = tk.Label(root, text="Enter Username:", font=("Arial", 11))
username_label.pack(pady=8)
username_entry = tk.Entry(root, font=("Arial", 11))
username_entry.pack(pady=5)


def start_game():
    username = username_entry.get().strip()

    if not username:
        messagebox.showwarning("Warning", "Please enter a username.")
        return

    player_id = register_player(username)
    if player_id is None:
        messagebox.showerror("Error", "Could not connect to database.")
        return

    root.withdraw()
    final_score, obstacle = game(player_id)
    game_over_window(player_id, final_score, obstacle)


tk.Button(root, text="Start Game", command=start_game, width=15).pack(pady=5)
tk.Button(root, text="Game History", command=show_history, width=15).pack(pady=5)
tk.Button(root, text="Stats", command=show_stats, width=15).pack(pady=5)

root.mainloop()

mycon = connect()
if mycon:
    c = mycon.cursor()
    c.execute("SELECT * FROM player")
    print("Registered players:", c.fetchall())
    mycon.close()