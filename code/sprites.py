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
        
        # Create simple tree visual - larger and more visible
        self.image = pygame.Surface((TILE_SIZE * 1.5, TILE_SIZE * 2.5))
        self.image.set_colorkey((0, 0, 0))
        
        # Tree trunk - brown and wider
        trunk_width = 20
        trunk_x = int(TILE_SIZE * 0.75 - trunk_width // 2)
        pygame.draw.rect(self.image, (101, 67, 33), (trunk_x, int(TILE_SIZE * 1.2), trunk_width, int(TILE_SIZE * 1.3)))
        
        # Tree foliage (circles) - bigger and darker green
        center_x = int(TILE_SIZE * 0.75)
        pygame.draw.circle(self.image, (34, 139, 34), (center_x, int(TILE_SIZE * 0.8)), 30)
        pygame.draw.circle(self.image, (20, 100, 20), (center_x - 20, int(TILE_SIZE * 0.6)), 25)
        pygame.draw.circle(self.image, (20, 100, 20), (center_x + 20, int(TILE_SIZE * 0.6)), 25)
        pygame.draw.circle(self.image, (40, 150, 40), (center_x, int(TILE_SIZE * 0.4)), 22)
        
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-40, -int(TILE_SIZE * 1.5))
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
        
        # Create simple rock visual - bigger
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey((0, 0, 0))
        
        # Draw rock with shading
        pygame.draw.ellipse(self.image, (100, 100, 100), (8, 25, 48, 35))
        pygame.draw.ellipse(self.image, (140, 140, 140), (12, 28, 40, 28))
        pygame.draw.ellipse(self.image, (180, 180, 180), (18, 32, 28, 20))
        
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        self.z = LAYERS['main']

class Fence(pygame.sprite.Sprite):
    def __init__(self, pos, group, horizontal=True):
        super().__init__(group)
        
        if horizontal:
            self.image = pygame.Surface((TILE_SIZE, 24))
            self.image.set_colorkey((0, 0, 0))
            # Draw horizontal fence posts
            pygame.draw.rect(self.image, (101, 67, 33), (0, 0, TILE_SIZE, 24))
            pygame.draw.rect(self.image, (139, 90, 43), (4, 4, TILE_SIZE - 8, 16))
        else:
            self.image = pygame.Surface((24, TILE_SIZE))
            self.image.set_colorkey((0, 0, 0))
            # Draw vertical fence posts
            pygame.draw.rect(self.image, (101, 67, 33), (0, 0, 24, TILE_SIZE))
            pygame.draw.rect(self.image, (139, 90, 43), (4, 4, 16, TILE_SIZE - 8))
            
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        self.z = LAYERS['main']