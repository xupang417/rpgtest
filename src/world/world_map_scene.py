import pygame
from src.core.scene_manager import SceneBase
from src.world.town_scene import TownScene


class WorldMapScene(SceneBase):
    def __init__(
        self,
        screen,
        scene_manager,
        content_loader,
        logger=None,
        unlocked_stages=None,
        game_state=None
    ):
        self.screen = screen
        self.scene_manager = scene_manager
        self.content = content_loader
        self.logger = logger
        self.game_state = game_state

        self.font = pygame.font.SysFont("simhei", 24)
        self.small = pygame.font.SysFont("simhei", 18)

        if game_state is not None:
            if unlocked_stages is not None:
                game_state.unlocked_stages = unlocked_stages[:]
            self.unlocked_stages = game_state.unlocked_stages
        else:
            self.unlocked_stages = unlocked_stages or ["ch01_battle_01"]

        self.selected = 0
        self.message = "请选择章节（空格进入整备）。"
        self._stage_rects = []

        self._refresh_stage_list()

    def on_enter(self):
        if self.logger:
            self.logger.info("进入世界地图场景")

    def on_exit(self):
        if self.logger:
            self.logger.info("离开世界地图场景")

    def _refresh_stage_list(self):
        all_ids = list(self.content.stage_index.get("stages", {}).keys())
        self.stage_ids = [sid for sid in all_ids if sid in self.unlocked_stages]
        if not self.stage_ids and all_ids:
            self.stage_ids = [all_ids[0]]
        if self.selected >= len(self.stage_ids):
            self.selected = 0

    def handle_event(self, event):
        self._refresh_stage_list()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if self.stage_ids:
                self.selected = (self.selected - 1) % len(self.stage_ids)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if self.stage_ids:
                self.selected = (self.selected + 1) % len(self.stage_ids)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not self.stage_ids:
                return
            stage_id = self.stage_ids[self.selected]
            self.scene_manager.push(
                TownScene(
                    self.screen,
                    self.scene_manager,
                    content_loader=self.content,
                    stage_id=stage_id,
                    unlocked_stages=self.unlocked_stages,
                    game_state=self.game_state
                )
            )
        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self._stage_rects):
                if rect.collidepoint(event.pos):
                    self.selected = i
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self._stage_rects):
                if not rect.collidepoint(event.pos):
                    continue
                self.selected = i
                break
            if not self.stage_ids:
                return
            stage_id = self.stage_ids[self.selected]
            self.scene_manager.push(
                TownScene(
                    self.screen,
                    self.scene_manager,
                    content_loader=self.content,
                    stage_id=stage_id,
                    unlocked_stages=self.unlocked_stages,
                    game_state=self.game_state
                )
            )

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((20, 40, 70))

        title = self.font.render("世界地图", True, (255, 230, 120))
        hint = self.small.render("↑↓ 选择章节  空格进入整备", True, (235, 235, 235))
        self.screen.blit(title, (40, 30))
        self.screen.blit(hint, (40, 68))

        panel = pygame.Rect(40, 110, 540, 460)
        pygame.draw.rect(self.screen, (35, 52, 85), panel)
        pygame.draw.rect(self.screen, (120, 140, 180), panel, 2)

        y = 140
        self._stage_rects = []
        for i, sid in enumerate(self.stage_ids):
            stage = self.content.stage_index["stages"].get(sid, {})
            name = stage.get("name", sid)
            rect = pygame.Rect(52, y - 2, 500, 28)
            self._stage_rects.append(rect)
            color = (255, 230, 120) if i == self.selected else (230, 230, 230)
            if i == self.selected:
                pygame.draw.rect(self.screen, (52, 75, 110), rect)
            txt = self.small.render("%s - %s" % (sid, name), True, color)
            self.screen.blit(txt, (60, y))
            y += 34

        msg = self.small.render(self.message, True, (200, 220, 240))
        self.screen.blit(msg, (40, 590))
