class QuestLog:
    def __init__(self):
        self.quests = []

    def add(self, quest: dict):
        self.quests.append(dict(quest))

