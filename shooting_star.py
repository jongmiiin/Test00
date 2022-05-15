
import random
import pygame # 파이게임 실행을 위한 라이브러리

from time import sleep
from pygame.locals import *
from datetime import datetime 

WINDOW_WIDTH = 480 # x축 (오른쪽이 값 증가)
WINDOW_HEIGHT = 640 # y축 (아래가 값 증가)

# 컬러
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (250,250,50)
RED = (250,50,50)

FPS = 60 # 1초에 몇 프레임이냐

# 플레이어 구현
class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        super(Fighter, self).__init__()
        self.image = pygame.image.load('fighter.png') #플레이어 이미지 가져오기
        self.rect = self.image.get_rect()
        self.rect.x = int(WINDOW_WIDTH / 2) # 처음 플레이어 위치 설정
        self.rect.y = WINDOW_HEIGHT - self.rect.height
        self.dx = 0
        self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        #화면 밖으로 나가는 거 방지 (y축 버그: 화면 밖으로 나가짐)
        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH:
            self.rect.x -= self.dx
        
        if self.rect.y < 0 or self.rect.y + self.rect.height > WINDOW_HEIGHT:
            self.rect.y -= self.dy
        
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

# 보스 구현
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        self.image = pygame.image.load('boss.png') #보스 이미지 가져오기 
        self.rect = self.image.get_rect()
        self.rect.x = int(WINDOW_WIDTH - 300) # 처음 위치 설정
        self.rect.y = WINDOW_HEIGHT - 600
        self.dx = 0
        self.dy = 0
    
    # 화면 밖으로 나가는 거 방지
    def update(self):
        self.rect.x += self.dx
        if self.rect.x + self.rect.width >= WINDOW_WIDTH:
            self.rect.x -= self.dx
        self.rect.y += self.dy
        if self.rect.y + self.rect.height >= 300:
            self.rect.y -= self.dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

#미사일 구현
class Missile(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Missile, self). __init__()
        self.image = pygame.image.load('missile.png') # 미사일 이미지 구현
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        self.sound = pygame.mixer.Sound('missile.wav') #소리 구현

    def launch(self):
        self.sound.play()

    def update(self):
        self.rect.y -= self.speed  # 미사일 발사

        #화면 밖으로 나가는 거 제거
        if self.rect.y + self.rect.height < 0:
            self.kill()
        
    def collide(self,sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite
# 레이저 구현
class Lazer(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Lazer, self). __init__()
        self.image = pygame.image.load('lazer.png') # 레이저 이미지 구현 (이미지 좋은 거 좀 써주세요)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        self.sound = pygame.mixer.Sound('missile.wav') #소리 구현

    def launch(self):
        self.sound.play()

    def update(self):
        self.rect.y -= self.speed  # 레이저 발사

        #화면 밖으로 나가는 거 제거
        if self.rect.y + self.rect.height < 0:
            self.kill()
        
    def collide(self,sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

#보스 공격 구현 (Bossmissile)
class Bossmissile(pygame.sprite.Sprite):    
    def __init__(self, xpos, ypos, speed):
        super(Bossmissile, self).__init__()
        #rock_images = ('rock01.png','rock02.png','rock03.png','rock04.png','rock05.png',\
            #'rock06.png','rock07.png','rock08.png','rock09.png','rock10.png')
        self.image = pygame.image.load('bossmissile.png')
        #self.image = pygame.image.load(random.choice(rock_images))
        self.rect = self.image.get_rect()
        self.rect.x = xpos # 위치값
        self.rect.y = ypos 
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    #화면 밖으로 나가는 것 체크
    def out_of_screen(self):
        if self.rect.y > WINDOW_HEIGHT:
            self.kill()

# 회복 아이템
class Heal(pygame.sprite.Sprite):    
    def __init__(self, xpos, ypos, speed):
        super(Heal, self).__init__()
        
        self.image = pygame.image.load('heal.png')
        #self.image = pygame.image.load(random.choice(rock_images))
        self.rect = self.image.get_rect()
        self.rect.x = xpos # 위치값
        self.rect.y = ypos 
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    #화면 밖으로 나가는 것 체크
    def out_of_screen(self):
        if self.rect.y > WINDOW_HEIGHT:
            return True

#글자 출력
def draw_text(text, font, surface, x ,y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)

#폭발
def occur_explosion(surface, x ,y):
    explosion_image = pygame.image.load('explosion.png')
    explosion_rect = explosion_image.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    surface.blit(explosion_image, explosion_rect)

    explosion_sounds = ('explosion01.wav','explosion02.wav','explosion03.wav')
    explosion_sound = pygame.mixer.Sound(random.choice(explosion_sounds))
    explosion_sound.play()


#반복으로 화면처리, 이벤트처리
def game_loop():
    default_font = pygame.font.Font('NanumGothic.ttf', 17) # 기본 폰트, 글자 크기
    background_image = pygame.image.load('background.png') # 배경이미지
    gameover_sound = pygame.mixer.Sound('gameover.wav') # 게임오버 효과음
    pygame.mixer.music.load('music.wav') # bgm 가져오기
    pygame.mixer.music.play(-1) # 몇 번 반복할건가 (-1은 무한반복)
    fps_clock = pygame.time.Clock() # 시간
    

    fighter = Fighter() # 플레이어 
    boss = Boss() # 보스
    missiles = pygame.sprite.Group() # 미사일
    bossmissiles = pygame.sprite.Group() # 보스 공격
    heals = pygame.sprite.Group() # 회복 아이템
    lazers = pygame.sprite.Group() # 레이저(스킬) 

    occur_prob = 30 # 확률적으로 얼만큼 나오게 할 것인가 (낮을수록 보스가 더 자주 공격함)
    shot_count = 0 # 점수
    count_life = 3 # 목숨
    boss_hp = 100 # 보스 hp
    start_time = datetime.now() # 시작 시간
    missile_count = 40 # 미사일 개수 
    occur_prob_heal = 800 # 아이템 등장 확률 (높을수록 등장 확률 희박)
    re_fill = 3 # 재장전 카운트
    lazer_count = 5 # 사용가능 레이저 개수 
    untouchable_mode = False 
    untouchable_start = 0 


    done = False
    
    while not done:
        for event in pygame.event.get():
            # 조작키
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    fighter.dx -= 5
                elif event.key == pygame.K_RIGHT:
                    fighter.dx += 5
                elif event.key == pygame.K_UP:
                    fighter.dy -= 5
                elif event.key == pygame.K_DOWN:
                    fighter.dy += 5
                elif event.key == pygame.K_SPACE: # 미사일 발사
                    if missile_count > 0: # 미사일이 있으면 발사, 없으면 발사 X
                        missile_count -= 1
                        missile = Missile(fighter.rect.centerx, fighter.rect.y, 10)
                        missile.launch()
                        missiles.add(missile)
                    elif missile_count == 0: # 미사일 재장전
                        if re_fill > 0:
                            missile_count += 30
                            re_fill -= 1
                elif event.key == pygame.K_a: # A를 눌러 레이저 발사 (스킬)
                    if lazer_count > 0:
                        lazer = Lazer(fighter.rect.centerx, fighter.rect.y, 20)
                        lazer_count -= 1
                        lazer.launch()
                        lazers.add(lazer)
                elif event.key == pygame.K_ESCAPE: # Esc를 누르면 게임 클리어
                    done = True
                    game_clear(shot_count)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighter.dx = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighter.dy = 0
        
       
        screen.blit(background_image, background_image.get_rect())

        now_time = datetime.now() # 계속 증가하는 시간
        delta_time = 100 + round((start_time - now_time).total_seconds()) # 제한 시간
        
        # 보스의 체력에 따라 난이도 조절 (체력이 낮을수록 암석 속도 증가)
        occur_of_bossmissile = 2 + int((100-boss_hp) / 100)
        min_bossmissile_speed = 2 + int((100-boss_hp) / 50)
        max_bossmissile_speed = 2 + int((100-boss_hp) / 25)
        occur_of_heals = 1

        # 보스의 공격
        if random.randint(1, occur_prob) == 1:
            for i in range(occur_of_bossmissile):
                speed = random.randint(min_bossmissile_speed, max_bossmissile_speed)
                bossmissile = Bossmissile(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
                bossmissiles.add(bossmissile)
        # 회복 아이템 등장
        if random.randint(1, occur_prob_heal) == 1:
            for i in range(occur_of_heals):
                speed = 2
                heal = Heal(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
                heals.add(heal)
        
        # 텍스트 표시 (점수, 목숨, 남은 시간, 미사일 수, 보스 체력, 재장전, 레이저 수)
        draw_text('SCORE: {}'.format(shot_count),default_font, screen, 80, 20, YELLOW)
        draw_text('LIFE: {}'.format(count_life),default_font, screen, 400, 20, RED)
        draw_text('TIME: {}'.format(delta_time),default_font, screen, 80, 50, WHITE)
        draw_text('MISSILES: {}'.format(missile_count),default_font, screen, 400, 50, YELLOW)
        draw_text('BOSS HP: {}'.format(boss_hp),default_font, screen, 250, 20, RED)
        draw_text('REFILL: {}'.format(re_fill),default_font, screen, 400, 75, YELLOW)
        draw_text('LAZERS(PRESS A): {}'.format(lazer_count),default_font, screen, 80, 75, YELLOW)
        
        for missile in missiles:
            '''
            rock = missile.collide(rocks) # 미사일로 암석 파괴
            if rock:
                missile.kill()
                rock.kill()
                occur_explosion(screen, rock.rect.x, rock.rect.y)
                shot_count += 100
            '''
            missile = boss.collide(missiles) # 미사일로 보스 공격
            if missile:
                missile.kill()
                occur_explosion(screen, missile.rect.x, (missile.rect.y - 30))
                boss_hp -= 1
                shot_count += 200

        for lazer in lazers: # 레이저로 보스의 공격을 격추
            bossmissile = lazer.collide(bossmissiles)
            if bossmissile:
                bossmissile.kill() # 레이저는 관통 공격
                occur_explosion(screen, bossmissile.rect.x, bossmissile.rect.y)
                
            lazer = boss.collide(lazers) # 레이저로 보스 공격
            if lazer:
                occur_explosion(screen, lazer.rect.x, lazer.rect.y)
                boss_hp -= 1
                shot_count += 200

        for bossmissile in bossmissiles:
            bossmissile = fighter.collide(bossmissiles) # 보스 공격에 맞았을 때
            if bossmissile:
                bossmissile.kill()
                count_life -= 1 # 목숨 - 1
                occur_explosion(screen, fighter.rect.x, fighter.rect.y)
                                
        for heal in heals: # 회복 아이템 획득
            heal = fighter.collide(heals)
            if heal:
                heal.kill()
                count_life += 1 # 먹으면 목숨 + 1
                
        bossmissiles.update() # 보스 공격
        bossmissiles.draw(screen)
        missiles.update() # 미사일
        missiles.draw(screen)
        fighter.update() # 플레이어
        fighter.draw(screen)
        boss.update() # 보스
        boss.draw(screen)
        heals.update() # 회복 아이템
        heals.draw(screen)
        lazers.update() # 레이저
        lazers.draw(screen)
        pygame.display.flip()
        
        # 게임오버 (목숨이 0이 되거나 시간이 100초를 넘기면 종료)
        if count_life == 0 or delta_time == 0:
            pygame.mixer_music.stop()
            occur_explosion(screen, fighter.rect.x, fighter.rect.y)
            pygame.display.update()
            gameover_sound.play()
            sleep(1)
            done = True # while 탈출
            game_over(shot_count)
            
        #보스 hp가 0이 되면 게임 클리어
        if boss_hp == 0:
            pygame.mixer_music.stop()
            occur_explosion(screen, boss.rect.x, boss.rect.y)
            pygame.display.update()
            sleep(1)
            done = True # while 탈출
            game_clear(shot_count)
            
        fps_clock.tick(FPS)
    return 'game_menu'

# 게임 오버 창
def game_over(shot_count):
    start_image = pygame.image.load('background.png')
    screen.blit(start_image, [0,0])
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_40 = pygame.font.Font('NanumGothic.ttf', 40)
    draw_text('GAME OVER :(', font_40,screen, draw_x, draw_y + 150, WHITE)
    draw_text('Score: {}'. format(shot_count), font_40,screen, draw_x, draw_y + 200, WHITE)
    pygame.display.update()
    sleep(2)
    return 'game_menu'

# 게임 클리어 창
def game_clear(shot_count):
    start_image = pygame.image.load('background.png')
    screen.blit(start_image, [0,0])
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_40 = pygame.font.Font('NanumGothic.ttf', 40)
    draw_text('GAME CLEAR :)', font_40,screen, draw_x, draw_y + 150, WHITE)
    font_40 = pygame.font.Font('NanumGothic.ttf', 30)
    draw_text('Score: {}'. format(shot_count), font_40,screen, draw_x, draw_y + 200, WHITE)
    pygame.display.update()
    sleep(2)
    return 'game_menu'

# 게임 메뉴 창
def game_menu():
    start_image = pygame.image.load('background.png')
    screen.blit(start_image, [0,0])
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_60 = pygame.font.Font('NanumGothic.ttf', 60)
    font_40 = pygame.font.Font('NanumGothic.ttf', 40)
    font_20 = pygame.font.Font('NanumGothic.ttf', 20)

    draw_text('SHOOTINGSTAR', font_60,screen, draw_x, draw_y, YELLOW)
    draw_text('엔터키를 누르면', font_40,screen, draw_x, draw_y + 150, WHITE)
    draw_text('게임이 시작됩니다', font_40,screen, draw_x, draw_y + 250, WHITE)
    draw_text('스페이스바: 공격    A: 스킬   방향키: 이동', font_20,screen, draw_x, draw_y + 300, WHITE)
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: # 엔터를 눌러 게임 시작
                return 'play'
            else:   # 그 외의 키를 누르면 게임을 시작하지 않고 종료
                return 'quit'

        if event.type == QUIT:
            return 'quit'


    return 'game_menu'

# 메인 함수
def main():
    global screen

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('python_game')

    action = 'game_menu'
    while action != 'quit':
        if action == 'game_menu':
            action = game_menu()
        elif action == 'play':
            action = game_loop()
        
        
    pygame.quit()

if __name__ == "__main__":
    main()
