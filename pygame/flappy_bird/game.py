import pygame
import random


class Game:
    def __init__(self, bird_img, pip_img, background_img, ground_img):
        self.bird = pygame.image.load(
            bird_img
        ).convert_alpha()  # after loading the image, convert_alpha method makes the image have perpixal transperancy
        self.bird_rect = self.bird.get_rect(
            center=(70, 180)
        )  # gets the rectangular area of the isurface object
        self.pipe = pygame.image.load(
            pip_img
        ).convert_alpha()  # changes the pixel format of the image including perpixel alphas
        self.background = pygame.image.load(background_img).convert_alpha()
        self.ground = pygame.image.load(ground_img).convert_alpha()
        self.ground_position = 0
        self.active = True  # shows the status of the game
        self.gravity = 0.05  # value for the make the bird move down
        self.bird_movement = (
            0  # value for determing whether the bird is flapping or not
        )
        self.rotated_bird = pygame.Surface((0, 0))
        self.pipes = []
        self.pipe_height = [280, 425, 562]
        self.score = 0
        self.font = pygame.font.SysFont(None, 48)
        self.high_score = 0

    def resize_images(self):
        self.bird = pygame.transform.scale(self.bird, (51, 34))
        self.pipe = pygame.transform.scale(self.pipe, (80, 438))
        self.background = pygame.transform.scale(self.background, (470, 720))
        self.ground = pygame.transform.scale(self.ground, (470, 160))

    def show_background(self, screen):
        # This method draws the background image to the screen(surface obj) in the top left corner(0, 0)
        screen.blit(self.background, (0, 0))

    def show_ground(self, screen):
        screen.blit(self.ground, (self.ground_position, 650))
        screen.blit(self.ground, (self.ground_position + 470, 650))

    def move_ground(self):
        self.ground_position -= 1
        if self.ground_position <= -400:
            self.ground_position = 0

    def show_bird(self, screen):
        screen.blit(self.rotated_bird, self.bird_rect)

    def update_bird(self):
        self.bird_movement += self.gravity
        self.rotated_bird = self.rotate_bird()
        self.bird_rect.centery += self.bird_movement

    def rotate_bird(self):
        new_bird = pygame.transform.rotozoom(self.bird, -self.bird_movement * 3, 1)
        return new_bird

    def flap(self):
        self.bird_movement = 0
        self.bird_movement -= 2.5

    def add_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe.get_rect(midtop=(600, random_pipe_pos))
        top_pipe = self.pipe.get_rect(midbottom=(600, random_pipe_pos - 211))
        self.pipes.append(bottom_pipe)
        self.pipes.append(top_pipe)

    def move_pipes(self):
        for pipe in self.pipes:
            pipe.centerx -= 1.75
            if pipe.centerx <= -40:
                self.pipes.remove(pipe)

    def show_pipes(self, screen):
        for pipe in self.pipes:
            if pipe.bottom >= 700:
                screen.blit(self.pipe, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe, False, True)
                screen.blit(flip_pipe, pipe)

    def check_collision(self):
        for pipe in self.pipes:
            if self.bird_rect.colliderect(pipe):
                self.active = False

        if self.bird_rect.top <= -100 or self.bird_rect.bottom >= 650:
            self.active = False

    def update_score(self):
        self.score += 0.01

    def show_score(self, game_state, screen, color):
        score_surface = self.font.render(f"Score: {int(self.score)}", True, color)
        score_rect = score_surface.get_rect(center=(202, 75))
        screen.blit(score_surface, score_rect)

        if game_state == "Game Over":
            restart_text_1 = self.font.render("Press Space Bar", True, color)
            restart_rect_1 = restart_text_1.get_rect(center=(200, 280))
            screen.blit(restart_text_1, restart_rect_1)

            restart_text_2 = self.font.render("to Play Again", True, color)
            restart_rect_2 = restart_text_2.get_rect(center=(200, 340))
            screen.blit(restart_text_2, restart_rect_2)

            high_score_surface = self.font.render(
                f"High Score: {int(self.high_score)}", True, color
            )
            high_score_rect = high_score_surface.get_rect(center=(200, 610))
            screen.blit(high_score_surface, high_score_rect)

    def game_over(self, screen, color):
        self.update_high_score()
        self.show_score("Game Over", screen, color)

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def restart(self):
        self.active = True
        del self.pipes[:]
        self.bird_rect.center = (70, 180)
        self.bird_movement = 0
        self.score = 0
