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

pygame.display.set_caption("pygame")  # 윈도우 제목

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock() # 게임화면 업데이트 속도

done = False # 게임이 진행 중인지 확인하는 변수

#게임반복 구간
while not done:
    for event in pygame.event.get(): # 이벤트 반복구간
        if event.type == pygame.QUIT :  # QUIT는 윈도우 창을 닫을 때 발생하는 이벤트
            done = True

# 게임 로직 구간

# 화면 삭제 구간

# 스크린 채우기
    screen.fill(WHITE)

# 화면 그리기 구간
    pygame.draw.line(screen, RED, [50, 50], [500, 50], 10)
    pygame.draw.line(screen, GREEN, [50, 100], [500, 100], 10)
    pygame.draw.line(screen, BLUE, [50, 150], [500, 150], 10)

    pygame.draw.rect(screen, RED, [50, 200, 150, 150], 4)
    pygame.draw.polygon(screen, GREEN, [[350, 200], [250, 350], [450, 350]], 4)
    pygame.draw.circle(screen, BLUE, [150, 450], 60, 4)
    pygame.draw.ellipse(screen, BLUE, [250, 400, 200, 100], 0)

    font = pygame.font.SysFont('FixedSys', 40, True, False)  # 폰트명, 크기, 두껍게, 이탤릭

    text = font.render("Hello Pygame", True, BLACK)  #텍스트, 안티알리아스 여부, 색상, 배경색
    screen.blit(text, [200, 550])



# 화면 업데이트
    pygame.display.flip()

    clock.tick(60)

pygame.quit()