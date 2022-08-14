import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    
Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 40
SPEED = 20

WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)


def percentof(number, percent):
    return number * percent // 100

class GameAI:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.floor_level = percentof(self.h, 55)
        # init display
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Capture the flag')
        self.clock = pygame.time.Clock()
        # MC = main character
        self.MC = Point(random.randint(0, (self.w - BLOCK_SIZE ) // BLOCK_SIZE ) * BLOCK_SIZE, self.floor_level)
        self.score = 0
        self.flag = None
        self._place_flag()

    def _place_flag(self):
        if self.MC.x > self.w / 2:
            self.flag = Point(random.randint(0, (self.w / 2 - BLOCK_SIZE ) // BLOCK_SIZE ) * BLOCK_SIZE, self.floor_level)
        else:
            self.flag = Point(self.w - (random.randint(1, (self.w / 2 - BLOCK_SIZE ) // BLOCK_SIZE ) * BLOCK_SIZE), self.floor_level)

    def play_step(self, action):
        # 1. collect user input
        prev_distance = self.MC.x - self.flag.x
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Final Score', self.score)
                pygame.quit()
                quit()
        self._move(action)
        new_distance = self.MC.x - self.flag.x
        # 3. check if game over
        game_over = False
        if self.score >= 1000:
            game_over = True
            if abs(new_distance) < abs(prev_distance):
                reward = 10
            elif abs(new_distance) > abs(prev_distance):
                reward = -10
            
            return reward, game_over, self.score
            
        # 4. place new food or just move
        if self.MC == self.flag:
            self.score += 1
            self._place_flag()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        if abs(new_distance) < abs(prev_distance):
            reward = 10
        elif abs(new_distance) > abs(prev_distance):
            reward = -10

        return reward, game_over, self.score
        
    def _update_ui(self):
        self.display.fill(GREEN)
        self.display.fill(BLACK, (0, 0, self.w, percentof(self.h, 55) + BLOCK_SIZE))
        pygame.draw.rect(self.display, BLUE, pygame.Rect(self.MC.x, self.MC.y, BLOCK_SIZE, BLOCK_SIZE))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.flag.x, self.flag.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        
        if np.array_equal(action, [1, 0]):
            new_dir = Direction.RIGHT
        else: # [0, 1]
            new_dir = Direction.LEFT

        self.direction = new_dir
        
        x = self.MC.x
        y = self.MC.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
            
        self.MC = Point(x, y)