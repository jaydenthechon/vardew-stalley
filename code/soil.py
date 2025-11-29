import pygame
from settings import *
from random import choice

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((101, 67, 33))  # Dark brown soil
        # Add some texture
        pygame.draw.rect(self.image, (120, 80, 40), (4, 4, TILE_SIZE - 8, TILE_SIZE - 8))
class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey((0, 0, 0))
        # Draw water puddle effect
        pygame.draw.ellipse(self.image, (64, 164, 223), (8, 12, TILE_SIZE - 16, TILE_SIZE - 24))
        pygame.draw.ellipse(self.image, (100, 180, 240), (12, 16, TILE_SIZE - 24, TILE_SIZE - 32))
        self.image.set_alpha(180)
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil water']
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((100, 149, 237))  # Cornflower blue water
        self.image.set_alpha(100)
        self.rect = self.image.get_rect(topleft=pos)

class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, pos, group, soil_tile):
        super().__init__(group)
        self.plant_type = plant_type
        self.age = 0
        self.max_age = 5
        self.grow_speed = 1
        self.harvestable = False
        self.soil_tile = soil_tile
        self.watered = False
        
        # Create plant visual
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((34, 139, 34))
        self.image.set_colorkey((0, 0, 0))
    def update_visual(self):
        # Simple visual progression
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey((0, 0, 0))
        
        center_x = TILE_SIZE // 2
        center_y = TILE_SIZE // 2 + 10
        
        # Draw plant based on age
        if self.age < 2:
            # Seedling - tiny sprout
            pygame.draw.line(self.image, (34, 139, 34), (center_x, center_y), (center_x, center_y - 8), 2)
            pygame.draw.circle(self.image, (50, 205, 50), (center_x, center_y - 8), 4)
        elif self.age < 4:
            # Growing - bigger with leaves
            pygame.draw.rect(self.image, (34, 139, 34), (center_x - 2, center_y - 15, 4, 25))
            pygame.draw.circle(self.image, (50, 205, 50), (center_x - 6, center_y - 10), 6)
            pygame.draw.circle(self.image, (50, 205, 50), (center_x + 6, center_y - 10), 6)
            pygame.draw.circle(self.image, (60, 220, 60), (center_x, center_y - 18), 8)
        else:
            # Mature - full plant with fruit/veggie
            pygame.draw.rect(self.image, (34, 139, 34), (center_x - 3, center_y - 20, 6, 30))
            # Leaves
            pygame.draw.circle(self.image, (40, 160, 40), (center_x - 10, center_y - 15), 8)
            pygame.draw.circle(self.image, (40, 160, 40), (center_x + 10, center_y - 15), 8)
            pygame.draw.circle(self.image, (50, 200, 50), (center_x, center_y - 22), 10)
            # Fruit/crop - golden color
            if self.plant_type == 'corn':
                pygame.draw.ellipse(self.image, (255, 215, 0), (center_x - 6, center_y - 28, 12, 16))
            elif self.plant_type == 'tomato':
                pygame.draw.circle(self.image, (220, 20, 60), (center_x, center_y - 24), 8)
            else:  # wheat
                pygame.draw.rect(self.image, (255, 222, 173), (center_x - 4, center_y - 30, 8, 12))
            self.harvestable = True
            # Mature - full plant
            pygame.draw.rect(self.image, (34, 139, 34), (TILE_SIZE // 2 - 3, TILE_SIZE // 2 - 10, 6, 30))
            pygame.draw.circle(self.image, (255, 215, 0), (TILE_SIZE // 2, TILE_SIZE // 2 - 15), 12)
            self.harvestable = True

    def grow(self):
        if self.watered and self.age < self.max_age:
            self.age += self.grow_speed * 0.01
            self.update_visual()
            self.watered = False

    def harvest(self):
        if self.harvestable:
            self.kill()
            return self.plant_type
        return None

class SoilLayer:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()
        
        # Grid to track soil tiles
        self.grid = {}
        
    def get_grid_pos(self, pos):
        grid_x = pos[0] // TILE_SIZE
        grid_y = pos[1] // TILE_SIZE
        return (grid_x, grid_y)
    
    def till_soil(self, pos):
        grid_pos = self.get_grid_pos(pos)
        
        if grid_pos not in self.grid:
            # Create soil tile
            world_x = grid_pos[0] * TILE_SIZE
            world_y = grid_pos[1] * TILE_SIZE
            
            soil_tile = SoilTile((world_x, world_y), [self.all_sprites, self.soil_sprites])
            self.grid[grid_pos] = {
                'soil': soil_tile,
                'water': None,
                'plant': None
            }
    
    def water(self, pos):
        grid_pos = self.get_grid_pos(pos)
        
        if grid_pos in self.grid and self.grid[grid_pos]['water'] is None:
            world_x = grid_pos[0] * TILE_SIZE
            world_y = grid_pos[1] * TILE_SIZE
            
            water_tile = WaterTile((world_x, world_y), [self.all_sprites, self.water_sprites])
            self.grid[grid_pos]['water'] = water_tile
            
            # Water the plant if exists
            if self.grid[grid_pos]['plant']:
                self.grid[grid_pos]['plant'].watered = True
    
    def plant_seed(self, pos, seed_type):
        grid_pos = self.get_grid_pos(pos)
        
        if grid_pos in self.grid and self.grid[grid_pos]['plant'] is None:
            world_x = grid_pos[0] * TILE_SIZE + TILE_SIZE // 2
            world_y = grid_pos[1] * TILE_SIZE + TILE_SIZE // 2
            
            plant = Plant(seed_type, (world_x, world_y), [self.all_sprites, self.plant_sprites], 
                         self.grid[grid_pos]['soil'])
            self.grid[grid_pos]['plant'] = plant
    
    def update_plants(self):
        for plant in self.plant_sprites:
            plant.grow()
    
    def remove_water(self):
        # Remove water sprites after a while
        for grid_pos in self.grid:
            if self.grid[grid_pos]['water']:
                self.grid[grid_pos]['water'].kill()
                self.grid[grid_pos]['water'] = None
