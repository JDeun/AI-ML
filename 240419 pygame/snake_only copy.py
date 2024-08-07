import pygame
import os
import sys
import random
from time import sleep
import time

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
        self.speed_multiplier = 1  # 추가된 부분: 뱀의 이동 속도를 조절하기 위한 변수
    
    # xy는 UP, DOWN, LEFT, RIGHT의 튜플. 새로운 뱀의 이동방향 설정 
    def control(self, xy) :
        if(xy[0] * -1, xy[1] * -1) == self.direction :      # 현재 방향의 반대의 키가 눌려졌다면 return으로 무시 
            return
        else :
            self.direction = xy     # 현재 방향의 반대가 아니라면 새 방향값 설정

    # 뱀이 한 칸 이동시 처리
    def move(self, orange, bonus_oranges):  # 추가된 부분: 보너스 오렌지도 뱀이 먹을 수 있도록 인자 추가
        cur = self.positions[0]  # 현재 (x, y) 화면 좌표 가져옴
        x, y = self.direction  # (a, b) 튜플
        new = (cur[0] + (x * GRID_SIZE), cur[1] + (y * GRID_SIZE))  # new = (x, y) cur기준으로 새 좌표 설정

        if new in self.positions[1:]:  # 머리가 몸에 부딪혔을 때
            sleep(3)
            self.create()  # 새 게임 시작
            orange.game_over_reset()  # 게임 오버 시 오렌지 위치 재설정
        
        elif new[0] < 0 or new[0] >= SCREEN_WIDTH or \
                new[1] < 0 or new[1] >= SCREEN_HEIGHT:
            sleep(3)
            self.create()
            orange.game_over_reset()  # 게임 오버 시 오렌지 위치 재설정
        
        else:  # 현재 상태로 이동.
            self.positions.insert(0, new)  # 바뀐 머리 위치에 새 데이터 추가
            if len(self.positions) > self.length:  # 일반적인 경우 - 이동.
                if self.positions[0] != orange.position:  # 먹이를 먹지 않았을 때
                    self.positions.pop()  # 마지막 데이터(꼬리)를 삭제
                else:  # 먹이를 먹었을 때
                    orange.reset()  # 먹이를 먹었다는 처리
                    self.length += 1  # 뱀의 길이를 1 증가시킴
                    self.speed_multiplier += 0.1  # 기존 오렌지를 먹으면 이동 속도 증가

                # 추가된 부분: 보너스 오렌지 먹기
                for bonus_orange in bonus_oranges:
                    if self.positions[0] == bonus_orange:
                        self.length += 1
                        bonus_oranges.remove(bonus_orange)
                        self.speed_multiplier += 0.1  # 보너스 오렌지를 먹으면 이동 속도 증가
                        break  # 한 번에 한 개의 보너스 오렌지만 먹을 수 있음

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

class Orange:
    def __init__(self):
        self.reset()

    def reset(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, screen):
        if self.position:
            color = ORANGE
            rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, color, rect)

    def eaten(self, snake):
        if self.position == snake.positions[0]:
            self.reset()

    def game_over_reset(self):
        self.reset()


# Game을 총괄하는 클래스 
class Game:
    def __init__(self):
        self.snake = Snake()
        self.orange = Orange()
        self.bonus_oranges = []  # 추가된 부분: 보너스 오렌지 리스트
        self.bonus_orange_timer = 0  # 추가된 부분: 보너스 오렌지 타이머
        self.speed = 5
        self.bonus_orange_created = False  # 추가된 부분: 보너스 오렌지가 생성되었는지 여부
        self.game_over = False  # 게임 오버 여부를 나타내는 변수 추가

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.control(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.control(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.control(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.control(RIGHT)
                elif event.key == pygame.K_b and not self.bonus_orange_created:  # 추가된 부분: 보너스 오렌지 생성 여부 확인
                    self.create_bonus_oranges()  # 보너스 오렌지 생성

        return False
    
    # 추가된 부분: 보너스 오렌지 생성
    def create_bonus_oranges(self):
        for _ in range(20):
            position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            self.bonus_oranges.append(position)
        self.bonus_orange_timer = time.time()
        self.bonus_orange_created = True  # 보너스 오렌지가 생성되었음을 표시

    # 뱀이 한칸 움직이는 것 구현. 이동, 먹었는지 체크, 속도 변화
    def run_logic(self):
        self.snake.move(self.orange, self.bonus_oranges)  # 추가된 부분: 보너스 오렌지도 인자로 전달

        # 추가된 부분: 보너스 오렌지 타이머 확인 및 보너스 오렌지 제거
        if time.time() - self.bonus_orange_timer > 10:
            self.bonus_oranges = []
            self.bonus_orange_timer = 0
            self.bonus_orange_created = False  # 보너스 오렌지가 모두 사라졌으므로 다시 생성 가능 상태로 변경

        # 추가된 부분: 뱀의 이동 속도 조절
        self.speed = 5 * self.snake.speed_multiplier
    
    # 화면에 필요한 텍스트 정보를 출력
    def draw_info(self, length, speed, screen) :
        info = 'Length: ' + str(length) + "  " + "Speed: " + str(round(speed, 2))
        font = pygame.font.SysFont('FixedSys', 30, False, False)
        text_obj = font.render(info, True, GRAY)
        text_rect = text_obj.get_rect()
        text_rect.x, text_rect.y = 10, 10
        screen.blit(text_obj, text_rect)

        # 추가된 부분: 보너스 오렌지 시간 표시
        if self.bonus_orange_created:
            remaining_time = max(0, 10 - (time.time() - self.bonus_orange_timer))
            time_text = 'Bonus Orange Time: ' + str(round(remaining_time, 1))
            time_obj = font.render(time_text, True, GRAY)
            time_rect = time_obj.get_rect()
            time_rect.x, time_rect.y = 10, 50
            screen.blit(time_obj, time_rect)

    # 전체 화면을 그리는 함수. 뱀 정보 출력
    def display_frame(self, screen):
        screen.fill(WHITE)
        self.draw_info(self.snake.length, self.speed, screen)
        self.snake.draw(screen)
        self.orange.draw(screen)  # 오렌지 그리기

        # 추가된 부분: 보너스 오렌지 그리기
        for position in self.bonus_oranges:
            color = RED
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, color, rect)

        pygame.display.flip()  # 화면 전체 업데이트 신호

    def game_over_reset(self):
        self.orange.game_over_reset()

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

