import mysql.connector

DB_host = "localhost"
DB_user = "root"
DB_password = "computer"
DB = "GAME"

def Db():
    mycon = mysql.connector.connect (host = DB_host, user = DB_user, password = DB_password, database = DB)
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
    print("database made")
    
Db()