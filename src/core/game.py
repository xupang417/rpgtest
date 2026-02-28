import pygame
from src.core.config import load_config
from src.core.scene_manager import SceneManager
from src.utils.logger import Logger
from src.content.content_loader import ContentLoader
from src.world.main_menu_scene import MainMenuScene
from src.core.game_state import GameState


class Game:
    def __init__(self):
        self.config = load_config()
        self.logger = Logger()

        pygame.init()
        self.screen = pygame.display.set_mode((self.config.screen_width, self.config.screen_height))
        pygame.display.set_caption(self.config.window_title)
        self.clock = pygame.time.Clock()
        self.running = True

        self.content = ContentLoader()
        self.content.load_all()

        self.state = GameState()

        self.scene_manager = SceneManager()
        self.scene_manager.push(
            MainMenuScene(
                self.screen,
                self.scene_manager,
                content_loader=self.content,
                config_obj=self.config,
                logger=self.logger,
                unlocked_stages=self.state.unlocked_stages
            )
        )

        self.logger.info("游戏启动：主菜单")

    def run(self):
        while self.running:
            dt = self.clock.tick(self.config.fps) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.scene_manager.handle_event(event)

            self.scene_manager.update(dt)
            self.scene_manager.draw()
            pygame.display.flip()

        pygame.quit()
        self.logger.info("游戏退出")