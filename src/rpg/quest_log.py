class QuestLog:
    def __init__(self):
        self.quests = []

    def add(self, quest: dict):
        q = dict(quest)
        q.setdefault("status", "active")
        self.quests.append(q)

    def has(self, quest_id: str) -> bool:
        return any(q.get("id") == quest_id for q in self.quests)

    def complete(self, quest_id: str) -> bool:
        for q in self.quests:
            if q.get("id") == quest_id and q.get("status") != "done":
                q["status"] = "done"
                return True
        return False
