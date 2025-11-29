import pygame
from pygame.sprite import Group
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, soil_layer):
        super().__init__(group)

        #setup
        self.image = pygame.Surface((32, 64))
        self.image.fill('green')
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(-20, -40)

        #movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200
        self.collision_sprites = collision_sprites

        #status
        self.status = 'down'
        self.facing_direction = 'down'

        #tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        #seeds
        self.seeds = ['corn', 'tomato', 'wheat']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        #inventory
        self.inventory = {
            'wood': 0,
            'corn': 0,
            'tomato': 0,
            'wheat': 0
        }
        self.money = 100

        #tool usage
        self.tool_active = False
        self.tool_timer = 0
        self.soil_layer = soil_layer

    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil_layer.till_soil(self.get_target_pos())
        elif self.selected_tool == 'axe':
            # Will handle tree chopping
            pass
        elif self.selected_tool == 'water':
            self.soil_layer.water(self.get_target_pos())

    def use_seed(self):
        self.soil_layer.plant_seed(self.get_target_pos(), self.selected_seed)

    def get_target_pos(self):
        return self.rect.center + PLAYER_TOOL_OFFSET[self.facing_direction]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.tool_active:
            # movement
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # tool usage
            if keys[pygame.K_SPACE]:
                self.tool_active = True
                self.direction = pygame.math.Vector2()
                self.tool_timer = 0
                self.use_tool()

            # seed planting
            if keys[pygame.K_LCTRL]:
                self.tool_active = True
                self.direction = pygame.math.Vector2()
                self.tool_timer = 0
                self.use_seed()

            # tool/seed selection
            if keys[pygame.K_q]:
                self.tool_index = (self.tool_index + 1) % len(self.tools)
                self.selected_tool = self.tools[self.tool_index]

            if keys[pygame.K_e]:
                self.seed_index = (self.seed_index + 1) % len(self.seeds)
                self.selected_seed = self.seeds[self.seed_index]
        
    def update_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        else:
            # Update facing direction based on movement
            if self.direction.x != 0:
                self.facing_direction = 'right' if self.direction.x > 0 else 'left'
            if self.direction.y != 0:
                self.facing_direction = 'down' if self.direction.y > 0 else 'up'

    def update_tool_timer(self, dt):
        if self.tool_active:
            self.tool_timer += dt
            if self.tool_timer >= 0.3:
                self.tool_active = False

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if hasattr(sprite, 'hitbox') and sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery

    def move(self, dt):
        #normalize
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self, dt):
        self.input()
        self.update_status()
        self.update_tool_timer(dt)
        self.move(dt)
