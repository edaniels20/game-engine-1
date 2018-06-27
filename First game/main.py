import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'map.txt')) 
        # self.bullet_img = pg.image.load_rect(10, 10)
        ''' This loads the map text file
        cannot put a note in map text file because it will mess up the size of the map
        because it will add another text line
        '''

    def new(self): #This is all the things nat need to happen at the start
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height) #This is the scrolling camera

    def run(self): #This is the primary game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self): #This is the section that processes all of the inputs
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self): #This function takes your input such as movement
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.player.move(Direction.left)
                    # self.player.move(dx=-1)
                    
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.player.move(Direction.right)
                    # self.player.move(dx=1) 
                    
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.player.move(Direction.up)
                    # self.player.move(dy=-1)
                    
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    # self.player.move(dy=1)
                    self.player.move(Direction.down)

                if event.key == pg.K_SPACE:
                    Projectile(self, self.player.rect.center, self.player.fire_direction)
                    
                    
                    

    

    def show_start_screen(self): #This will be the start screen
        pass

    def show_go_screen(self): #This will be the game over screen
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()