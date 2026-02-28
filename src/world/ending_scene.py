import pygame
from src.core.scene_manager import SceneBase


class EndingScene(SceneBase):
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.font = pygame.font.SysFont("simhei", 30)
        self.small = pygame.font.SysFont("simhei", 20)
        self.lines = [
            "第一章制作名单",
            "策划/程序：你 + Copilot",
            "测试：你自己",
            "",
            "感谢游玩！",
            "按 Esc / Enter 返回"
        ]
        self.offset = 0.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                self.scene_manager.pop()

    def update(self, dt):
        self.offset += 18 * dt

    def draw(self):
        self.screen.fill((10, 10, 18))
        y0 = self.screen.get_height() - int(self.offset)
        for i, line in enumerate(self.lines):
            font = self.font if i == 0 else self.small
            txt = font.render(line, True, (235, 235, 235))
            self.screen.blit(txt, (self.screen.get_width() // 2 - txt.get_width() // 2, y0 + i * 42))