class QuestSystem:
    def __init__(self, quest_log):
        self.quest_log = quest_log

    def init_default_quests(self):
        if not self.quest_log.quests:
            self.quest_log.add({"id": "main_01", "name": "完成第一章", "progress": 0})

    def on_shop_buy(self):
        return None

