import pygame as p, random as r, os
p.init()
S, F = p.display.set_mode((800,800)), p.time.Clock()
p.display.set_caption("Snake Game")
font, HS_FILE, HS_COUNT = p.font.SysFont(None, 36), "highscores.txt", 5

def f(snake):
    while 1:
        pos = [r.randrange(0,800,20), r.randrange(0,800,20)]
        if tuple(pos) not in snake: return pos

def load_scores():
    if not os.path.exists(HS_FILE): return []
    with open(HS_FILE) as f:
        return sorted([(n,int(s)) for n,s in [l.strip().split(",",1) for l in f if "," in l]], key=lambda x:x[1], reverse=True)[:HS_COUNT]

def save_score(n,s): open(HS_FILE,"a").write(f"{n},{s}\n")

def enter_name():
    name, big = "", p.font.SysFont(None,48)
    while True:
        S.fill((0,0,0))
        S.blit(big.render('Dein Name:',1,(255,255,255)),(300,250))
        S.blit(font.render(name+"|",1,(0,255,0)),(300,300))
        p.display.flip()
        for e in p.event.get():
            if e.type == p.QUIT: p.quit(); exit()
            if e.type == p.KEYDOWN:
                if e.key == p.K_RETURN and name.strip(): return name.strip()
                if e.key == p.K_BACKSPACE: name = name[:-1]
                elif len(name) < 20: name += e.unicode

def show_scores(scores):
    S.fill((0,0,0))
    S.blit(p.font.SysFont(None,48).render("Highscores",1,(255,255,0)),(300,150))
    for i,(n,s) in enumerate(scores):
        S.blit(font.render(f"{i+1}. {n} - {s}",1,(255,255,255)),(250,200+i*30))

def game():
    snake,d,food,score,last = [(20,20)],(20,0),f([]),0,p.time.get_ticks()
    while True:
        for e in p.event.get():
            if e.type==p.QUIT: return None
            if e.type==p.KEYDOWN:
                k={p.K_UP:(0,-20),p.K_DOWN:(0,20),p.K_LEFT:(-20,0),p.K_RIGHT:(20,0)}.get(e.key)
                if k and (k[0]+d[0],k[1]+d[1])!=(0,0): d=k
        if p.time.get_ticks()-last>=100:
            last = p.time.get_ticks()
            snake = [(snake[0][0]+d[0],snake[0][1]+d[1])]+snake
            if snake[0]==tuple(food): food,score = f(snake),score+1
            else: snake.pop()
        S.fill((0,0,0))
        [p.draw.rect(S,(0,255,0),(*s,20,20)) for s in snake]
        p.draw.rect(S,(255,0,0),(*food,20,20))
        S.blit(font.render(f'Score: {score}',1,(255,255,255)),(10,10))
        p.display.flip()
        F.tick(60)
        if not(0<=snake[0][0]<800 and 0<=snake[0][1]<800) or snake[0] in snake[1:]: return score

while True:
    score = game()
    if score is None: break
    name = enter_name()
    save_score(name,score)
    scores = load_scores()
    show_scores(scores)
    S.blit(p.font.SysFont(None,48).render('Game Over',1,(255,0,0)),(310,200+HS_COUNT*30+40))
    S.blit(font.render(f'Score: {score} | R: Neustart | ESC: Beenden',1,(255,255,255)),(190,200+HS_COUNT*30+80))
    p.display.flip()
    while True:
        for e in p.event.get():
            if e.type==p.QUIT: p.quit();exit()
            if e.type==p.KEYDOWN:
                if e.key==p.K_r: break
                if e.key==p.K_ESCAPE: p.quit();exit()
        else: continue
        break
