from src.content.class_loader import load_classes
from src.content.item_loader import load_weapons
from src.content.stage_loader import load_stage_index, load_stage_file
from src.content.enemy_loader import load_enemy_templates
from src.content.skill_loader import load_skills
from src.content.promotion_loader import load_promotions
from src.content.story_loader import load_main_story


class ContentLoader:
    def __init__(self):
        self.classes = {}
        self.weapons = {}
        self.skills = {}
        self.promotions = []
        self.stage_index = {}
        self.enemy_templates = {}
        self.story = {}

    def load_all(self):
        self.classes = load_classes()
        self.weapons = load_weapons()
        self.skills = load_skills()
        self.promotions = load_promotions()
        self.stage_index = load_stage_index()
        self.enemy_templates = load_enemy_templates()
        self.story = load_main_story()

    def load_stage(self, stage_id: str) -> dict:
        entry = self.stage_index.get("stages", {}).get(stage_id)
        if not entry:
            return {}
        return load_stage_file(entry["file"])

    def get_next_stage(self, stage_id: str) -> str:
        entry = self.stage_index.get("stages", {}).get(stage_id, {})
        return entry.get("next_stage", "")