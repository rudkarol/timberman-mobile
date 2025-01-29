import pygame
import random
from enum import Enum

import connection


pygame.init()
pygame.mixer.init()

WINDOW_WIDTH = 440
WINDOW_HEIGHT = 956
SCREEN_MIDDLE = WINDOW_WIDTH // 2
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

START_BUTTON_WIDTH = 200
START_BUTTON_HEIGHT = 50
START_BUTTON_X = (WINDOW_WIDTH - START_BUTTON_WIDTH) // 2
START_BUTTON_Y = 400


class Position(Enum):
    LEFT = 0
    RIGHT = 1


class TreeSegment(Enum):
    EMPTY = 0
    LEFT_BRANCH = 1
    RIGHT_BRANCH = 2
    ANIMAL = 3


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
        self.owl = pygame.image.load("assets/textures/owl.png")
        self.player = pygame.image.load("assets/textures/player.png")
        self.player_chopping = pygame.image.load("assets/textures/player1.png")

        # Load font
        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 30)
        self.small_font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 20)

        # Load sounds
        self.chop_sound = pygame.mixer.Sound("assets/sounds/chop.wav")
        self.death_sound = pygame.mixer.Sound("assets/sounds/death.wav")
        self.out_of_time_sound = pygame.mixer.Sound("assets/sounds/out_of_time.wav")

        self.reset_game()

        self.nickname = ""
        self.nickname_active = True

        self.show_record_text = False

        self.start_button_rect = pygame.Rect(
            START_BUTTON_X,
            START_BUTTON_Y,
            START_BUTTON_WIDTH,
            START_BUTTON_HEIGHT
        )

        self.nickname_start_button = pygame.Rect(
            (WINDOW_WIDTH - START_BUTTON_WIDTH) // 2,
            WINDOW_HEIGHT // 3 + 60,
            START_BUTTON_WIDTH,
            START_BUTTON_HEIGHT
        )

        self.rescue_button = pygame.Rect(
            WINDOW_WIDTH // 2 - 75,
            WINDOW_HEIGHT - 100,
            150,
            50
        )

    def reset_game(self):
        self.tree = [TreeSegment.EMPTY, TreeSegment.EMPTY]

        for _ in range(5):
            self.tree.append(self.generate_segment())

        self.player_position = Position.RIGHT
        self.points = 0
        self.game_running = False
        self.player_chopping_animation = False
        self.animation_timer = 0
        self.game_over_sound_played = False
        self.show_rescue_button = False
        self.animal_rescued = False

        # Time
        self.remaining_time = INITIAL_TIME
        self.last_update = pygame.time.get_ticks()

        self.show_record_text = False

    def generate_segment(self):
        # 51% empty, 24% left branch, 24% right branch, 1% animal
        return random.choices(
            [TreeSegment.EMPTY, TreeSegment.LEFT_BRANCH, TreeSegment.RIGHT_BRANCH, TreeSegment.ANIMAL],
            weights=[51, 24, 24, 1])[0]

    def handle_mouse_click(self, pos):
        if self.nickname_active:
            if len(self.nickname) > 0 and self.nickname_start_button.collidepoint(pos):
                self.nickname_active = False
            return

        if not self.game_running:
            if self.start_button_rect.collidepoint(pos):
                self.reset_game()
                self.game_running = True
                return

        if self.game_running:
            if self.show_rescue_button and self.rescue_button.collidepoint(pos):
                self.rescue_animal()
                return

            x, y = pos

            if x < SCREEN_MIDDLE:
                self.player_position = Position.LEFT
            else:
                self.player_position = Position.RIGHT

            self.player_chopping_animation = True
            self.animation_timer = pygame.time.get_ticks()
            self.cut_tree()

    def rescue_animal(self):
        self.animal_rescued = True
        self.show_rescue_button = False
        self.points += 5

    def cut_tree(self):
        current_segment = self.tree[1]

        if current_segment == TreeSegment.ANIMAL and not self.animal_rescued:
            self.points = max(0, self.points - 10)

        self.tree.pop(0)
        self.tree.append(self.generate_segment())

        self.animal_rescued = False

        # Player collision with branch
        if ((current_segment == TreeSegment.LEFT_BRANCH and self.player_position == Position.LEFT) or
                (current_segment == TreeSegment.RIGHT_BRANCH and self.player_position == Position.RIGHT)):
            self.game_running = False
            self.death_sound.play()

            try:
                user_data = connection.get_user_max_scores(self.nickname)
                if not user_data.items:
                    connection.create_user(self.nickname, self.points)
                else:
                    if self.points > user_data.items[0].score:
                        self.show_record_text = True
                        connection.update_user_max_scores(user_data.items[0].id, self.points)
            except Exception as e:
                print(e)

            return

        self.chop_sound.play()
        self.points += 1

        # Add time bonus
        time_reduction = (self.points // 10) * TIME_ACCELERATION
        bonus = max(MIN_TIME_BONUS, TIME_BONUS - time_reduction)
        self.remaining_time = min(self.remaining_time + bonus, MAX_TIME)

        if self.tree[1] == TreeSegment.ANIMAL:
            self.show_rescue_button = True
        else:
            self.show_rescue_button = False

    def draw_start_button(self):
        pygame.draw.rect(self.window, WHITE, self.start_button_rect)
        pygame.draw.rect(self.window, BLACK, self.start_button_rect, 2)

        button_text = self.font.render("START", True, BLACK)
        text_rect = button_text.get_rect(center=self.start_button_rect.center)
        self.window.blit(button_text, text_rect)

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
            pygame.draw.rect(self.window, WHITE, self.nickname_start_button)
            pygame.draw.rect(self.window, BLACK, self.nickname_start_button, 2)

            start_text = self.font.render("START", True, BLACK)
            start_text_rect = start_text.get_rect(center=self.nickname_start_button.center)
            self.window.blit(start_text, start_text_rect)

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
            if not self.game_over_sound_played:
                self.out_of_time_sound.play()
                self.game_over_sound_played = True

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
            if segment == TreeSegment.EMPTY:
                tree_sprite = self.tree_empty
            elif segment == TreeSegment.LEFT_BRANCH:
                tree_sprite = self.tree_left
            elif segment == TreeSegment.RIGHT_BRANCH:
                tree_sprite = self.tree_right
            elif segment == TreeSegment.ANIMAL:
                tree_sprite = self.tree_empty

            sprite_rect = tree_sprite.get_rect(center=(220, y_pos))
            self.window.blit(tree_sprite, sprite_rect)

            if segment == TreeSegment.ANIMAL:
                owl_rect = self.owl.get_rect(center=(220, y_pos))
                self.window.blit(self.owl, owl_rect)

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

        # Draw rescue button
        if self.show_rescue_button and self.game_running:
            pygame.draw.rect(self.window, GREEN, self.rescue_button)
            rescue_text = self.small_font.render("RESCUE", True, BLACK)
            text_rect = rescue_text.get_rect(center=self.rescue_button.center)
            self.window.blit(rescue_text, text_rect)

        # Draw start/game over text
        if not self.game_running:
            if self.points == 0:
                start_text = self.font.render("NEW GAME", True, BLACK)
                self.window.blit(start_text, (220 - start_text.get_width() // 2, 300))
                self.draw_start_button()
            else:
                game_over_text = self.font.render("GAME OVER", True, BLACK)
                self.window.blit(game_over_text, (220 - game_over_text.get_width() // 2, 300))
                self.draw_start_button()

                if self.show_record_text:
                    record_text = self.font.render("NEW RECORD!", True, BLACK)
                    self.window.blit(record_text, (220 - record_text.get_width() // 2, 500))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click(event.pos)

                if event.type == pygame.KEYDOWN:
                    if self.nickname_active:
                        if event.key == pygame.K_BACKSPACE:
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