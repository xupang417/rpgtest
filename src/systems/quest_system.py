import json
from pathlib import Path


class QuestSystem:
    def __init__(self, quest_log):
        self.quest_log = quest_log
        self.main_quests = self._load_quest_file("data/quests/main_quests.json")
        self.side_quests = self._load_quest_file("data/quests/side_quests.json")

    @staticmethod
    def _load_quest_file(path: str) -> list[dict]:
        p = Path(path)
        if not p.exists():
            return []
        raw = json.loads(p.read_text(encoding="utf-8"))
        return raw.get("quests", [])

    def init_default_quests(self):
        if self.quest_log.quests:
            return
        for q in self.main_quests + self.side_quests:
            self.quest_log.add(q)

    def on_shop_buy(self):
        return None

    def on_stage_clear(self, stage_id: str, inventory=None, shop=None, npc_system=None, party=None, content=None) -> dict:
        rewards = {"gold": 0, "items": [], "recruited": []}
        all_quests = self.main_quests + self.side_quests
        for q in all_quests:
            if q.get("target_stage") and q.get("target_stage") != stage_id:
                continue
            if not self.quest_log.complete(q.get("id", "")):
                continue

            rw = q.get("rewards", {})
            gold = int(rw.get("gold", 0) or 0)
            rewards["gold"] += gold
            if shop is not None and gold:
                shop.gold += gold

            items = list(rw.get("items", []))
            rewards["items"].extend(items)
            if inventory is not None and items:
                inventory.add_many(items)

            recruit_id = rw.get("recruit_npc")
            if recruit_id and npc_system is not None and party is not None and content is not None:
                added = npc_system.recruit_to_party(recruit_id, party, content)
                if added:
                    rewards["recruited"].append(added.name)
        return rewards
