
import pygame # 파이게임 
import sys
import random # 랜덤
from time import sleep # sleep() 사용
from pygame.locals import * 
from datetime import datetime # 시간 

monMissile = ['monmissile.png']
explosionSound = ['explosion01.wav']

BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (250,250,50)
RED = (250,50,50)

padWidth = 480 # 가로크기 (우로 갈수록 증가)
padHeight = 640 # 세로크기 (아래로 갈수록 증가)

# 게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def initGame():
    global gamePad, clock, background, fighter, missile, explosion, boss, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('ShootingStar') # 게임 이름
    background = pygame.image.load('background.png') # 배경 그림
    fighter = pygame.image.load('fighter.png') #플레이어 이미지 가져오기
    missile = pygame.image.load('missile.png') # 미사일 이미지 구현
    explosion = pygame.image.load('explosion.png') # 폭발 이미지 구현
    boss = pygame.image.load('boss.png') #보스 이미지 가져오기
    pygame.mixer.music.load('music.wav') # bgm
    pygame.mixer.music.play(-1) # bgm 재생 (-1이면 무한반복)
    missileSound = pygame.mixer.Sound('missile.wav') # 미사일 소리
    gameOverSound = pygame.mixer.Sound('gameover.wav') # 게임오버 사운드
    clock = pygame.time.Clock()

# 점수 계산
def Score(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('점수: ' + str(count), True, WHITE)
    gamePad.blit(text,(10,0))

# 남은 목숨
def Life(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('목숨: ' + str(count), True, RED)
    gamePad.blit(text,(390,0))

# 보스 체력
def BossHp(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('HP: ' + str(count), True, RED)
    gamePad.blit(text,(200,0))

# 잔여 미사일
def Missilecount(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('미사일: ' + str(count), True, RED)
    gamePad.blit(text,(10,30))

# 남은 시간
def Time(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('시간: ' + str(count), True, YELLOW)
    gamePad.blit(text,(390,30))


# 게임 메시지 출력
def writeMessage(text):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 80)
    text = font.render(text, True, RED)
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    runGame()


def Gamemenu():
    global gamepad
    


# 게임 클리어

def Gameclear():
    global gamePad
    writeMessage('게임 클리어!')

# 게임 오버창
def Gameover():
    global gamePad
    writeMessage('게임 오버!')

def runGame():
    global gamePad, clock, background, fighter, missile, boss

    # 전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    # 전투기 초기 위치 (x,y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0
    fighterY = 0

    # 보스 크기
    bossSize = boss.get_rect().size
    bossWidth = bossSize[0]
    bossHeight = bossSize[1]
    # 보스 초기 위치
    a = padWidth * 0.4
    b = 20
    bossX = 0
    bossY = 0
    # 무기 좌표 리스트
    missileXY = []
    
    monmissile = pygame.image.load('monmissile.png')
    monmissileSize = monmissile.get_rect().size # 보스 공격 크기 
    monmissileWidth = monmissileSize[0]
    monmissileHeight = monmissileSize[1]

    # 보스 공격 초기 위치 설정
    monmissileX = random.randrange(0,padWidth - monmissileWidth)
    monmissileY = 0
    monmissileSpeed = 2

    Crash = False # 플레이어가 공격에 맞으면 True
    Shot = False # 미사일에 보스가 맞으면 True
    shotpoint = 0 # 점수
    life = 3 # 남은 목숨 
    bosshp = 10 # 보스 체력
    missile_count = 20 # 남은 미사일 수
    start_time = datetime.now() # 시작 시간

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]: # 프로그램 종료
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT: # 왼쪽으로 이동
                    fighterX -= 5 
                elif event.key == pygame.K_RIGHT: # 오른쪽으로 이동
                    fighterX += 5
                elif event.key == pygame.K_UP: # 위로 이동
                    fighterY -= 5
                elif event.key == pygame.K_DOWN: # 아래로 이동
                    fighterY += 5
                elif event.key == pygame.K_a: # 스페이스바로 미사일 공격
                    if missile_count > 0:
                        missileSound.play()
                        missileX = x + fighterWidth/2
                        missileY = y - fighterHeight
                        missileXY.append([missileX, missileY])
                        missile_count -= 1
                

            if event.type in [pygame.KEYUP]: # 방향키를 떼면 전투기 멈춤
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighterY = 0
        now_time = datetime.now() # 계속 증가하는 시간
        delta_time = 100 + round((start_time - now_time).total_seconds()) # 제한 시간
                    
        drawObject(background, 0, 0) # 배경화면 그리기
        # 전투기 위치 재조정
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth
        y += fighterY
        if y < 0:
            y = 0
        elif y > padHeight - fighterHeight:
            y = padHeight - fighterHeight

         # 전투기가 공격에 맞았는지 체크
        if (monmissileY > y and monmissileY < y + fighterHeight) or \
            (monmissileY + monmissileHeight > y and monmissileY + monmissileHeight < y + fighterHeight):
            if (monmissileX > x and monmissileX < x + fighterWidth) or \
                (monmissileX + monmissileWidth > x and monmissileX + monmissileWidth < x + fighterWidth):
                    Crash = True
                    life -= 1 # 맞으면 목숨 - 1, 0이 되면 게임오버
                
        if Shot:
            drawObject(explosion, a, b) # 보스 폭발
            
            if bosshp == 5: # 보스의 체력에 따라 난이도 조절
                monmissileSpeed = 4
            if bosshp == 2:
                monmissileSpeed = 6
       
       
        if Crash:
            drawObject(explosion, x, y) # 플레이어 폭발
            
            #pygame.mixer.load('explosion01.wav')
        
        drawObject(boss, a, b) # 보스를 (a,b) 에 그림
        drawObject(fighter, x, y) # 비행기를 게임 화면의 (x,y) 좌표에 그림
        
        # 미사일 발사 화면에 그리기 
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY): # 미사일 요소에 대해 반복
                bxy[1] -= 10 # 총알의 y좌표 -10 
                missileXY[i][1] = bxy[1]

                # 공격이 보스를 맞춘 경우
                if bxy[1] < b:
                    if a < bxy[0] < a + bossWidth:
                        missileXY.remove(bxy)
                        
                        Shot = True
                        shotpoint += 100
                        bosshp -= 1
        
                if bxy[1] <= 0: # 미사일이 화면 밖으로 나가면
                    try:
                        missileXY.remove(bxy) # 미사일 제거
                    except:
                        pass
        
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile,bx,by)
        
        Score(shotpoint) # 점수 표시 
        Life(life) # 목숨 표시
        BossHp(bosshp) # 보스 체력 표시
        Missilecount(missile_count) # 남은 미사일 표시
        Time(delta_time) # 남은 시간 표시
        if bosshp == 0:
            Gameclear()

        if life == 0 or delta_time == 0:
            pygame.mixer.music.stop()
            gameOverSound.play()
            onGame = True
            Gameover()

        monmissileY += monmissileSpeed # 적 공격 아래로

        # 공격이 떨어진 경우
        
        if monmissileY > padHeight:
            monmissileSize = monmissile.get_rect().size
            monmissileWidth = monmissileSize[0]
            monmissileHeight = monmissileSize[1]
            monmissileX = random.randrange(0, padWidth - monmissileWidth)
            monmissileY = 0
         
        drawObject(monmissile, monmissileX, monmissileY) #적의 공격 그리기
        
        pygame.display.update() # 화면을 다시 그림
        clock.tick(60) # 게임 화면의 초당 프레임수를 60으로 설정

    pygame.quit()

initGame()
runGame()
