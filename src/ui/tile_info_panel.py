import pygame


class TileInfoPanel:
    def __init__(self, small):
        self.small = small

    def draw(self, screen, rect, terrain):
        pygame.draw.rect(screen, (36, 36, 48), rect)
        pygame.draw.rect(screen, (95, 95, 120), rect, 1)
        text = "地形: %s" % (terrain.id if terrain else "-")
        screen.blit(self.small.render(text, True, (230, 230, 230)), (rect.x + 8, rect.y + 12))

