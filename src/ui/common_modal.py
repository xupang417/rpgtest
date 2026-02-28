import pygame


class CommonModal:
    def __init__(self):
        self.visible = False
        self.title = ""
        self.lines = []
        self.font = pygame.font.SysFont("simhei", 24)
        self.small = pygame.font.SysFont("simhei", 18)

    def open(self, title, lines):
        self.visible = True
        self.title = title
        self.lines = lines[:]

    def close(self):
        self.visible = False
        self.title = ""
        self.lines = []

    def draw(self, screen):
        if not self.visible:
            return

        sw, sh = screen.get_size()
        rect = pygame.Rect(200, 120, sw - 400, sh - 240)
        pygame.draw.rect(screen, (25, 25, 40), rect)
        pygame.draw.rect(screen, (120, 120, 150), rect, 2)

        screen.blit(self.font.render(self.title, True, (255, 230, 120)), (rect.x + 16, rect.y + 12))

        y = rect.y + 60
        for ln in self.lines:
            screen.blit(self.small.render(ln, True, (230, 230, 230)), (rect.x + 20, y))
            y += 28

        tip = self.small.render("空格/回车关闭", True, (180, 200, 230))
        screen.blit(tip, (rect.right - 160, rect.bottom - 30))