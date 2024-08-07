import pygame
import random
import time

# 게임 화면 크기
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 그리드 크기
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# 방향 정의
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 색깔 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
ORANGE = (250, 150, 0)


class Snake:
    """뱀 클래스"""
    def __init__(self):
        """뱀 초기화"""
        self.create()

    def create(self):
        """뱀 생성"""
        self.length = 2
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.speed_multiplier = 1  # 뱀 이동 속도 조절 변수

    def control(self, direction):
        """뱀 이동 방향 제어"""
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def move(self, orange, bonus_oranges):
        """뱀 이동"""
        head_x, head_y = self.positions[0]
        move_x, move_y = self.direction
        new_head = (head_x + (move_x * GRID_SIZE), head_y + (move_y * GRID_SIZE))

        # 뱀 몸에 부딪히면 게임 재시작
        if new_head in self.positions[1:]:
            time.sleep(3)
            self.create()
            orange.game_over_reset()

        # 화면 경계에 부딪히면 게임 재시작
        elif not (0 <= new_head[0] < SCREEN_WIDTH and 0 <= new_head[1] < SCREEN_HEIGHT):
            time.sleep(3)
            self.create()
            orange.game_over_reset()

        else:
            self.positions.insert(0, new_head)

            # 먹이를 먹었을 때
            if len(self.positions) > self.length:
                if self.positions[0] != orange.position:
                    self.positions.pop()
                else:
                    orange.reset()
                    self.length += 1
                    self.speed_multiplier += 0.1

                # 보너스 오렌지를 먹었을 때
                for bonus_orange in bonus_oranges:
                    if self.positions[0] == bonus_orange:
                        self.length += 1
                        bonus_oranges.remove(bonus_orange)
                        self.speed_multiplier += 0.1
                        break

    def draw(self, screen):
        """뱀 그리기"""
        red = 50 / (self.length - 1)
        green = 150
        blue = 150 / (self.length - 1)

        for i, (x, y) in enumerate(self.positions):
            color = (100 + red * i, green, blue * i)
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, color, rect)


class Orange:
    """오렌지 클래스"""
    def __init__(self):
        """오렌지 초기화"""
        self.reset()

    def reset(self):
        """오렌지 위치 초기화"""
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, screen):
        """오렌지 그리기"""
        color = ORANGE
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)

    def eaten(self, snake):
        """오렌지가 먹혔는지 확인"""
        if self.position == snake.positions[0]:
            self.reset()

    def game_over_reset(self):
        """게임 오버 시 리셋"""
        self.reset()


class BonusOrange:
    """보너스 오렌지 클래스"""
    def __init__(self):
        """보너스 오렌지 초기화"""
        self.reset()

    def reset(self):
        """보너스 오렌지 위치 초기화"""
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, screen):
        """보너스 오렌지 그리기"""
        color = RED
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)


class Game:
    """게임 클래스"""
    def __init__(self):
        """게임 초기화"""
        self.snake = Snake()
        self.orange = Orange()
        self.bonus_oranges = []
        self.bonus_orange_timer = 0
        self.speed = 5
        self.bonus_orange_created = False
        self.game_over = False

    def process_events(self):
        """게임 이벤트 처리"""
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
                elif event.key == pygame.K_b and not self.bonus_orange_created:
                    self.create_bonus_oranges()

        return False

    def create_bonus_oranges(self):
        """보너스 오렌지 생성"""
        for _ in range(20):
            position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            self.bonus_oranges.append(position)
        self.bonus_orange_timer = time.time()
        self.bonus_orange_created = True

    def run_logic(self):
        """게임 로직 실행"""
        self.snake.move(self.orange, self.bonus_oranges)

        if time.time() - self.bonus_orange_timer > 10:
            self.bonus_oranges = []
            self.bonus_orange_timer = 0
            self.bonus_orange_created = False

        self.speed = 5 * self.snake.speed_multiplier

    def draw_info(self, screen):
        """화면에 필요한 정보 출력"""
        info = f'Length: {self.snake.length}  Speed: {round(self.speed, 2)}'
        font = pygame.font.SysFont('FixedSys', 30, False, False)
        text_obj = font.render(info, True, GRAY)
        text_rect = text_obj.get_rect()
        text_rect.x, text_rect.y = 10, 10
        screen.blit(text_obj, text_rect)

        if self.bonus_orange_created:
            remaining_time = max(0, 10 - (time.time() - self.bonus_orange_timer))
            time_text = 'Bonus Orange Time: ' + str(round(remaining_time, 1))
            time_obj = font.render(time_text, True, GRAY)
            time_rect = time_obj.get_rect()
            time_rect.x, time_rect.y = 10, 50
            screen.blit(time_obj, time_rect)

    def display_frame(self, screen):
        """화면 업데이트"""
        screen.fill(WHITE)
        self.draw_info(screen)
        self.snake.draw(screen)
        self.orange.draw(screen)

        for position in self.bonus_oranges:
            color = RED
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, color, rect)

        pygame.display.flip()

    def game_over_reset(self):
        """게임 오버 시 리셋"""
        self.orange.game_over_reset()


def main():
    """메인 함수"""
    pygame.init()
    pygame.display.set_caption("Snake Game")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    done = False
    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        pygame.display.flip()
        clock.tick(game.speed)

    pygame.quit()


if __name__ == "__main__":
    main()