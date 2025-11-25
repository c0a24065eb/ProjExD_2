import os
import sys
import pygame as pg
import random
import math


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
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
    kk_img = pg.image.load("fig/3.png")
    kk_direction_dict = {
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 0.9),
        (5, 0): pg.transform.flip(kk_img, True, False),
        (0, 5): pg.transform.rotozoom(pg.transform.flip(kk_img, False, True), 90, 0.9),
        (0, -5): pg.transform.flip(pg.transform.rotozoom(kk_img, -90, 0.9), True, False),
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 0.9),
        (5, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 45, 0.9),
        (-5, 5): pg.transform.rotozoom(kk_img, 45, 0.9),
        (5, 5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -45, 0.9),
    }
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
    bullet_speed_size_increase_interval = 100  # Increase speed and size every 100 frames
    bullet_speed_increment = 1.1  # Speed increment value
    bullet_size_increment = 2  # Size increment value
    bullet_timer = 0

    # gameover screen
    black_screen = pg.Surface((WIDTH, HEIGHT))
    black_screen.fill((0, 0, 0))
    font = pg.font.Font(None, 150)
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = WIDTH // 2, HEIGHT // 2
    game_over_displayed = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        
        # bullet 
        if bullet_timer >= bullet_speed_size_increase_interval:
            vx *= bullet_speed_increment
            vy *= bullet_speed_increment
            bb_new_img = pg.Surface((bb_rct.width + bullet_size_increment, bb_rct.height + bullet_size_increment))
            pg.draw.circle(bb_new_img, (255, 0, 0), (bb_new_img.get_width() // 2, bb_new_img.get_height() // 2), bb_new_img.get_width() // 2)
            bb_new_img.set_colorkey((0, 0, 0))
            bb_img = bb_new_img
            bb_rct = bb_img.get_rect(center=bb_rct.center)
            bullet_timer = 0

        # move bullet
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

        kk_img = kk_direction_dict.get(DELTA, kk_img) if DELTA != (0, 0) else kk_img
        
        if check_bound(kk_rct.move(DELTA)) == (True, True):
            kk_rct.move_ip(DELTA)
        screen.blit(kk_img, kk_rct)
        pg.display.update()

        # collision check
        if kk_rct.colliderect(bb_rct):
            # display game over screen
            screen.blit(black_screen, (0, 0))
            screen.blit(text, text_rect)
            pg.display.update()
            pg.time.wait(2000)
            return

        tmr += 1
        bullet_timer += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
