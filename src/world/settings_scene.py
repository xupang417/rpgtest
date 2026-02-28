import pygame
from src.core.scene_manager import SceneBase
from src.core.config import save_config


class SettingsScene(SceneBase):
    def __init__(self, screen, scene_manager, config_obj):
        self.screen = screen
        self.scene_manager = scene_manager
        self.cfg = config_obj

        self.font = pygame.font.SysFont("simhei", 28)
        self.small = pygame.font.SysFont("simhei", 18)

        self.options = ["主音量", "音效音量", "窗口模式", "保存并返回", "返回(不保存)"]
        self.selected = 0
        self.message = "左右调整参数，空格确认。"

        self.master_volume = self.cfg.master_volume
        self.sfx_volume = self.cfg.sfx_volume
        self.window_mode = self.cfg.window_mode

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.options)
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.options)
        elif event.key == pygame.K_LEFT:
            self._change_value(-5)
        elif event.key == pygame.K_RIGHT:
            self._change_value(5)
        elif event.key == pygame.K_SPACE:
            self._confirm()
        elif event.key == pygame.K_ESCAPE:
            self.scene_manager.pop()

    def _change_value(self, delta):
        op = self.options[self.selected]
        if op == "主音量":
            self.master_volume = max(0, min(100, self.master_volume + delta))
        elif op == "音效音量":
            self.sfx_volume = max(0, min(100, self.sfx_volume + delta))
        elif op == "窗口模式":
            self.window_mode = "全屏" if self.window_mode == "窗口" else "窗口"

    def _confirm(self):
        op = self.options[self.selected]
        if op == "保存并返回":
            self.cfg.master_volume = self.master_volume
            self.cfg.sfx_volume = self.sfx_volume
            self.cfg.window_mode = self.window_mode
            save_config(self.cfg)
            self.scene_manager.pop()
        elif op == "返回(不保存)":
            self.scene_manager.pop()

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((20, 24, 36))
        title = self.font.render("设置", True, (255, 230, 120))
        self.screen.blit(title, (40, 30))

        y = 120
        for i, op in enumerate(self.options):
            color = (255, 230, 120) if i == self.selected else (230, 230, 230)
            text = op
            if op == "主音量":
                text = "主音量：%d" % self.master_volume
            elif op == "音效音量":
                text = "音效音量：%d" % self.sfx_volume
            elif op == "窗口模式":
                text = "窗口模式：%s" % self.window_mode

            row = self.small.render(text, True, color)
            self.screen.blit(row, (60, y))
            y += 42

        msg = self.small.render(self.message, True, (200, 200, 220))
        self.screen.blit(msg, (40, self.screen.get_height() - 40))