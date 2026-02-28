import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.content.content_loader import ContentLoader
from src.world.npc_system import NPCSystem
from src.world.interaction_system import InteractionSystem
from src.world.chapter_flow import ChapterFlow


def test_story_and_stage_content_extended():
    loader = ContentLoader()
    loader.load_all()

    assert "prologue" in loader.story
    assert "ch03_battle_01_intro" in loader.story
    assert "side_rescue_medic" in loader.side_story

    assert loader.get_next_stage("ch02_battle_01") == "ch03_battle_01"
    st3 = loader.load_stage("ch03_battle_01")
    assert st3.get("id") == "ch03_battle_01"
    assert len(st3.get("enemy_units", [])) >= 3

    d3 = loader.load_chapter_dialogues("chapter_03")
    assert d3.get("chapter_id") == "chapter_03"
    assert len(d3.get("town_dialogues", [])) >= 1


def test_npc_interaction_and_chapter_flow_helpers():
    npc_data = {
        "ch01_battle_01": [
            {"id": "npc_a", "name": "斥候", "role": "情报员", "line": "发现敌军。"}
        ]
    }
    npc_system = NPCSystem(npc_data)
    npcs = npc_system.npcs_for_stage("ch01_battle_01")
    assert len(npcs) == 1

    lines = InteractionSystem.get_stage_npc_lines(npcs)
    assert lines and "斥候" in lines[0]

    npc_system.recruit("npc_a")
    assert npc_system.is_recruited("npc_a")

    flow = ChapterFlow()
    flow.mark_completed("ch01_battle_01")
    assert flow.is_completed("ch01_battle_01")

