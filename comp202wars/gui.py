import sys, copy, glob
import pygame
import platform
from consts import *
from pygame.locals import *
from collections import defaultdict

DIR_CHAR = '/' if platform.system() == 'Darwin' else '\\'

class GameGUI:
    CELL_SIZE = (100, 100)
    FONT_SIZE = 24
    BACKGROUND_COLOR = (230, 230, 230)
    GRID_LINE_COLOR = (100, 100, 100)
    SCORES_WIDTH = 400
    ANIMATION_FPS = 120
    
    def __init__(self, fps, grid_size):
        self.FPS = fps
        self.GRID_SIZE = grid_size
        self.GRID_WIDTH, self.GRID_HEIGHT = grid_size[0]*self.CELL_SIZE[0], grid_size[1]*self.CELL_SIZE[1]
        self.WIDTH, self.HEIGHT = self.GRID_WIDTH + self.SCORES_WIDTH, self.GRID_HEIGHT
        self.SCORE_POS = (self.GRID_WIDTH, self.CELL_SIZE[1]//3)
        self.clock = pygame.time.Clock()
    
    def start(self, num_players):
        pygame.font.init()
        pygame.mixer.init()
        pygame.display.init()
        pygame.display.set_caption('COMP 202 WARS!!!')

        self.load_images()
        self.load_sounds()
        self.font = pygame.font.SysFont('Times New Roman', self.FONT_SIZE)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
    
    def stop(self):
        pygame.quit()
    
    def update_screen(self, state, flip=True, game_over=False, tops=[]):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_grid_lines()
        self.draw_grid_objects(state)
        self.draw_scores(state, game_over=game_over, tops=tops)
        
        if flip:
            pygame.display.flip()
            self.clock.tick(self.FPS)
                
        if not game_over:
            events = pygame.event.get()
        else: # wait for quit event
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN and event.key == K_q:
                        return
                self.clock.tick(self.FPS)
    
    def load_images(self):
        self.images = {}
        self.small_images = {}
        self.icon_images = {}
        for image_file in glob.glob(f".{DIR_CHAR}tiles{DIR_CHAR}*.png"):
            image = pygame.image.load(image_file)
            image = pygame.transform.scale(image, self.CELL_SIZE)
            self.images[image_file] = image
            
            image = pygame.image.load(image_file)
            image = pygame.transform.scale(image, (2*self.CELL_SIZE[0]//3, 2*self.CELL_SIZE[1]//3))
            self.small_images[image_file] = image
            
            image = pygame.image.load(image_file)
            image = pygame.transform.scale(image, (self.FONT_SIZE*2, self.FONT_SIZE*2))
            self.icon_images[image_file] = image
    
    def load_sounds(self):
        self.sounds = {}
        for sound_file in glob.glob(f".{DIR_CHAR}sounds{DIR_CHAR}*.wav"):
            sound = pygame.mixer.Sound(sound_file)
            self.sounds[sound_file] = sound
    
    def play_sound(self, sound):
        self.sounds[f'.{DIR_CHAR}sounds{DIR_CHAR}{sound}.wav'].play()
    
    def draw_grid_lines(self):
        for i in range(0, self.GRID_WIDTH, self.CELL_SIZE[0]):
            pygame.draw.line(self.screen, self.GRID_LINE_COLOR, (0, i), (self.GRID_WIDTH, i), 1)
        for i in range(0, self.GRID_HEIGHT, self.CELL_SIZE[1]):
            pygame.draw.line(self.screen, self.GRID_LINE_COLOR, (i, 0), (i, self.GRID_HEIGHT), 1)
    
    def draw_grid_objects(self, state):
        # draw bots
        positions = [bot.position for bot in state.bots]
        
        pos_cts = defaultdict(int)
        for bot in state.bots:
            i, j = bot.position
            name = bot.get_name()
            img = f'.{DIR_CHAR}tiles{DIR_CHAR}tile_{name}.png'
            image = self.images[img]
            
            x, y = j*self.CELL_SIZE[0], i*self.CELL_SIZE[1]
            overlap = positions.count((i, j))
            if overlap > 1:
                shift = pos_cts[(i, j)]
                x, y = x+shift*(self.CELL_SIZE[0]//3), y+shift*(self.CELL_SIZE[1]//3)
                pos_cts[(i, j)] += 1
                image = self.small_images[img]
            
            self.screen.blit(image, (x, y))
        
        # draw objects
        for i in range(len(state.map)): # row
            for j in range(len(state.map[i])): # column
                item = state.map[i][j]
                if len(item) == 0:
                    continue
                item = item[0]
                if type(item) != GameObject:
                    continue
                img = f'.{DIR_CHAR}tiles{DIR_CHAR}tile_{item.get_name()}.png'
                self.screen.blit(self.images[img], (j*self.CELL_SIZE[1], i*self.CELL_SIZE[0]))

    def draw_scores(self, state, games_won=[], game_over=False, tops=[]):
        pygame.draw.rect(self.screen, (240, 240, 240), pygame.Rect((self.SCORE_POS[0], 0), (self.WIDTH-self.GRID_WIDTH, self.HEIGHT)), border_radius=10)
        
        max_tops = max([bot.category_tops for bot in state.bots])
        bots = state.bots[:]
        bots.sort(key=lambda bot: bot.category_tops, reverse=True)                
        cur_y = self.SCORE_POS[1]
        for i, bot in enumerate(bots):
            text = f"#{i+1}: {bot.collected_objects}             {bot.player.name}"
            rendered_text = self.font.render(text, False, (0, 0, 0))
            self.screen.blit(rendered_text, (self.SCORE_POS[0], cur_y))
            self.screen.blit(self.icon_images[f'.{DIR_CHAR}tiles{DIR_CHAR}tile_{bot.get_name()}.png'], (self.SCORE_POS[0]+130, cur_y-15))
            
            if not game_over:
                for j, (cgameObject, pgameObject) in enumerate(zip(bot.collected_objects, bot.prev_collected_objects)):
                    if cgameObject - pgameObject > 0:
                        # render + to indicate new gameObject collected
                        rendered_text = self.font.render("+", False, (0, 150, 0))
                        self.screen.blit(rendered_text, (self.SCORE_POS[0]+50+(j*5), cur_y+50))
            elif bot.category_tops == max_tops:
                rendered_text = self.font.render(f"Game Over! {bot.player.name} wins!", False, (0, 150, 0))
                self.screen.blit(rendered_text, (self.SCORE_POS[0]+50+(0*5), cur_y+50))
            
            cur_y += self.CELL_SIZE[1]
        
        text = f"Turn: {state.turn}/{DEFAULT_CONFIG['max_turns']}"
        rendered_text = self.font.render(text, False, (0, 0, 0))
        self.screen.blit(rendered_text, (self.SCORE_POS[0], cur_y))
        
        if game_over:
            rendered_text = self.font.render("Press q to quit", False, (0, 0, 0))
            self.screen.blit(rendered_text, (self.SCORE_POS[0]+200, cur_y))