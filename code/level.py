import pygame
from settings import *
from player import Player
from soil import SoilLayer
from sprites import Tree, Rock, Fence, Generic
from overlay import Overlay
from random import randint

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        
        # Soil layer
        self.soil_layer = SoilLayer(self.all_sprites)
        
        self.setup()
        
        # Overlay
        self.overlay = None
        
        # Day/night cycle
        self.day_timer = 0
        self.day_length = 60  # seconds
        
    def setup(self):
        # Create ground with solid color (no checkerboard to avoid rendering issues)
        for x in range(-TILE_SIZE * 5, SCREEN_WIDTH + TILE_SIZE * 5, TILE_SIZE):
            for y in range(-TILE_SIZE * 5, SCREEN_HEIGHT + TILE_SIZE * 5, TILE_SIZE):
                ground = pygame.Surface((TILE_SIZE, TILE_SIZE))
                ground.fill((107, 142, 35))  # Olive drab green
                Generic((x, y), ground, self.all_sprites, LAYERS['ground'])
        
        # Remove fence borders - no invisible barriers!
        
        # Create trees
        tree_positions = [
            (200, 150), (400, 200), (600, 150),
            (300, 400), (500, 450), (700, 400),
            (150, 300), (850, 250), (950, 500)
        ]
        
        for pos in tree_positions:
            tree = Tree(pos, [self.all_sprites, self.collision_sprites, self.tree_sprites])
        
        # Create rocks
        rock_positions = [
            (250, 250), (550, 300), (750, 500),
            (450, 150), (650, 350)
        ]
        
        for pos in rock_positions:
            rock = Rock(pos, [self.all_sprites, self.collision_sprites])
        
        # Create player
        self.player = Player((640, 360), self.all_sprites, self.collision_sprites, self.soil_layer)
        
        # Create overlay after player
        self.overlay = Overlay(self.player)
        
    def plant_collision(self):
        # Check if player is near harvestable plants
        for plant in self.soil_layer.plant_sprites:
            if plant.harvestable and plant.rect.colliderect(self.player.hitbox.inflate(20, 20)):
                # Harvest plant on interaction
                pass
    
    def tree_collision(self):
        # Handle tree chopping
        if self.player.selected_tool == 'axe' and self.player.tool_active:
            for tree in self.tree_sprites:
                if tree.hitbox.collidepoint(self.player.get_target_pos()):
                    if tree.damage():
                        # Tree was chopped down
                        self.player.inventory['wood'] += randint(2, 5)
                        self.player.money += 10
        
    def run(self, dt):
        self.display_surface.fill((135, 206, 235))  # Sky blue
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
        
        # Update soil and plants
        self.soil_layer.update_plants()
        
        # Collisions
        self.plant_collision()
        self.tree_collision()
        
        # Overlay
        if self.overlay:
            self.overlay.display()
        
        # Day cycle
        self.day_timer += dt
        if self.day_timer >= self.day_length:
            self.day_timer = 0
            self.soil_layer.remove_water()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
    def custom_draw(self, player):
        # Camera follows player
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        
        # Sort all sprites by their z-layer first, then by y position
        sorted_sprites = sorted(self.sprites(), key=lambda sprite: (sprite.z if hasattr(sprite, 'z') else LAYERS['main'], sprite.rect.centery))
        
        # Draw all sprites with proper offset
        for sprite in sorted_sprites:
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)