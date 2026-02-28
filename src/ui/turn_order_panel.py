import pygame


class TurnOrderPanel:
    def __init__(self, small):
        self.small = small

    def draw(self, screen, rect, phase, turn_count):
        pygame.draw.rect(screen, (36, 36, 48), rect)
        pygame.draw.rect(screen, (95, 95, 120), rect, 1)
        line = "回合 %d  阶段: %s" % (turn_count, phase)
        screen.blit(self.small.render(line, True, (230, 230, 230)), (rect.x + 8, rect.y + 12))

