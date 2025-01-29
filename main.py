import pygame
import random
from enum import Enum

pygame.init()

WINDOW_WIDTH = 440
WINDOW_HEIGHT = 956
FPS = 60

INITIAL_TIME = 5000  # 5 sec start time
MAX_TIME = 5000  # 5 sec max time
TIME_BONUS = 400  # Time bonus
MIN_TIME_BONUS = 150  # Min time bonus
TIME_ACCELERATION = 30  # Reduce time bonus
TIMER_BAR_HEIGHT = 30
TIMER_BAR_POS_TOP = 30
TIMER_BAR_POS_lEFT = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

MAX_NICKNAME_LENGTH = 9


class Position(Enum):
    LEFT = 0
    RIGHT = 1


class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Timberman")
        self.clock = pygame.time.Clock()

        # Load images
        self.background = pygame.image.load("assets/textures/background.png")
        self.tree_empty = pygame.image.load("assets/textures/tree0.png")
        self.tree_left = pygame.image.load("assets/textures/tree1.png")
        self.tree_right = pygame.image.load("assets/textures/tree2.png")
        self.player = pygame.image.load("assets/textures/player.png")
        self.player_chopping = pygame.image.load("assets/textures/player1.png")

        # Load font
        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 30)
        self.small_font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 20)

        self.reset_game()

        self.nickname = ""
        self.nickname_active = True

    def reset_game(self):
        self.tree = [0, 0]  # Start with two empty segments

        for _ in range(5):
            self.tree.append(self.generate_segment())

        self.player_position = Position.RIGHT
        self.points = 0
        self.game_running = False
        self.player_chopping_animation = False
        self.animation_timer = 0

        # Time
        self.remaining_time = INITIAL_TIME
        self.last_update = pygame.time.get_ticks()

    def generate_segment(self):
        # 50% empty, 25% left branch, 25% right branch
        return random.choices([0, 1, 2], weights=[2, 1, 1])[0]

    def cut_tree(self):
        current_segment = self.tree[1]

        self.tree.pop(0)
        self.tree.append(self.generate_segment())

        # Player collision with branch
        if ((current_segment == 1 and self.player_position == Position.LEFT) or
                (current_segment == 2 and self.player_position == Position.RIGHT)):
            self.game_running = False
            return

        self.points += 1

        # Add time bonus
        time_reduction = (self.points // 10) * TIME_ACCELERATION
        bonus = max(MIN_TIME_BONUS, TIME_BONUS - time_reduction)
        self.remaining_time = min(self.remaining_time + bonus, MAX_TIME)

    def draw_nickname_input(self):
        # Input field
        input_box = pygame.Rect(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 3, WINDOW_WIDTH // 2, 40)
        pygame.draw.rect(self.window, WHITE, input_box)
        pygame.draw.rect(self.window, BLACK, input_box, 2)

        nickname_surface = self.small_font.render(self.nickname, True, BLACK)
        nickname_rect = nickname_surface.get_rect(center=input_box.center)
        self.window.blit(nickname_surface, nickname_rect)

        prompt_text = self.small_font.render("Enter Nickname:", True, BLACK)
        prompt_rect = prompt_text.get_rect(centerx=WINDOW_WIDTH // 2, bottom=input_box.top - 10)
        self.window.blit(prompt_text, prompt_rect)

        if len(self.nickname) > 0:
            enter_text = self.small_font.render("Press Enter to Start", True, BLACK)
            enter_rect = enter_text.get_rect(centerx=WINDOW_WIDTH // 2, top=input_box.bottom + 10)
            self.window.blit(enter_text, enter_rect)

    def update_time(self):
        if not self.game_running:
            return

        current_time = pygame.time.get_ticks()
        dt = current_time - self.last_update
        self.last_update = current_time

        self.remaining_time = max(0, self.remaining_time - dt)
        if self.remaining_time <= 0:
            self.remaining_time = 0
            self.game_running = False

    def draw_timer_bar(self):
        # Black background
        timer_rect = pygame.Rect(
            TIMER_BAR_POS_lEFT,
            TIMER_BAR_POS_TOP - TIMER_BAR_HEIGHT // 2,
            WINDOW_WIDTH // 4,
            TIMER_BAR_HEIGHT
        )
        pygame.draw.rect(self.window, BLACK, timer_rect)

        # Timer bar
        if self.remaining_time > 0:
            fill_width = (self.remaining_time / MAX_TIME) * (WINDOW_WIDTH // 4)
            fill_rect = pygame.Rect(
                TIMER_BAR_POS_lEFT,
                TIMER_BAR_POS_TOP - TIMER_BAR_HEIGHT // 2,
                fill_width,
                TIMER_BAR_HEIGHT
            )

            if self.remaining_time > MAX_TIME * 0.6:
                color = GREEN
            elif self.remaining_time > MAX_TIME * 0.3:
                color = YELLOW
            else:
                color = RED

            pygame.draw.rect(self.window, color, fill_rect)

    def draw(self):
        # Background
        self.window.blit(self.background, (0, 0))

        if self.nickname_active:
            self.draw_nickname_input()
            return

        self.draw_timer_bar()

        # Tree
        y_pos = 810

        for segment in self.tree[:7]:
            tree_sprite = None
            if segment == 0:
                tree_sprite = self.tree_empty
            elif segment == 1:
                tree_sprite = self.tree_left
            else:
                tree_sprite = self.tree_right

            sprite_rect = tree_sprite.get_rect(center=(220, y_pos))
            self.window.blit(tree_sprite, sprite_rect)
            y_pos -= 135

        # Draw player
        player_sprite = self.player_chopping if self.player_chopping_animation else self.player
        player_x = 380 if self.player_position == Position.RIGHT else 60

        # Flip player sprite
        if self.player_position == Position.LEFT:
            player_sprite = pygame.transform.flip(player_sprite, True, False)

        sprite_rect = player_sprite.get_rect(center=(player_x, 810))
        self.window.blit(player_sprite, sprite_rect)

        # Draw score and nickname
        score_text = self.font.render(str(self.points), True, BLACK)
        nickname_text = self.small_font.render(self.nickname, True, BLACK)
        self.window.blit(score_text, (380 - score_text.get_width() // 2, 30 - score_text.get_height() // 2))
        self.window.blit(nickname_text, (220 - nickname_text.get_width() // 2, 30 - nickname_text.get_height() // 2))

        # Draw start/game over text
        if not self.game_running:
            if self.points == 0:
                start_text = self.font.render("START", True, BLACK)
                space_text = self.font.render("Press Space", True, BLACK)
                self.window.blit(start_text, (220 - start_text.get_width() // 2, 300))
                self.window.blit(space_text, (220 - space_text.get_width() // 2, 400))
            else:
                game_over_text = self.font.render("GAME OVER", True, BLACK)
                space_text = self.font.render("Press Space", True, BLACK)
                self.window.blit(game_over_text, (220 - game_over_text.get_width() // 2, 300))
                self.window.blit(space_text, (220 - space_text.get_width() // 2, 400))

    def run(self):
        running = True
        while running:
            # Events handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if self.nickname_active:
                        if event.key == pygame.K_RETURN and len(self.nickname) > 0:
                            self.nickname_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.nickname = self.nickname[:-1]
                        elif len(self.nickname) < MAX_NICKNAME_LENGTH and event.unicode.isalnum():
                            self.nickname += event.unicode
                    elif self.game_running:
                        if event.key in (pygame.K_a, pygame.K_LEFT):
                            self.player_position = Position.LEFT
                            self.player_chopping_animation = True
                            self.animation_timer = pygame.time.get_ticks()
                            self.cut_tree()
                        elif event.key in (pygame.K_d, pygame.K_RIGHT):
                            self.player_position = Position.RIGHT
                            self.player_chopping_animation = True
                            self.animation_timer = pygame.time.get_ticks()
                            self.cut_tree()
                    elif event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.game_running = True

            # Update time
            self.update_time()

            # Update animation
            if self.player_chopping_animation and pygame.time.get_ticks() - self.animation_timer > 40:
                self.player_chopping_animation = False

            # Draw screen
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()