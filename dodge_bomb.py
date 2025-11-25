import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0

    # bullet
    bb_img = pg.Surface((20, 20))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5, +5

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        
        # bullet movement
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)


        key_lst = pg.key.get_pressed()
        DELTA = (0, 0,)
        if key_lst[pg.K_UP]:
            DELTA = (DELTA[0], DELTA[1] - 5)
        if key_lst[pg.K_DOWN]:
            DELTA = (DELTA[0], DELTA[1] + 5)
        if key_lst[pg.K_LEFT]:
            DELTA = (DELTA[0] - 5, DELTA[1])
        if key_lst[pg.K_RIGHT]:
            DELTA = (DELTA[0] + 5, DELTA[1])
        if check_bound(kk_rct.move(DELTA)) == (True, True):
            kk_rct.move_ip(DELTA)
        screen.blit(kk_img, kk_rct)
        pg.display.update()

        # collision check
        if kk_rct.colliderect(bb_rct):
            return

        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
