import pygame
from src.core.scene_manager import SceneBase
from src.world.world_map_scene import WorldMapScene
from src.world.settings_scene import SettingsScene
from src.ui.menu_main import MainMenuUI
from src.core.save_system import load_game


class MainMenuScene(SceneBase):
    def __init__(self, screen, scene_manager, content_loader, config_obj, logger=None, unlocked_stages=None):
        self.screen = screen
        self.scene_manager = scene_manager
        self.content = content_loader
        self.cfg = config_obj
        self.logger = logger
        self.unlocked_stages = unlocked_stages or ["ch01_battle_01"]

        self.ui = MainMenuUI()
        # 覆盖菜单文本
        self.ui.options = ["开始新游戏", "继续游戏(槽1)", "设置", "退出"]

        self.message = "欢迎来到像素王国。"

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        action = self.ui.handle_key(event.key)
        if not action:
            return

        if action == "开始新游戏":
            self.scene_manager.push(
                WorldMapScene(
                    self.screen,
                    self.scene_manager,
                    content_loader=self.content,
                    logger=self.logger,
                    unlocked_stages=self.unlocked_stages
                )
            )

        elif action == "继续游戏(槽1)":
            data = load_game(1)
            if data is None:
                self.message = "存档槽1为空。"
            else:
                # 继续游戏：进入世界地图并带解锁信息（简化）
                unlocked = data.get("unlocked_stages", self.unlocked_stages)
                self.scene_manager.push(
                    WorldMapScene(
                        self.screen,
                        self.scene_manager,
                        content_loader=self.content,
                        logger=self.logger,
                        unlocked_stages=unlocked
                    )
                )

        elif action == "设置":
            self.scene_manager.push(SettingsScene(self.screen, self.scene_manager, self.cfg))

        elif action == "退出":
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self, dt):
        pass

    def draw(self):
        self.ui.draw(self.screen)
        small = pygame.font.SysFont("simhei", 18)
        tip = small.render(self.message, True, (210, 210, 220))
        self.screen.blit(tip, (20, self.screen.get_height() - 30))