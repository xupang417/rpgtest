import pygame


class UnitInfoPanel:
    def __init__(self, font, small):
        self.font = font
        self.small = small

    def draw(self, screen, rect, unit, title=""):
        pygame.draw.rect(screen, (36, 36, 48), rect)
        pygame.draw.rect(screen, (95, 95, 120), rect, 1)
        ty = rect.y + 8
        screen.blit(self.small.render(title, True, (235, 235, 235)), (rect.x + 8, ty))
        if not unit:
            return
        ty += 28
        lines = [unit.name, "HP %d/%d" % (unit.hp, unit.max_hp)]
        for line in lines:
            screen.blit(self.small.render(line, True, (210, 210, 220)), (rect.x + 8, ty))
            ty += 24

