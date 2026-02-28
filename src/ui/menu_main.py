import pygame


class MainMenuUI:
    def __init__(self):
        self.font = pygame.font.SysFont("simhei", 32)
        self.small = pygame.font.SysFont("simhei", 20)
        self.options = ["开始", "退出"]
        self.selected = 0
        self.option_rects = []

    def handle_key(self, key):
        if key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.options)
        elif key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.options)
        elif key == pygame.K_SPACE:
            return self.options[self.selected]
        return None

    def draw(self, screen):
        screen.fill((16, 24, 40))
        title = self.font.render("像素战旗", True, (255, 230, 120))
        screen.blit(title, (40, 40))
        y = 180
        self.option_rects = []
        for i, option in enumerate(self.options):
            rect = pygame.Rect(52, y - 2, 320, 30)
            self.option_rects.append(rect)
            color = (255, 230, 120) if i == self.selected else (230, 230, 230)
            if i == self.selected:
                pygame.draw.rect(screen, (48, 64, 92), rect)
            row = self.small.render(option, True, color)
            screen.blit(row, (60, y))
            y += 40

    def hover(self, pos):
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(pos):
                self.selected = i
                return

    def click(self, pos):
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(pos):
                self.selected = i
                return self.options[i]
        return None
