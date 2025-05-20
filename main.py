import pygame as p, random as r, os
p.init()
flags = 0 if os.environ.get("XDG_SESSION_TYPE") == "wayland" else p.RESIZABLE
S = p.display.set_mode((1000, 1000), flags)
F = p.time.Clock()
p.display.set_caption("Snake Game")
font, HS_FILE, HS_COUNT = p.font.SysFont(None, 36), "highscores.txt", 5
SPIELFELD_GR, FELD_GR = 800, 20

def f(snake):
    while True:
        pos = [r.randrange(0, SPIELFELD_GR, FELD_GR), r.randrange(0, SPIELFELD_GR, FELD_GR)]
        if tuple(pos) not in snake:
            return pos

def load_scores():
    return sorted([(n, int(s)) for n, s in (line.strip().split(",", 1) for line in open(HS_FILE))],
                  key=lambda x: x[1], reverse=True)[:HS_COUNT] if os.path.exists(HS_FILE) else []

def save_score(n,s): open(HS_FILE,"a").write(f"{n},{s}\n")

def enter_name():
    name, big = "", p.font.SysFont(None,48)
    while True:
        S.fill((0,0,0))
        msg = big.render('Dein Name:',1,(255,255,255))
        S.blit(msg, ((S.get_width()-msg.get_width())//2, 250))
        t = font.render(name+"|",1,(0,255,0))
        x = (S.get_width()-t.get_width())//2
        S.blit(t,(x,300))
        p.display.flip()
        for e in p.event.get():
            if e.type==p.QUIT: p.quit(); exit()
            if e.type==p.KEYDOWN:
                if e.key==p.K_RETURN and name.strip(): return name.strip()
                if e.key==p.K_BACKSPACE: name = name[:-1]
                elif len(name)<20: name += e.unicode

def show_scores(scores, offset):
    S.fill((0,0,0))
    S.blit(p.font.SysFont(None,48).render("Highscores",1,(255,255,0)),(offset[0]+300,offset[1]+150))
    for i,(n,s) in enumerate(scores):
        S.blit(font.render(f"{i+1}. {n} - {s}",1,(255,255,255)),(offset[0]+250,offset[1]+200+i*30))

def get_offset():
    w, h = S.get_size()
    return ((w - SPIELFELD_GR) // 2, (h - SPIELFELD_GR) // 2)

def draw_playfield(snake, food, score, offset):
    S.fill((30, 30, 30))
    p.draw.rect(S, (100, 100, 100), (*offset, SPIELFELD_GR, SPIELFELD_GR), 4)
    for s in snake:
        p.draw.rect(S, (0,255,0), (offset[0]+s[0], offset[1]+s[1], FELD_GR, FELD_GR))
    p.draw.rect(S, (255,0,0), (offset[0]+food[0], offset[1]+food[1], FELD_GR, FELD_GR))
    S.blit(font.render(f'Score: {score}', 1, (255,255,255)), (offset[0]+10, offset[1]+10))

def game():
    snake,d,food,score,last = [(20,20)],(FELD_GR,0),f([]),0,p.time.get_ticks()
    while True:
        for e in p.event.get():
            if e.type==p.QUIT: return None
            if e.type==p.KEYDOWN:
                k={p.K_UP:(0,-FELD_GR),p.K_DOWN:(0,FELD_GR),p.K_LEFT:(-FELD_GR,0),p.K_RIGHT:(FELD_GR,0)}.get(e.key)
                if k and (k[0]+d[0],k[1]+d[1])!=(0,0): d=k
        if p.time.get_ticks()-last>=100:
            last = p.time.get_ticks()
            snake = [(snake[0][0]+d[0],snake[0][1]+d[1])]+snake
            if snake[0]==tuple(food): food,score = f(snake),score+1
            else: snake.pop()
        offset = get_offset()
        draw_playfield(snake, food, score, offset)
        p.display.flip()
        F.tick(60)
        if not(0<=snake[0][0]<SPIELFELD_GR and 0<=snake[0][1]<SPIELFELD_GR) or snake[0] in snake[1:]: return score

while True:
    score = game()
    if score is None: break
    name = enter_name()
    save_score(name, score)
    scores = load_scores()
    while True:
        offset = get_offset()
        show_scores(scores, offset)
        S.blit(p.font.SysFont(None, 48).render('Game Over', 1, (255, 0, 0)), (offset[0]+310, offset[1]+200+HS_COUNT*30+40))
        S.blit(font.render(f'Score: {score} | R: Neustart | ESC: Beenden', 1, (255, 255, 255)), (offset[0]+190, offset[1]+200+HS_COUNT*30+80))
        p.display.flip()
        for e in p.event.get():
            if e.type == p.QUIT: p.quit(); exit()
            if e.type == p.KEYDOWN:
                if e.key == p.K_r: break
                if e.key == p.K_ESCAPE: p.quit(); exit()
        else:
            F.tick(60)
            continue
        break