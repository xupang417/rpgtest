import os
import sys
from pathlib import Path
import pygame

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.battle.tactical_scene import TacticalScene
from src.content.content_loader import ContentLoader
from src.core.game_state import GameState


os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


class DummySceneManager:
    def __init__(self):
        self.pop_count = 0
        self.replaced_scene = None

    def pop(self):
        self.pop_count += 1

    def replace(self, scene):
        self.replaced_scene = scene


def _build_scene():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    content = ContentLoader()
    content.load_all()
    gs = GameState()
    mgr = DummySceneManager()
    scene = TacticalScene(
        screen=screen,
        scene_manager=mgr,
        logger=None,
        stage_id="ch01_battle_01",
        content_loader=content,
        unlocked_stages=gs.unlocked_stages,
        deploy_ids=["p1", "p2", "p3"],
        game_state=gs,
    )
    return scene, mgr, gs


def test_cancel_after_move_consumes_action():
    scene, _, _ = _build_scene()
    unit = scene.players[0]

    scene._on_left_click((unit.x * 64 + 4, unit.y * 64 + 4))
    scene._on_left_click((unit.x * 64 + 4, (unit.y - 1) * 64 + 4))
    scene.draw()

    cancel_rect = scene.action_menu._item_rects[-1]
    scene._on_left_click(cancel_rect.center)

    assert unit.acted is True

    scene._on_left_click((unit.x * 64 + 4, unit.y * 64 + 4))
    assert scene.selected_unit is None


def test_auto_enemy_phase_when_all_players_acted():
    scene, _, _ = _build_scene()
    for unit in scene.players[1:]:
        unit.acted = True
    scene._finish_player_action(scene.players[0])

    assert scene.phase == "player"
    assert scene.turn_count == 2
    assert all(not u.acted for u in scene.players if u.alive)


def test_victory_unlocks_and_enters_next_chapter():
    scene, mgr, gs = _build_scene()

    scene._end_battle(victory=True)

    assert "ch02_battle_01" in gs.unlocked_stages
    assert mgr.pop_count == 1
    assert mgr.replaced_scene is not None
    assert getattr(mgr.replaced_scene, "stage_id", "") == "ch02_battle_01"
