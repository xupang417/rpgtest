class AchievementSystem:
    def __init__(self):
        self.unlocked = set()
        self.defeated_total = 0

    def on_enemy_defeated(self):
        self.defeated_total += 1
        if self.defeated_total >= 10:
            self.unlocked.add("ach_10_kills")
        if self.defeated_total >= 50:
            self.unlocked.add("ach_50_kills")

    def on_first_promotion(self):
        self.unlocked.add("ach_first_promotion")

    def on_clear_ch1(self):
        self.unlocked.add("ach_clear_ch1")

    def list_achievements(self):
        mapping = {
            "ach_10_kills": "初露锋芒：累计击败10名敌人",
            "ach_50_kills": "百战老兵：累计击败50名敌人",
            "ach_first_promotion": "晋升之路：完成首次转职",
            "ach_clear_ch1": "第一章完结"
        }
        return [mapping[k] for k in sorted(self.unlocked) if k in mapping]