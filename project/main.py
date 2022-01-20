from settings import *
from load_map import *
from os import path,listdir
import pygame , sys

pygame.init()
pygame.display.set_caption("battle tanks")
font = pygame.font.Font(None, 36)

class game():
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 640
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_name = pygame.font.match_font('arial')
        self.cur_map = 0
        self.running = False

    def play(self):
        loading_maps(path.join(files_dir , "map_1"))
        self.running = True
        
        while self.running:
            self.clock.tick(30) #FPS
            
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    sys.exit()
            
            for bad_bullet in bad_bullets_group:                 
                hit_the_good_guys = pygame.sprite.spritecollide(bad_bullet,players,False)
                if len(hit_the_good_guys) and pygame.time.get_ticks() - bad_bullet.appear > 100:
                    bad_bullet.kill()
                    for player in hit_the_good_guys:
                        player.get_shot()
                        boom = pygame.mixer.Sound(path.join(files_dir,"resources_musics_boom.mp3"))
                        boom.set_volume(0.2)
                        boom.play()
            
            for bullet in bullets_group:
                hit_the_blocks = pygame.sprite.spritecollide(bullet,blocks_group,False)
                if(len(hit_the_blocks)):
                    bullet.kill()
                    for obj in hit_the_blocks:
                        obj.get_shot()
                        boom = pygame.mixer.Sound(path.join(files_dir,"resources_musics_boom.mp3"))
                        boom.set_volume(0.2)
                        boom.play()                   
                    
                hit_the_enemies = pygame.sprite.spritecollide(bullet,tanks_group,False)
                if len(hit_the_enemies) and pygame.time.get_ticks() - bullet.appear > 200:
                    bullet.kill()
                    for enemy in hit_the_enemies:
                        enemy.get_shot()
                        boom = pygame.mixer.Sound(path.join(files_dir,"resources_musics_boom.mp3"))
                        boom.set_volume(0.2)
                        boom.play()
                
                hit_the_players = pygame.sprite.spritecollide(bullet,players,False)
                if len(hit_the_players) and pygame.time.get_ticks() - bullet.appear > 200:
                    bullet.kill()
                    for player in hit_the_players:
                        player.get_shot()
                        boom = pygame.mixer.Sound(path.join(files_dir,"resources_musics_boom.mp3"))
                        boom.set_volume(0.2)
                        boom.play()
                        
            self.screen.fill((0, 0, 0))        
            sprites.draw(self.screen)
            sprites.update()
                
            if len(players)<=1: 
                pygame.time.wait(3000)
                self.running = False
                
            pygame.display.flip()
                                              
if __name__ == '__main__':
    tank = game()
    tank.play()