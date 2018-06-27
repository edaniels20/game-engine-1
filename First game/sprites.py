import pygame as pg
from settings import *

import pygame as pg
from settings import *

from enum import Enum

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.fire_direction = Direction.right

    def move(self, direction):
        self.fire_direction = direction

        dx = 0
        dy = 0

        if direction == Direction.left:
            dx = -1
        elif direction == Direction.right:
            dx = 1
        elif direction == Direction.up:
            dy = -1
        else:
            dy = 1

        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.direction = Direction.right

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Direction(Enum):
    down = 0
    left = 1
    up = 2
    right = 3

class Projectile(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.bullet_img
        self.image = pg.Surface((TILESIZE // 2, TILESIZE // 2))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.rect.center = self.pos
        self.dir = dir
        self.spawn_time = pg.time.get_ticks()

    def update(self):

        if self.dir == Direction.up:
            self.rect.y -= TILESIZE // 3
        if self.dir == Direction.down:
            self.rect.y += TILESIZE // 3
        if self.dir == Direction.left:
            self.rect.x -= TILESIZE // 3
        if self.dir == Direction.right:
            self.rect.x += TILESIZE // 3
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > ARROW_TIME:
            self.kill()