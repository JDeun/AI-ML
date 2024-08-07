import pygame
import os

#게임 스크린 크기
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#색 정의 : 전역변수
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

#print(type(BLUE))  - tuple

pygame.init()  # pygame 초기화

pygame.display.set_caption("Keyboard")  # 윈도우 제목

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock() # 게임화면 업데이트 속도

keyboard_image = pygame.image.load('keyboard.png')
keyboard_x = int(SCREEN_WIDTH / 2)
keyboard_y = int(SCREEN_HEIGHT / 2)
keyboard_dx = 0
keyboard_dy = 0

done = False # 게임이 진행 중인지 확인하는 변수

#게임반복 구간
while not done:
    for event in pygame.event.get(): # 이벤트 반복구간
        if event.type == pygame.QUIT :  # QUIT는 윈도우 창을 닫을 때 발생하는 이벤트
            done = True
        
        # 키가 눌릴 경우
        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT :
                keyboard_dx = -3
            elif event.key == pygame.K_RIGHT :
                keyboard_dx = 3
            elif event.key == pygame.K_UP :
                keyboard_dy = -3
            elif event.key == pygame.K_DOWN :
                keyboard_dy = 3

        elif event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                keyboard_dx = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN :
                keyboard_dy = 0
                
# 게임 로직 구간
# 키보드 위치 변경
    keyboard_x += keyboard_dx
    keyboard_y += keyboard_dy
# 화면 삭제 구간

# 스크린 채우기
    screen.fill(GRAY)

# 화면 그리기 구간
    screen.blit(keyboard_image, [keyboard_x, keyboard_y])

# 화면 업데이트
    pygame.display.flip()

    clock.tick(60)

pygame.quit()