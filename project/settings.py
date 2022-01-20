import pygame
from os import path
import random

files_dir = path.join(path.dirname(__file__), 'assets')

#setting the pygame group for convenience
bullets_group = pygame.sprite.Group()
bad_bullets_group = pygame.sprite.Group()
tanks_group = pygame.sprite.Group()
blocks_group = pygame.sprite.Group()
sprites = pygame.sprite.Group()
players = pygame.sprite.Group()

### base class
class block(pygame.sprite.Sprite):
    def __init__(self):
        #add the object into the groups
        super().__init__(blocks_group,sprites)
        self.image = None
        self.HP = None
        
    def get_shot(self):
        if self.HP is not None:
            self.HP -= 1
            if self.HP <= 0:
                self.kill()
            
###################################################################################  
###  brick && iron are both 32 x 32 
##   simple objects
    
class brick(block):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load(path.join(files_dir,'bricks.png'))
        self.HP = 1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class iron(block):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load(path.join(files_dir,'iron.png'))
        self.HP = None
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        super().__init__(bullets_group,sprites)
        self.image = pygame.image.load(path.join(files_dir,"bullet.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speed = 8
        self.appear = pygame.time.get_ticks()
    
    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

class bad_bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        super().__init__(bad_bullets_group,sprites)
        self.image = pygame.image.load(path.join(files_dir,"bullet.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speed = 6
        self.appear = pygame.time.get_ticks()
    
    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

###################################################################################
### settings of the tanks and players

class tanks(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__(tanks_group,sprites)
        self.image = pygame.image.load(path.join(files_dir,'tank_c.png'))
        self.HP = 1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        
        ### degrees required to turn if the direction is valid
        self.directions = {'left': {'up': 270, 'right': 180, 'down': 90, 'left': 0},
                           'right': {'up': 90, 'right': 0, 'down': 270, 'left': 180},
                           'up': {'up': 0, 'right': 270, 'down': 180, 'left': 90},
                           'down': {'up': 180, 'right': 90, 'down': 0, 'left': 270}}
        self.current_direction = 'up'
        self.next_direction = None
        self.cooldown = 1000
        self.last_shoot = 0
        self.move_cooldown = 400
        self.last_move = 0
        
    def get_shot(self):
        self.HP -= 1
        if self.HP <= 0:
            self.kill()
        
    def check_path_valid(self):
        if self.next_direction=="right":
            next_x = self.rect.x + 32
            next_y = self.rect.y + 0
            now_x = self.rect.x
            now_y = self.rect.y
            self.rect.x ,self.rect.y = next_x,next_y
            collide_list = pygame.sprite.spritecollide(self,blocks_group,False)
            crash_list = pygame.sprite.spritecollide(self,tanks_group,False)
            crash_list_2 = pygame.sprite.spritecollide(self,players,False)
            if len(collide_list) + len(crash_list) + len(crash_list_2) != 1:
                self.rect.x , self.rect.y= now_x , now_y
            else:
                self.image = pygame.transform.rotate(self.image , self.directions[self.next_direction][self.current_direction])
                self.current_direction = self.next_direction
                
        elif self.next_direction=="left":
            next_x = self.rect.x - 32
            next_y = self.rect.y + 0
            now_x = self.rect.x
            now_y = self.rect.y
            self.rect.x ,self.rect.y = next_x,next_y
            collide_list = pygame.sprite.spritecollide(self,blocks_group,False)
            crash_list = pygame.sprite.spritecollide(self,tanks_group,False)
            crash_list_2 = pygame.sprite.spritecollide(self,players,False)
            if len(collide_list) + len(crash_list) + len(crash_list_2) != 1:
                self.rect.x , self.rect.y= now_x , now_y
            else:
                self.image = pygame.transform.rotate(self.image , self.directions[self.next_direction][self.current_direction])
                self.current_direction = self.next_direction
        
        elif self.next_direction=="up":
            next_x = self.rect.x + 0
            next_y = self.rect.y - 32
            now_x = self.rect.x
            now_y = self.rect.y
            self.rect.x ,self.rect.y = next_x,next_y
            collide_list = pygame.sprite.spritecollide(self,blocks_group,False)
            crash_list = pygame.sprite.spritecollide(self,tanks_group,False)
            crash_list_2 = pygame.sprite.spritecollide(self,players,False)
            if len(collide_list) + len(crash_list) + len(crash_list_2) != 1:
                self.rect.x , self.rect.y= now_x , now_y
            else:
                self.image = pygame.transform.rotate(self.image , self.directions[self.next_direction][self.current_direction])
                self.current_direction = self.next_direction   
        
        elif self.next_direction=="down":
            next_x = self.rect.x + 0
            next_y = self.rect.y + 32
            now_x = self.rect.x
            now_y = self.rect.y
            self.rect.x , self.rect.y = next_x,next_y
            collide_list = pygame.sprite.spritecollide(self,blocks_group,False)
            crash_list = pygame.sprite.spritecollide(self,tanks_group,False)
            crash_list_2 = pygame.sprite.spritecollide(self,players,False)
            if len(collide_list) + len(crash_list) + len(crash_list_2) != 1:
                self.rect.x , self.rect.y= now_x , now_y
            else:
                self.image = pygame.transform.rotate(self.image , self.directions[self.next_direction][self.current_direction])
                self.current_direction = self.next_direction  
        
    def update(self):
        now = pygame.time.get_ticks()
        
        if now - self.last_shoot > self.cooldown:
            bad_bullet(self.rect.x+10,self.rect.y+10,self.current_direction)
            self.last_shoot = now
        
        moving = ["up","down","left","right"]
        if now - self.last_move > self.move_cooldown:
            self.next_direction = moving[random.randint(0,3)]
            self.check_path_valid()
            self.last_move = now
        
                
class player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__(players,sprites)
        self.image = pygame.image.load(path.join(files_dir,'tank_p.png'))
        self.HP = 3 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.directions = {'left': {'up': 270, 'right': 180, 'down': 90, 'left': 0},
                           'right': {'up': 90, 'right': 0, 'down': 270, 'left': 180},
                           'up': {'up': 0, 'right': 270, 'down': 180, 'left': 90},
                           'down': {'up': 180, 'right': 90, 'down': 0, 'left': 270}}
        self.current_direction = 'up'
        self.next_direction = None
        self.cooldown = 500
        self.move_cooldown = 64
        self.last_shoot = 0
        self.last_move = 0
        self.control = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
                        'shot': pygame.K_SPACE}
     
    def get_shot(self):
        self.HP -= 1
        if self.HP <= 0:
            self.kill()
      
    def check_path_valid(self):
        if self.next_direction=="right":
            self.image = pygame.transform.rotate(self.image , self.directions[self.next_direction][self.current_direction])
            self.current_direction = self.next_direction
            next_x = self.rect.x + 32
            next_y = self.rect.y + 0
            now_x = self.rect.x
            now_y = self.rect.y
            self.rect.x ,self.rect.y = next_x,next_y
            collide_list = pygame.sprite.spritecollide(self,blocks_group,False)
            crash_list = pygame.sprite.spritecollide(self,tanks_group,False)
            crash_list_2 = pygame.sprite.spritecollide(self,players,False)
            if len(collide_list) + len(crash_list) + len(crash_list_2) != 1:
                self.rect.x , self.rect.y= now_x , now_y
            
               
        elif self.next_direction=="left":
            self.image = pygame.transform.rotate(self.image , self.directions[self.next_direction][self.current_direction])
            self.current_direction = self.next_direction
            next_x = self.rect.x - 32
            next_y = self.rect.y + 0
            now_x = self.rect.x
            now_y = self.rect.y
            self.rect.x ,self.rect.y = next_x,next_y
            collide_list = pygame.sprite.spritecollide(self,blocks_group,False)
            crash_list = pygame.sprite.spritecollide(self,tanks_group,False)
            crash_list_2 = pygame.sprite.spritecollide(self,players,False)
            if len(collide_list) + len(crash_list) + len(crash_list_2) != 1:
                self.rect.x , self.rect.y = now_x , now_y
                
                   
        elif self.next_direction=="up":
            self.image = pygame.transform.rotate(self.image , self.directions[self.next_direction][self.current_direction])
            self.current_direction = self.next_direction
            next_x = self.rect.x + 0
            next_y = self.rect.y - 32
            now_x = self.rect.x
            now_y = self.rect.y
            self.rect.x ,self.rect.y = next_x,next_y
            collide_list = pygame.sprite.spritecollide(self,blocks_group,False)
            crash_list = pygame.sprite.spritecollide(self,tanks_group,False)
            crash_list_2 = pygame.sprite.spritecollide(self,players,False)
            if len(collide_list) + len(crash_list) + len(crash_list_2) != 1:
                self.rect.x , self.rect.y= now_x , now_y
            
                          
        elif self.next_direction=="down":
            self.image = pygame.transform.rotate(self.image , self.directions[self.next_direction][self.current_direction])
            self.current_direction = self.next_direction
            next_x = self.rect.x + 0
            next_y = self.rect.y + 32
            now_x = self.rect.x
            now_y = self.rect.y
            self.rect.x ,self.rect.y = next_x,next_y
            collide_list = pygame.sprite.spritecollide(self,blocks_group,False)
            crash_list = pygame.sprite.spritecollide(self,tanks_group,False)
            crash_list_2 = pygame.sprite.spritecollide(self,players,False)
            if len(collide_list) + len(crash_list) + len(crash_list_2) != 1:
                self.rect.x , self.rect.y= now_x , now_y
            
            
    def update(self):
        now = pygame.time.get_ticks()
        key_state = pygame.key.get_pressed()  #list of boolean values
        
        if now - self.last_move > self.move_cooldown:
            self.last_move = now
            
            if key_state[self.control["left"]]:
                self.next_direction = "left"
                self.check_path_valid()
            
            elif key_state[self.control["right"]]:
                self.next_direction = "right"
                self.check_path_valid()
            
            elif key_state[self.control["up"]]:
                self.next_direction = "up"
                self.check_path_valid()
            
            elif key_state[self.control["down"]]:
                self.next_direction = "down"
                self.check_path_valid()
            
            elif key_state[self.control["shot"]]:
                now = pygame.time.get_ticks()
            
                if now - self.last_shoot > self.cooldown:
                    bullet(self.rect.x+10,self.rect.y+10,self.current_direction)
                    self.last_shoot = now
    
class player_2(player):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.control = {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d,
                                       'shot': pygame.K_q}
    
################################################