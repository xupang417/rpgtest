class BestiarySystem:
    """
    敌人图鉴
    """
    def __init__(self):
        self.records = {}  # enemy_id -> {"name":..., "seen":bool, "defeated":int}

    def see_enemy(self, enemy_id: str, name: str):
        if enemy_id not in self.records:
            self.records[enemy_id] = {"name": name, "seen": True, "defeated": 0}
        else:
            self.records[enemy_id]["seen"] = True

    def defeat_enemy(self, enemy_id: str, name: str):
        self.see_enemy(enemy_id, name)
        self.records[enemy_id]["defeated"] += 1

    def list_all(self):
        return sorted(self.records.items(), key=lambda x: x[0])