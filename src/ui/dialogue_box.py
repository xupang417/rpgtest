import pygame


class DialogueBox:
    def __init__(self):
        self.visible = False
        self.lines = []
        self.index = 0

        self.font = pygame.font.SysFont("simhei", 20)
        self.small = pygame.font.SysFont("simhei", 18)

    def open(self, lines: list[dict]):
        self.lines = lines or []
        self.index = 0
        self.visible = True if self.lines else False

    def close(self):
        self.visible = False
        self.lines = []
        self.index = 0

    def current(self):
        if not self.visible or not self.lines:
            return None
        return self.lines[self.index]

    def next_line(self):
        if not self.visible:
            return False
        self.index += 1
        if self.index >= len(self.lines):
            self.close()
            return False
        return True

    def draw(self, screen):
        if not self.visible:
            return

        sw, sh = screen.get_size()
        rect = pygame.Rect(24, sh - 180, sw - 48, 150)
        pygame.draw.rect(screen, (28, 28, 42), rect)
        pygame.draw.rect(screen, (120, 120, 150), rect, 2)

        cur = self.current()
        if not cur:
            return

        speaker = cur.get("speaker", "???")
        text = cur.get("text", "")

        sp = self.font.render(f"{speaker}", True, (255, 230, 120))
        tx = self.small.render(text, True, (235, 235, 235))
        hint = self.small.render("空格：下一句", True, (180, 180, 210))

        screen.blit(sp, (rect.x + 14, rect.y + 10))
        screen.blit(tx, (rect.x + 14, rect.y + 52))
        screen.blit(hint, (rect.right - 140, rect.bottom - 30))