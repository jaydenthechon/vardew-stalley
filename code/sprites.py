import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, z=LAYERS['main']):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy()

class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        
        # Create simple tree visual
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE * 2))
        self.image.set_colorkey((0, 0, 0))
        
        # Tree trunk
        pygame.draw.rect(self.image, (101, 67, 33), (TILE_SIZE // 2 - 8, TILE_SIZE, 16, TILE_SIZE))
        
        # Tree foliage (circles)
        pygame.draw.circle(self.image, (34, 139, 34), (TILE_SIZE // 2, TILE_SIZE - 10), 25)
        pygame.draw.circle(self.image, (50, 205, 50), (TILE_SIZE // 2 - 15, TILE_SIZE - 20), 20)
        pygame.draw.circle(self.image, (50, 205, 50), (TILE_SIZE // 2 + 15, TILE_SIZE - 20), 20)
        
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-40, -TILE_SIZE)
        self.z = LAYERS['main']
        
        self.health = 3
        self.alive = True
        
    def damage(self):
        self.health -= 1
        # Flash red when hit
        temp_surface = self.image.copy()
        temp_surface.fill((255, 0, 0, 50), special_flags=pygame.BLEND_RGB_ADD)
        
        if self.health <= 0:
            self.alive = False
            self.kill()
            return True  # Tree is chopped down
        return False

class Rock(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        
        # Create simple rock visual
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey((0, 0, 0))
        
        # Draw rock
        pygame.draw.ellipse(self.image, (128, 128, 128), (5, 20, 50, 40))
        pygame.draw.ellipse(self.image, (169, 169, 169), (10, 25, 40, 30))
        
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        self.z = LAYERS['main']

class Fence(pygame.sprite.Sprite):
    def __init__(self, pos, group, horizontal=True):
        super().__init__(group)
        
        if horizontal:
            self.image = pygame.Surface((TILE_SIZE, 20))
            self.image.fill((139, 90, 43))
        else:
            self.image = pygame.Surface((20, TILE_SIZE))
            self.image.fill((139, 90, 43))
            
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        self.z = LAYERS['main']
