from src.rpg.quest_log import QuestLog
from src.systems.quest_system import QuestSystem
from src.systems.bestiary_system import BestiarySystem
from src.systems.item_codex_system import ItemCodexSystem
from src.systems.achievement_system import AchievementSystem
from src.systems.chapter_stats_system import ChapterStatsSystem


class GameState:
    def __init__(self):
        self.unlocked_stages = ["ch01_battle_01"]

        self.quest_log = QuestLog()
        self.quest_system = QuestSystem(self.quest_log)
        self.quest_system.init_default_quests()

        self.bestiary = BestiarySystem()
        self.item_codex = ItemCodexSystem()
        self.achievement = AchievementSystem()
        self.chapter_stats = ChapterStatsSystem()