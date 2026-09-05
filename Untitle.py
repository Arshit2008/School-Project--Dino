from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        width, height = A4
        # Header
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.black)
        self.drawString(14 * mm, height - 12 * mm, "CLASS 12 CS PROJECT SUBMISSION — DINO GAME & MYSQL")
        self.setFont("Helvetica", 8)
        self.drawRightString(width - 14 * mm, height - 12 * mm, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(colors.HexColor("#222222"))
        self.setLineWidth(1)
        self.line(14 * mm, height - 13.5 * mm, width - 14 * mm, height - 13.5 * mm)

        # Footer
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.6)
        self.line(14 * mm, 12 * mm, width - 14 * mm, 12 * mm)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawString(14 * mm, 8 * mm, "Dino Game & MySQL Integration")
        self.drawRightString(width - 14 * mm, 8 * mm, f"Page {self._pageNumber} of {page_count}")

def build_pdf(filename="Class_12_CS_Project_Submission_Final.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=17 * mm,
        bottomMargin=16 * mm
    )

    # Styles
    code_style = ParagraphStyle(
        name="CodeStyle",
        fontName="Courier",
        fontSize=7.1,
        leading=8.8,
        textColor=colors.HexColor("#111111"),
        spaceAfter=0,
        spaceBefore=0
    )

    card_title_style = ParagraphStyle(
        name="CardTitle",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=10,
        textColor=colors.black
    )

    card_sub_style = ParagraphStyle(
        name="CardSub",
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=9,
        textColor=colors.HexColor("#555555"),
        spaceAfter=4
    )

    card_body_style = ParagraphStyle(
        name="CardBody",
        fontName="Helvetica",
        fontSize=7.3,
        leading=9.2,
        textColor=colors.HexColor("#222222"),
        spaceAfter=3
    )

    def make_banner(title, subtitle):
        title_p = Paragraph(f"<b>{title}</b>", ParagraphStyle(name="BTitle", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=colors.black))
        sub_p = Paragraph(subtitle, ParagraphStyle(name="BSub", fontName="Helvetica", fontSize=7.5, leading=9.5, textColor=colors.HexColor("#444444")))
        tbl = Table([[title_p], [sub_p]], colWidths=[182 * mm])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F8F8")),
            ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#222222")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        return tbl

    def format_code_block(code_lines):
        # Color keywords, strings, comments
        formatted = []
        kw_list = {"def", "return", "import", "from", "as", "try", "except", "finally", 
                   "if", "elif", "else", "while", "for", "in", "break", "True", "False", "None", "and", "or", "not"}
        
        for line in code_lines:
            line_esc = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;")
            
            # Comments
            if line.strip().startswith("#"):
                line_out = f'<font color="#DD0000"><i>{line_esc}</i></font>'
            else:
                line_out = line_esc
                # Color quotes
                line_out = line_out.replace('&quot;', '"')
                # Add highlighting around common tokens
                for kw in kw_list:
                    line_out = line_out.replace(f'&nbsp;{kw}&nbsp;', f'&nbsp;<font color="#E65C00"><b>{kw}</b></font>&nbsp;')
                    line_out = line_out.replace(f'({kw}&nbsp;', f'(<font color="#E65C00"><b>{kw}</b></font>&nbsp;')
                    line_out = line_out.replace(f'&nbsp;{kw}:', f'&nbsp;<font color="#E65C00"><b>{kw}</b></font>:')
                    if line_out.startswith(f'{kw}&nbsp;'):
                        line_out = f'<font color="#E65C00"><b>{kw}</b></font>&nbsp;' + line_out[len(kw)+6:]

            formatted.append(Paragraph(line_out, code_style))

        tbl = Table([[p] for p in formatted], colWidths=[182 * mm])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FAFAFA")),
            ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor("#DCDCDC")),
            ('TOPPADDING', (0,0), (-1,-1), 0.3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0.3),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        return tbl

    def make_card(title, subtitle, bullets):
        elements = [
            Paragraph(f"<b>{title}</b>", card_title_style),
            Paragraph(subtitle, card_sub_style),
            Spacer(1, 1*mm)
        ]
        for bold_t, body_t in bullets:
            elements.append(Paragraph(f"<b>• {bold_t}</b> {body_t}", card_body_style))
        
        tbl = Table([[elements]], colWidths=[88 * mm], rowHeights=[120 * mm])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#222222")),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        return tbl

    story = []

    # ================= PAGE 1 =================
    story.append(make_banner("MAIN SOURCE CODE (PART 1)", "Project: Dino Runner with MySQL Integration | Backend & Schema Initialization"))
    story.append(Spacer(1, 3*mm))
    code_p1 = [
        "import random",
        "import tkinter as tk",
        "from tkinter import messagebox",
        "import mysql.connector",
        "import pygame",
        "",
        "# DATABASE CONFIGURATION",
        'DB_host = "localhost"',
        'DB_user = "root"',
        'DB_password = "computer"',
        'DB = input("Database Name: ").strip()',
        "",
        "def connect():",
        '    """Connect to selected MySQL database and return connection object."""',
        "    try:",
        "        return mysql.connector.connect(host=DB_host, user=DB_user, password=DB_password, database=DB)",
        "    except Exception as err:",
        '        print("DATABASE CONNECTION ERROR:", err)',
        "        return None",
        "",
        "def reset(db_name):",
        '    """Delete selected database."""',
        "    mycon = None",
        "    try:",
        "        mycon = mysql.connector.connect(host=DB_host, user=DB_user, password=DB_password)",
        "        c = mycon.cursor()",
        '        c.execute(f"DROP DATABASE IF EXISTS {db_name}")',
        "    finally:",
        "        if mycon: mycon.close()",
        "",
        "def Db():",
        '    """Initialize database and player, highscores, and game_history tables."""',
        "    mycon = None",
        "    try:",
        "        mycon = mysql.connector.connect(host=DB_host, user=DB_user, password=DB_password)",
        "        c = mycon.cursor()",
        '        c.execute(f"CREATE DATABASE IF NOT EXISTS {DB}")',
        '        c.execute(f"USE {DB}")',
        '        c.execute("""CREATE TABLE IF NOT EXISTS player(',
        "            players_id INT PRIMARY KEY AUTO_INCREMENT,",
        "            username VARCHAR(20) UNIQUE NOT NULL",
        '        )""")',
        '        c.execute("""CREATE TABLE IF NOT EXISTS highscores(',
        "            score_id INT PRIMARY KEY AUTO_INCREMENT,",
        "            player_id INT UNIQUE,",
        "            score INT NOT NULL,",
        "            obstacles INT NOT NULL,",
        "            FOREIGN KEY(player_id) REFERENCES player(players_id) ON DELETE CASCADE",
        '        )""")',
        '        c.execute("""CREATE TABLE IF NOT EXISTS game_history(',
        "            history_id INT PRIMARY KEY AUTO_INCREMENT,",
        "            player_id INT,",
        "            score INT NOT NULL,",
        "            obstacles INT NOT NULL,",
        "            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,",
        "            FOREIGN KEY(player_id) REFERENCES player(players_id) ON DELETE CASCADE",
        '        )""")',
        "        mycon.commit()",
        "    finally:",
        "        if mycon: mycon.close()",
        "",
        "def register_player(username):",
        '    """Find or register a user handle and return primary key player_id."""',
        "    mycon = connect()",
        "    if not mycon: return None",
        "    try:",
        "        c = mycon.cursor()",
        '        c.execute("SELECT players_id FROM player WHERE username = %s", (username,))',
        "        check = c.fetchone()",
        "        if check: return check[0]",
        "        else:",
        '            c.execute("INSERT INTO player (username) VALUES (%s)", (username,))',
        "            mycon.commit()",
        "            return c.lastrowid",
        "    finally: mycon.close()"
    ]
    story.append(format_code_block(code_p1))
    story.append(PageBreak())

    # ================= PAGE 2 =================
    story.append(make_banner("MAIN SOURCE CODE (PART 2)", "Pygame 2D Engine Loop & Tkinter GUI Dashboard"))
    story.append(Spacer(1, 3*mm))
    code_p2 = [
        "def save_scores(player_id, score, obs):",
        '    """Update highscore if new run surpasses previous personal best."""',
        "    mycon = connect()",
        "    if mycon:",
        "        c = mycon.cursor()",
        '        c.execute("SELECT score FROM highscores WHERE player_id = %s", (player_id,))',
        "        res = c.fetchone()",
        "        if res and score > res[0]:",
        '            c.execute("UPDATE highscores SET score=%s, obstacles=%s WHERE player_id=%s", (score, obs, player_id))',
        "        elif not res:",
        '            c.execute("INSERT INTO highscores (player_id, score, obstacles) VALUES (%s, %s, %s)", (player_id, score, obs))',
        "        mycon.commit()",
        "        mycon.close()",
        "",
        "def game(player_id):",
        "    pygame.init()",
        "    width, height = 800, 400",
        "    screen = pygame.display.set_mode((width, height))",
        "    clock, run = pygame.time.Clock(), True",
        "    obs, dino_h, dino_w, dino_x, dino_y = 0, 50, 30, 100, 300",
        "    dino_rect = pygame.Rect(dino_x, dino_y, dino_w, dino_h)",
        "    cac_speed, ground_y, cactus_list = 6, 350, []",
        "    spawn_timer, next_spawn, velo, gravity, jump = 0, 80, 0, 1, -15",
        "    font = pygame.font.Font(None, 36)",
        "    while run:",
        "        for event in pygame.event.get():",
        "            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):",
        "                run = False",
        "            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and dino_y >= ground_y - dino_h:",
        "                velo = jump",
        "        velo += gravity",
        "        dino_y += velo",
        "        if dino_y >= ground_y - dino_h:",
        "            dino_y, velo = ground_y - dino_h, 0",
        "        dino_rect.y = dino_y",
        "        screen.fill((255, 255, 255))",
        '        screen.blit(font.render(f"Score: {obs * 5} Speed: {cac_speed}", True, (0, 0, 0)), (10, 10))',
        "        pygame.draw.line(screen, (0, 0, 0), (0, ground_y), (width, ground_y), 3)",
        "        pygame.draw.rect(screen, (0, 0, 0), dino_rect)",
        "        spawn_timer += 1",
        "        if spawn_timer >= next_spawn:",
        "            ch, cw = random.choice([(25, 15), (60, 25), (40, 45)])",
        "            cactus_list.append([pygame.Rect(width, ground_y - ch, cw, ch), False])",
        "            spawn_timer, next_spawn = 0, random.randint(max(28, int(450 / cac_speed)), max(45, int(750 / cac_speed)))",
        "        for c_box in cactus_list:",
        "            c_box[0].x -= cac_speed",
        "            pygame.draw.rect(screen, (0, 150, 0), c_box[0])",
        "            if c_box[0].right < dino_x and not c_box[1]:",
        "                obs += 1; c_box[1] = True",
        "                if obs % 5 == 0 and cac_speed < 30: cac_speed += 2",
        "            if dino_rect.colliderect(c_box[0]):",
        "                save_scores(player_id, obs * 5, obs); run = False; break",
        "        cactus_list = [c_box for c_box in cactus_list if c_box[0].right >= 0]",
        "        pygame.display.update(); clock.tick(60)",
        "    pygame.quit()",
        "    return obs * 5, obs",
        "",
        "#--- DRIVER & GUI DASHBOARD ---",
        "Db()",
        "root = tk.Tk()",
        'root.title("Dino Game Menu"); root.geometry("360x220")',
        'tk.Label(root, text="Enter Username:", font=("Arial", 11)).pack(pady=8)',
        'username_entry = tk.Entry(root, font=("Arial", 11)); username_entry.pack(pady=4)',
        "def start_click():",
        "    u = username_entry.get().strip()",
        '    if not u: messagebox.showwarning("Input", "Enter username!"); return',
        "    pid = register_player(u)",
        "    if pid:",
        "        root.withdraw()",
        "        score, obs = game(pid)",
        "        root.deiconify()",
        'tk.Button(root, text="Start Game", width=16, command=start_click).pack(pady=4)',
        'tk.Button(root, text="Exit", width=16, command=root.destroy).pack(pady=4)',
        "root.mainloop()"
    ]
    story.append(format_code_block(code_p2))
    story.append(PageBreak())

    # ================= PAGE 3 =================
    story.append(make_banner("EXPLANATION FOR MAJOR PARTS (PART 1)", "Database Connectivity, Schema Relational Integrity & Data Logic"))
    story.append(Spacer(1, 4*mm))
    c1 = make_card("DATABASE INIT", "connect() & Db()", [
        ("DDL Automation:", "Initializes the mysql.connector session with error-trapping to prevent abrupt crashes if MySQL is offline."),
        ("Auto Schema:", "Runs CREATE DATABASE and table setup commands automatically on driver launch.")
    ])
    c2 = make_card("SCHEMA DESIGN", "Relational Integrity", [
        ("Primary Keys:", "player stores unique handles with AUTO_INCREMENT ID."),
        ("Highscores:", "1-to-1 relationship with unique player_id foreign key storing best run."),
        ("Game History:", "1-to-Many relationship logging individual runs with TIMESTAMP and CASCADE deletion.")
    ])
    c3 = make_card("PLAYER AUTH", "register_player()", [
        ("Sanitization:", "Queries user handles via parameterized placeholders (%s) to prevent SQL injection vulnerabilities."),
        ("Key Retrieval:", "Fetches existing players_id or executes INSERT and returns cursor.lastrowid.")
    ])
    c4 = make_card("SCORE TRACKING", "save_scores() / history", [
        ("Conditional Update:", "save_scores() queries personal best and updates record only upon a new highscore."),
        ("Run Auditing:", "Continuously logs score, obstacle count, and timestamp for statistical verification.")
    ])

    grid_p3 = Table([[c1, c2], [c3, c4]], colWidths=[91*mm, 91*mm])
    grid_p3.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
    ]))
    story.append(grid_p3)
    story.append(PageBreak())

    # ================= PAGE 4 =================
    story.append(make_banner("EXPLANATION FOR MAJOR PARTS (PART 2)", "Tkinter GUI Dashboard & Pygame 2D Physics Mechanics"))
    story.append(Spacer(1, 4*mm))
    c5 = make_card("GUI DASHBOARD", "Tkinter Windows", [
        ("Input Validation:", "Validates player credentials before spawning game loop."),
        ("Driver Flow:", "Handles start click, hides main window during Pygame execution, and cleanly recovers after game over.")
    ])
    c6 = make_card("JUMP PHYSICS", "Discrete Mechanics", [
        ("Impulse & Gravity:", "SPACE triggers upward velocity (-15); gravity increments velocity frame-by-frame."),
        ("Ground Check:", "Detects ground boundary and clamps vertical position to halt displacement.")
    ])
    c7 = make_card("DYNAMIC OBSTACLES", "Procedural Spawning", [
        ("Dimensions:", "Randomly picks from small, tall, or wide obstacle hitboxes."),
        ("Dynamic Spacing:", "Scales spawn intervals inversely with movement speed so jumps remain playable."),
        ("Difficulty Scaling:", "Increases speed by +2 after every 5 cleared obstacles.")
    ])
    c8 = make_card("COLLISION & LOOP", "Pygame 60 FPS", [
        ("Hitbox Check:", "Uses pygame.Rect.colliderect() at 60 FPS for instant collision testing."),
        ("Memory Cleanup:", "Prunes offscreen obstacles to prevent list memory leaks."),
        ("Auto Commit:", "Triggers database record persistence instantly upon collision.")
    ])

    grid_p4 = Table([[c5, c6], [c7, c8]], colWidths=[91*mm, 91*mm])
    grid_p4.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
        ('TOPPADDING', (0,0), (-1,-1), 2*mm),
    ]))
    story.append(grid_p4)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated clean 4-page PDF: {filename}")

if __name__ == "__main__":
    build_pdf()