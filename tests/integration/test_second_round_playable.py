import json
import os
import sys
from pathlib import Path

import pygame

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.content.content_loader import ContentLoader
from src.core.game_state import GameState
from src.rpg.inventory import Inventory
from src.rpg.party import Party
from src.rpg.stats import Stats
from src.rpg.unit import Unit
from src.systems.shop_system import ShopSystem
from src.ui.menu_class_change import ClassChangeMenu
from src.world.npc_system import NPCSystem
from src.battle.tactical_scene import TacticalScene


os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


class DummySceneManager:
    def __init__(self):
        self.replaced_scene = None

    def pop(self):
        return None

    def replace(self, scene):
        self.replaced_scene = scene


def _load_npc_data():
    p = Path("/home/runner/work/rpgtest/rpgtest/data/npcs/npcs.json")
    raw = json.loads(p.read_text(encoding="utf-8"))
    return raw.get("npcs", {})


def test_stage_clear_grants_rewards_and_recruits_npc():
    content = ContentLoader()
    content.load_all()
    gs = GameState()
    inv = Inventory()
    shop = ShopSystem(initial_gold=100)
    party = Party(max_deploy=3)
    base = Unit("p1", "Aren", "player", 0, 0, content.classes["lord"], Stats(24, 8, 2, 8, 8, 6, 6, 3), content.weapons["iron_sword"])
    party.set_all_members([base])
    party.deployed_ids = ["p1"]
    npc_system = NPCSystem(_load_npc_data())

    rewards = gs.quest_system.on_stage_clear(
        "ch01_battle_01",
        inventory=inv,
        shop=shop,
        npc_system=npc_system,
        party=party,
        content=content,
    )

    assert rewards["gold"] >= 700
    assert shop.gold >= 800
    assert inv.has("potion_m", 1)
    assert any(u.id == "npc_healer_lysa" for u in party.all_members)


def test_class_change_menu_promotes_unit():
    content = ContentLoader()
    content.load_all()
    inv = Inventory()
    inv.add("seal_master", 1)
    u = Unit("p1", "Aren", "player", 0, 0, content.classes["lord"], Stats(24, 8, 2, 8, 8, 6, 6, 3), content.weapons["iron_sword"])
    u.level = 10

    menu = ClassChangeMenu()
    menu.open([u], content.promotions, content.classes, content.skills, inv)
    menu.handle_key(pygame.K_RETURN)

    assert u.job.id == "swordmaster"
    assert inv.has("seal_master", 1) is False


def test_battle_victory_sets_pending_victory_dialogue():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    content = ContentLoader()
    content.load_all()
    gs = GameState()
    gs.shop_system = ShopSystem(initial_gold=0)
    gs.camp_inventory = Inventory()
    gs.npc_system = NPCSystem(_load_npc_data())

    mgr = DummySceneManager()
    scene = TacticalScene(
        screen=screen,
        scene_manager=mgr,
        logger=None,
        stage_id="ch01_battle_01",
        content_loader=content,
        unlocked_stages=gs.unlocked_stages,
        deploy_ids=["p1", "p2", "p3"],
        external_inventory=gs.camp_inventory,
        game_state=gs,
    )
    party = Party(max_deploy=3)
    party.set_all_members(scene.players[:])
    party.deployed_ids = [u.id for u in scene.players[:3]]
    gs.camp_party = party

    scene._end_battle(victory=True)
    assert mgr.replaced_scene is not None
    assert getattr(mgr.replaced_scene, "dialogue_box").visible is True
