import pygame
import os
import sys
import random
from time import sleep

# game screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 전역변수
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

# 방향정보 : 좌측상단이 (0, 0)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 색 정보
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
ORANGE = (250, 150, 0)


class Snake() :
    def __init__(self) :
        self.create()
    
    # 최초 뱀의 길이, 위치 및 방향 설정
    def create(self) :
        self.length = 2
        self.positions = [(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))]  #좌표 리스트 (x,y) 튜플을 가진 리스트
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
    
    # xy는 UP, DOWN, LEFT, RIGHT의 튜플. 새로운 뱀의 이동방향 설정 
    def control(self, xy) :
        if(xy[0] * -1, xy[1] * -1) == self.direction :      # 현재 방향의 반대의 키가 눌려졌다면 return으로 무시 
            return
        else :
            self.direction = xy     # 현재 방향의 반대가 아니라면 새 방향값 설정

    # 뱀이 한 칸 이동시 처리
    def move(self) :
        cur = self.positions[0]     # 현재 (x, y) 화면 좌표 가져옴
        x, y = self.direction       # (a, b) 튜플
        new = (cur[0] + (x * GRID_SIZE)), (cur[1] + (y * GRID_SIZE))    # new = (x, y) cur기준으로 새 좌표 설정

        if new in self.positions[2:] :      # 머리가 몸에 부딪혔을 때
            sleep(3)
            self.create()                   # 새 게임 시작
        
        # 머리가 테두리에 닿았을 때
        elif new[0] < 0 or new[0] >= SCREEN_WIDTH or \
             new[1] < 0 or new[1] >= SCREEN_HEIGHT :
            sleep(3)
            self.create()
        
        else :  # 현재 상태로 이동. 
            self.positions.insert(0, new)       # 바뀐 머리 위치에 새 데이터 추가
            # 일반적인 경우는 len(self.position)과 self.length가 같다. 
            # 바로 위에서 길이가 늘어났으므로 self.position이 긴 것이 일반적
            # 먹이를 먹으면(position길이와 length 길이가 같아짐) 길이가 늘어나야 하므로 pop() 안함 
            if len(self.positions) > self.length :      # 일반적인 경우 - 이동.
                self.positions.pop()        # 마지막 데이터를 삭제

    # 뱀을 화면에 그린다 
    def draw(self, screen) :
        red = 50 / (self.length -1)     # 뱀의 길이에 따라 Red 색 변경
        green = 150                     # 초록색 고정  
        blue = 150 / (self.length -1)   # 뱀의 길이에 따리 Blue 색 변경

        #enumerate() 함수는 기본적으로 인덱스와 원소로 이루어진 tuple을 만들어줍니다.
        
        for i, p in enumerate(self.positions) :
            color = (100 + red * i, green, blue * i)  # RGB 색 조합, 길이에 따라 조금씩 색이 변한다
            rect = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE)) # 4각형 정의
            pygame.draw.rect(screen, color, rect) 

# Game을 총괄하는 클래스 
class Game() :

    # 뱀 생성, 초기속도 설정
    def __init__(self) :
        self.snake = Snake()    # 뱀 생성
        self.speed = 5          # 초기속도 설정

    # 키보드 입력 처리
    def process_events(self) :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                return True
            
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_UP :
                    self.snake.control(UP)          # 새 방향값 적용
                elif event.key == pygame.K_DOWN :
                    self.snake.control(DOWN)        # 새 방향값 적용
                elif event.key == pygame.K_LEFT :
                    self.snake.control(LEFT)        # 새 방향값 적용
                elif event.key == pygame.K_RIGHT :
                    self.snake.control(RIGHT)       # 새 방향값 적용
        return False
    
    # 뱀이 한칸 움직이는 것 구현. 이동, 먹었는지 체크, 속도 변화
    def run_logic(self) :
        self.snake.move()
        self.speed = (10 + self.snake.length) / 2
    
    # 화면에 필요한 텍스트 정보를 출력
    def draw_info(self, length, speed, screen) :
        info = 'Length: ' + str(length) + "  " + "Speed: " + str(round(speed, 2))
        font = pygame.font.SysFont('FixedSys', 30, False, False)
        text_obj = font.render(info, True, GRAY)
        text_rect = text_obj.get_rect()
        text_rect.x, text_rect.y = 10, 10
        screen.blit(text_obj, text_rect)

    # 전체 화면을 그리는 함수. 뱀 정보 출력
    def display_frame(self, screen) :
        screen.fill(WHITE)
        self.draw_info(self.snake.length, self.speed, screen)
        self.snake.draw(screen)
        screen.blit(screen, (0,0))       # rect 부문만 업데이트 

# 프로그램 시작점
def main() :
    pygame.init()
    pygame.display.set_caption("Snake Game")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()     # 시계 생성
    game = Game()                   # Game 객체 생성
    
    done = False
    while not done :
        done = game.process_events()        # 키보드 입력이 있으면 키보드 입력처리
        game.run_logic()                    # 뱀이 한 칸 이동
        game.display_frame(screen)          # 전체 화면 출력
        pygame.display.flip()               # 화면 전체 업데이트 신호
        clock.tick(game.speed)              # frame 속도를 변화시킴. game.speed가 커지면 더 빨라짐
    
    pygame.quit()

main()
