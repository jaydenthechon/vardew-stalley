import pygame
from settings import *

class Overlay:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def display_tool(self):
        # Tool display
        tool_surf = self.font.render(f"Tool: {self.player.selected_tool}", True, (255, 255, 255))
        tool_rect = tool_surf.get_rect(topleft=(20, SCREEN_HEIGHT - 100))
        
        # Background
        bg_rect = tool_rect.inflate(20, 10)
        pygame.draw.rect(self.display_surface, (0, 0, 0), bg_rect, border_radius=5)
        pygame.draw.rect(self.display_surface, (255, 255, 255), bg_rect, 2, border_radius=5)
        
        self.display_surface.blit(tool_surf, tool_rect)
        
    def display_seed(self):
        # Seed display
        seed_surf = self.font.render(f"Seed: {self.player.selected_seed}", True, (255, 255, 255))
        seed_rect = seed_surf.get_rect(topleft=(20, SCREEN_HEIGHT - 60))
        
        # Background
        bg_rect = seed_rect.inflate(20, 10)
        pygame.draw.rect(self.display_surface, (0, 0, 0), bg_rect, border_radius=5)
        pygame.draw.rect(self.display_surface, (255, 255, 255), bg_rect, 2, border_radius=5)
        
        self.display_surface.blit(seed_surf, seed_rect)
    
    def display_money(self):
        # Money display
        money_surf = self.font.render(f"${self.player.money}", True, (255, 215, 0))
        money_rect = money_surf.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        
        # Background
        bg_rect = money_rect.inflate(20, 10)
        pygame.draw.rect(self.display_surface, (0, 0, 0), bg_rect, border_radius=5)
        pygame.draw.rect(self.display_surface, (255, 215, 0), bg_rect, 2, border_radius=5)
        
        self.display_surface.blit(money_surf, money_rect)
    
    def display_inventory(self):
        # Display inventory items
        y_offset = 80
        inv_title = self.small_font.render("Inventory:", True, (255, 255, 255))
        self.display_surface.blit(inv_title, (SCREEN_WIDTH - 150, y_offset))
        
        y_offset += 30
        for item, amount in self.player.inventory.items():
            if amount > 0:
                item_surf = self.small_font.render(f"{item}: {amount}", True, (255, 255, 255))
                self.display_surface.blit(item_surf, (SCREEN_WIDTH - 150, y_offset))
                y_offset += 25
    
    def display_controls(self):
        # Display controls at bottom
        controls = [
            "Arrow Keys: Move",
            "SPACE: Use Tool",
            "CTRL: Plant Seed",
            "Q: Change Tool",
            "E: Change Seed"
        ]
        
        y_offset = 20
        for control in controls:
            control_surf = self.small_font.render(control, True, (200, 200, 200))
            self.display_surface.blit(control_surf, (20, y_offset))
            y_offset += 25
    
    def display(self):
        self.display_tool()
        self.display_seed()
        self.display_money()
        self.display_inventory()
        self.display_controls()
