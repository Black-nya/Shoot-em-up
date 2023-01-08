import pygame
import sys
import traceback
from pygame.locals import *
from random import *
import player
import Enemy
import bullet
import supply

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Shoooot'em")
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

background = pygame.image.load("images/background.png").convert()

def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1 = Enemy.Small(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1,group2,num):
    for i in range(num):
        e1 = Enemy.Medium(bg_size)
        group1.add(e1)
        group2.add(e1)
def add_large_enemies(group1,group2,num):
    for i in range(num):
        e1 = Enemy.Large(bg_size)
        group1.add(e1)
        group2.add(e1)
        
def speedup(target, speed):
    for i in target:
        i.speed+=speed

def level(n,small_enemies,mid_enemies,large_enemies,enemies):
    if not n%1:    
        add_small_enemies(small_enemies, enemies,15)
        add_mid_enemies(mid_enemies, enemies,10)
        add_large_enemies(large_enemies, enemies,5)
    elif not n%2:
        add_small_enemies(small_enemies, enemies,5)
        add_mid_enemies(mid_enemies, enemies,3)
        add_large_enemies(large_enemies, enemies,1)
        speedup(small_enemies,1)
    elif not n%3:
        add_small_enemies(small_enemies, enemies,5)
        add_mid_enemies(mid_enemies, enemies,3)
        add_large_enemies(large_enemies, enemies,2)
        speedup(small_enemies,2)
        speedup(mid_enemies,2)
    elif not n%4:
        add_small_enemies(small_enemies, enemies,5)
        add_mid_enemies(mid_enemies, enemies,3)
        add_large_enemies(large_enemies, enemies,2)
        speedup(small_enemies,3)
        speedup(mid_enemies,3)
        speedup(large_enemies,3)
        
def main():
    #pygame.mixer.music.play(-1)

    me = player.Player(bg_size)

    running = True

    clock = pygame.time.Clock()

    enemies = pygame.sprite.Group()

    # generate enemy groups
    small_enemies = pygame.sprite.Group()
    mid_enemies = pygame.sprite.Group()
    large_enemies = pygame.sprite.Group()

    #generate bullets
    bullet1 = []
    bullet1_index = 0
    BULLET_NUM = 5
    for i in range(BULLET_NUM):
        bullet1.append(bullet.Bullet(me.rect.midtop))

    # generate special bullets
    bullet2 = []
    bullet2_index = 0
    for i in range(BULLET_NUM):
        bullet2.append(bullet.Bullet_supper((me.rect.centerx-33,me.rect.centery)))
        bullet2.append(bullet.Bullet_supper((me.rect.centerx+30,me.rect.centery)))

    #destroy_image_index
    e1_destroy_image_index = 0
    e2_destroy_image_index = 0
    e3_destroy_image_index = 0
    me_destroy_image_index = 0

    # switch image
    switch = True

    # delay
    delay = 100

    score = 0
    font = pygame.font.Font("font/Fresh Lychee.ttf", 36)
    Gameover_font = pygame.font.Font("font/Fresh Lychee.ttf", 48)
    
    paused = False
    pause1 = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause2 = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume1 = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume2 = pygame.image.load("images/resume_pressed.png").convert_alpha()
    paused_rect = pause1.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width, 10
    paused_image = pause1

    #level
    lev = 0

    #initialize 3 bombs
    bomb_image =  pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_num = 3

    # one supply every 30s
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    TIMER = USEREVENT
    pygame.time.set_timer(TIMER,30000)

    # Supper bullet timer
    DOUBLE_BULLET_TIMER = USEREVENT +1
    is_double_bullet = False

    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life = 3

    #invincible timer
    Invincible_Timer = USEREVENT +2

    recorded = False

    play_again = pygame.image.load("images/again.png").convert_alpha()
    game_over = pygame.image.load("images/gameover.png").convert_alpha()
    play_again_p = pygame.image.load("images/again_pressed.png").convert_alpha()
    game_over_p = pygame.image.load("images/gameover_pressed.png").convert_alpha()
    again_rect = play_again.get_rect()
    over_rect = game_over.get_rect()
        
    while running:

        screen.blit(background, (0,0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        paused_image = resume2
                        pygame.time.set_timer(TIMER,0)
                    else:
                        paused_image = pause2
                        pygame.time.set_timer(TIMER,30000)
                    
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume2
                    else:
                        paused_image = pause2
                else:
                    if paused:
                        paused_image = resume1
                    else:
                        paused_image = pause1
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        for each in enemies:
                            if each.rect.bottom>0:
                                each.live = False
                                
            elif event.type == TIMER:
                if choice([True,False]):
                    bullet_supply.reset()
                else:
                    bomb_supply.reset()
                    
            elif event.type == DOUBLE_BULLET_TIMER:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIMER,0)

            elif event.type == Invincible_Timer:
                me.invincible = False
                pygame.time.set_timer(Invincible_Timer,0)
        
        if score<500 and lev==0:
            lev = 1
            level(lev,small_enemies,mid_enemies,large_enemies,enemies)
        elif lev==1 and 500<=score<1500:
            lev = 2
            level(lev,small_enemies,mid_enemies,large_enemies,enemies)
        elif lev==2 and 1500<=score<2500:
            lev = 3
            level(lev,small_enemies,mid_enemies,large_enemies,enemies)
        elif lev ==3 and 2500<=score<3500:
            lev = 4
            level(lev,small_enemies,mid_enemies,large_enemies,enemies)

         
        if not paused and life:
             
            key_pressed = pygame.key.get_pressed()
            
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    bomb_num+=1
                    bomb_supply.active = False
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply,me):
                    pygame.time.set_timer(DOUBLE_BULLET_TIMER,18000)
                    is_double_bullet = True
                    bullet_supply.active = False

            # shoot bullet
            if not(delay%10):
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx-33,me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx+30,me.rect.centery))
                    bullet2_index = (bullet2_index +2)%(BULLET_NUM*2)
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index +1)%BULLET_NUM

            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in large_enemies:
                                e.hit = True
                                e.health -= 1
                                if e.health == 0:
                                    e.live = False
                            else:
                                e.live = False
            # blit large enemies
            for enemy in large_enemies:
                if enemy.live:
                    enemy.move()
                    if enemy.hit:
                        screen.blit(enemy.image_hit, enemy.rect)
                        enemy.hit = False
                    else:
                        if switch:
                            screen.blit(enemy.image1, enemy.rect)
                        else:
                            screen.blit(enemy.image2, enemy.rect)

                    pygame.draw.line(screen, BLACK,(enemy.rect.left,enemy.rect.top-5),(enemy.rect.right,enemy.rect.top-5),2)
                    health_remain = enemy.health / Enemy.Large.health
                    if health_remain > 0.2:
                        health_color = GREEN
                    else:
                        health_color = RED
                    pygame.draw.line(screen,health_color,(enemy.rect.left,enemy.rect.top-5),(enemy.rect.width*health_remain+enemy.rect.left,enemy.rect.top-5),2)
                    
                    #play sound when large plane is coming
                    if enemy.rect.bottom > -50:
                        pass
                else:
                    #destroy
                    if not(delay %3):
                        screen.blit(enemy.destroy_images[e3_destroy_image_index],enemy.rect)
                        e3_destroy_image_index = (e3_destroy_image_index+1)%6
                        if e3_destroy_image_index == 0:
                            score += 100
                            enemy.reset()
                    
            # blit medium enemies
            for enemy in mid_enemies:
                if enemy.live:
                    enemy.move()
                    if enemy.hit:
                        screen.blit(enemy.image_hit, enemy.rect)
                        enemy.hit = False
                    else:
                        screen.blit(enemy.image, enemy.rect)

                    pygame.draw.line(screen, BLACK,(enemy.rect.left,enemy.rect.top-5),(enemy.rect.right,enemy.rect.top-5),2)
                    health_remain = enemy.health / Enemy.Medium.health
                    if health_remain > 0.2:
                        health_color = GREEN
                    else:
                        health_color = RED
                    pygame.draw.line(screen,health_color,(enemy.rect.left,enemy.rect.top-5),(enemy.rect.width*health_remain+enemy.rect.left,enemy.rect.top-5),2)
                else:
                    if not(delay %3):
                        screen.blit(enemy.destroy_images[e2_destroy_image_index],enemy.rect)
                        e2_destroy_image_index = (e2_destroy_image_index+1)%4
                        if e2_destroy_image_index == 0:
                            score += 10
                            enemy.reset()
            # blit small enemies
            for enemy in small_enemies:
                if enemy.live:
                    enemy.move()
                    screen.blit(enemy.image, enemy.rect)
                else:
                    if not(delay %3):
                        screen.blit(enemy.destroy_images[e1_destroy_image_index],enemy.rect)
                        e1_destroy_image_index = (e1_destroy_image_index+1)%4
                        if e1_destroy_image_index == 0:
                            score += 1
                            enemy.reset()
                            
            # collision between player and enemies           
            enemies_down = pygame.sprite.spritecollide(me, enemies,False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.live = False
                for e in enemies_down:
                    e.live = False
                    
            # 1,2,2,2,2,2,1,1,1,1,1
            # switch image every 5 frames
            if me.live:
                if switch:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                if not(delay %3):
                    screen.blit(me.destroy_images[me_destroy_image_index],me.rect)
                    me_destroy_image_index = (me_destroy_image_index+1)%4
                    if me_destroy_image_index == 0:
                        life -=1
                        me.reset()
                        pygame.time.set_timer(Invincible_Timer,3000)
            
            # display number of bombs
            bomb_text = font.render("x %d" % bomb_num,True,WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image,(10, height-10-bomb_rect.height))
            screen.blit(bomb_text,(20+bomb_rect.width, height -5-text_rect.height))

            if life:
                for i in range(life):
                    screen.blit(life_image,(width-10-(i+1)*life_rect.width, height-10-life_rect.height))

            #display score
            score_text = font.render("Score : %s"%str(score), True, WHITE)
            screen.blit(score_text,(10,5))
            
        elif life ==0:
            pygame.time.set_timer(TIMER,0)         

            if not recorded:
                recorded = True
                with open("record.txt","r") as f:
                    record_score = int(f.read())

                if score > record_score:
                    with open("record.txt","w") as f:
                        f.write(str(score))
            # Game over screen
            
            record_txt = font.render("Best : %d"%record_score,True,WHITE)
            screen.blit(record_txt,(10,5))
            score_txt1 = Gameover_font.render("Your Score:",True,WHITE)
            temp = score_txt1.get_rect()
            screen.blit(score_txt1,((width-temp.width)//2,250))
            score_txt2 = Gameover_font.render("%d"%score,True,WHITE)
            temp = score_txt2.get_rect()
            screen.blit(score_txt2,((width-temp.width)//2,290))
            again_rect.left,again_rect.top = (width-again_rect.width)//2, 350
            over_rect.left,over_rect.top = (width-over_rect.width)//2, 400
            screen.blit(play_again,again_rect)
            screen.blit(game_over,over_rect)

            pos = pygame.mouse.get_pos()

            if again_rect.left<pos[0]<again_rect.right and again_rect.top<pos[1]<again_rect.bottom:
                if pygame.mouse.get_pressed()[0]:
                    main()
                else:
                    screen.blit(play_again_p,again_rect)
            elif over_rect.left<pos[0]<over_rect.right and over_rect.top<pos[1]<over_rect.bottom:
                if pygame.mouse.get_pressed()[0]:
                    pygame.quit()
                    sys.exit()
                else:
                    screen.blit(game_over_p,over_rect)
                
        screen.blit(paused_image,paused_rect)
        
        if not (delay%5):
            switch = not switch
        delay -=1

        if not delay:
            delay =100
            
        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
