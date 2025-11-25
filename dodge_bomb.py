import os
import sys
import pygame as pg
import random
import math
import pygame.math as pgm


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Bomb:
    """ばくだんをあらわすクラス"""
    def __init__(self, img: pg.Surface, rct: pg.Rect, direction = random.uniform(0, 360), speed = 5, sensitivity = 3):
        """
        引数：ばくだん画像Surface，ばくだんRect，進行方向（デフォルトはランダム），速度（デフォルト5），感度（デフォルト3）
        """ 
        self.img = img
        self.rct = rct
        self.vector = pgm.Vector2.from_polar((speed, direction))
        self.develop_progress = 0
        self.sensitivity = sensitivity  # Adjust this value to change how quickly the bullet homes in

    def move(self, target_rct: pg.Rect):
        """
        ばくだんを進行方向にspeedだけ動かす。画面外に出たら跳ね返る。
        目標（こうかとん）に向かって徐々に進行方向を変える。
        引数：目標のRect
        """
        yoko, tate = check_bound(self.rct)
        if not yoko:
            self.vector = pgm.Vector2.from_polar((self.vector.length(), 180 - self.vector.as_polar()[1]))
        if not tate:
            self.vector = pgm.Vector2.from_polar((self.vector.length(), -self.vector.as_polar()[1]))

        target_vector = pgm.Vector2(target_rct.center)
        self_vector = pgm.Vector2(self.rct.center)
        direction = target_vector - self_vector
        
        # Calculate angle difference properly handling wraparound
        target_angle = direction.as_polar()[1]
        current_angle = self.vector.as_polar()[1]
        angle_diff = (target_angle - current_angle + 180) % 360 - 180
        
        if abs(angle_diff) < self.sensitivity:
            self.vector = pgm.Vector2.from_polar((self.vector.length(), target_angle))
        else:
            self.vector.rotate_ip(self.sensitivity if angle_diff > 0 else -self.sensitivity)

        self.rct.move_ip(self.vector)

    def develop(self):
        """ばくだんを徐々に大きくする、速度を上げる"""
        self.develop_progress += 1
        if self.develop_progress >= 100:
            # increase size
            new_surface = pg.Surface((self.img.get_width() + 2, self.img.get_height() + 2))
            new_surface.set_colorkey((0, 0, 0))
            pg.draw.circle(new_surface, (255, 0, 0), (new_surface.get_width() // 2, new_surface.get_height() // 2), new_surface.get_width() // 2)
            self.img = new_surface
            self.rct = self.img.get_rect(center=self.rct.center)
            self.develop_progress = 0

            #increase speed
            speed = self.vector.length() * 1.1
            self.vector = pgm.Vector2.from_polar((speed, self.vector.as_polar()[1]))


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

    # こうかとんの向き別画像辞書
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

    # 初期こうかとん
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    clock = pg.time.Clock()
    tmr = 0
    bullets = []

    # 爆弾追加
    for i in range(5):
        bb_img = pg.Surface((20, 20))
        bb_rct = bb_img.get_rect()
        bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
        bb_img.set_colorkey((0, 0, 0))
        bullets.append(Bomb(bb_img, bb_rct, random.uniform(0, 360), speed=random.randint(2, 4), sensitivity=random.uniform(2, 5)))

    # gameover screen
    black_screen = pg.Surface((WIDTH, HEIGHT))
    black_screen.fill((0, 0, 0))
    font = pg.font.Font(None, 150)
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = WIDTH // 2, HEIGHT // 2

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        # move bullet (homing behavior)
        for bullet in bullets:
            bullet.move(kk_rct)
            screen.blit(bullet.img, bullet.rct)

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
        for bullet in bullets:
            if kk_rct.colliderect(bullet.rct):
                # display game over screen
                screen.blit(black_screen, (0, 0))
                screen.blit(text, text_rect)
                pg.display.update()
                pg.time.wait(2000)
                return
        # bullet develop
        for bullet in bullets:
            bullet.develop()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
