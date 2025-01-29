import pygame
import random
from enum import Enum


pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1050
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Position(Enum):
    LEFT = 0
    RIGHT = 1


class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Timberman")
        self.clock = pygame.time.Clock()

        # Assets loading
        self.background = pygame.image.load("assets/textures/background.png")
        self.tree_empty = pygame.image.load("assets/textures/tree0.png")
        self.tree_left = pygame.image.load("assets/textures/tree1.png")
        self.tree_right = pygame.image.load("assets/textures/tree2.png")
        self.player = pygame.image.load("assets/textures/player.png")
        self.player_chopping = pygame.image.load("assets/textures/player1.png")
        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 30)

        self.reset_game()

    def reset_game(self):
        self.tree = [0, 0]  # Start with two empty segments

        for _ in range(5):
            self.tree.append(self.generate_segment())

        self.player_position = Position.RIGHT
        self.points = 0
        self.game_running = False
        self.player_chopping_animation = False
        self.animation_timer = 0

    def generate_segment(self):
        # 50% empty, 25% left branch, 25% right branch
        return random.choices([0, 1, 2], weights=[2, 1, 1])[0]

    def cut_tree(self):
        current_segment = self.tree[1]

        # Branch collision
        if ((current_segment == 1 and self.player_position == Position.LEFT) or
                (current_segment == 2 and self.player_position == Position.RIGHT)):
            self.game_running = False
            return

        self.tree.pop(0)
        self.tree.append(self.generate_segment())
        self.points += 1

    def draw(self):
        self.window.blit(self.background, (0, 0))

        # Draw tree
        y_pos = 900

        for segment in self.tree[:7]:
            tree_sprite = None
            if segment == 0:
                tree_sprite = self.tree_empty
            elif segment == 1:
                tree_sprite = self.tree_left
            else:
                tree_sprite = self.tree_right

            sprite_rect = tree_sprite.get_rect(center=(600, y_pos))
            self.window.blit(tree_sprite, sprite_rect)
            y_pos -= 150

        # Draw player
        player_sprite = self.player_chopping if self.player_chopping_animation else self.player
        player_x = 800 if self.player_position == Position.RIGHT else 400

        # Flip player sprite
        if self.player_position == Position.LEFT:
            player_sprite = pygame.transform.flip(player_sprite, True, False)

        sprite_rect = player_sprite.get_rect(center=(player_x, 900))
        self.window.blit(player_sprite, sprite_rect)

        # Draw score
        score_text = self.font.render(f"Points: {self.points}", True, BLACK)
        self.window.blit(score_text, (20, 50))

        # Draw start screen
        if not self.game_running:
            start_text = self.font.render("START", True, BLACK)
            space_text = self.font.render("Space", True, BLACK)
            self.window.blit(start_text, (1000, 50))
            self.window.blit(space_text, (1000, 90))

    def run(self):
        running = True
        while running:
            # Events handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if self.game_running:
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

                elif event.type == pygame.MOUSEBUTTONDOWN and self.game_running:
                    if event.button == 1:  # Left click
                        self.player_position = Position.LEFT
                        self.player_chopping_animation = True
                        self.animation_timer = pygame.time.get_ticks()
                        self.cut_tree()
                    elif event.button == 3:  # Right click
                        self.player_position = Position.RIGHT
                        self.player_chopping_animation = True
                        self.animation_timer = pygame.time.get_ticks()
                        self.cut_tree()

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