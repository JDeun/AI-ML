import pygame

#게임 스크린 크기
SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 600

#색 정의 : 전역변수
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#print(type(BLUE))  - tuple

pygame.init()  # pygame 초기화

pygame.display.set_caption("Ball3")  # 윈도우 제목

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock() # 시계 생성

# 공 정보 초기화 (위치, 속도, 크기)
ball_x = int(SCREEN_WIDTH / 2)
ball_y = int(SCREEN_HEIGHT / 2)
ball_dx = 10
ball_dy = 10
ball_size = 20

done = False # 게임이 진행 중인지 확인하는 변수

#게임반복 구간
while not done:
    for event in pygame.event.get(): # 이벤트 반복구간
        if event.type == pygame.QUIT :  # QUIT는 윈도우 창을 닫을 때 발생하는 이벤트
            done = True

        
        # 키가 눌릴 경우
        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT :
                ball_dx = -3
            elif event.key == pygame.K_RIGHT :
                ball_dx = 3
            elif event.key == pygame.K_UP :
                ball_dy = -3
            elif event.key == pygame.K_DOWN :
                ball_dy = 3

        elif event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                ball_dx
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN :
                ball_dy

# 게임 로직 구간

# 속도에 따라 원형 위치 변경
    ball_x += ball_dx
    ball_y += ball_dy


# 공이 스크린을 벗어날 경우
    if(ball_x + ball_size > SCREEN_WIDTH) or (ball_x - ball_size) < 0 :
        ball_dx = ball_dx * -1

    if(ball_y + ball_size > SCREEN_HEIGHT) or (ball_y - ball_size) < 0 :
        ball_dy = ball_dy * -1

# 화면 삭제 구간

# 스크린 채우기
    screen.fill(WHITE)

# 화면 그리기 구간

# 공 그리기
    pygame.draw.circle(screen, BLUE, [ball_x, ball_y], ball_size, 0)

# 화면 업데이트
    pygame.display.flip()

    clock.tick(120)

pygame.quit()