class ChapterStatsSystem:
    def __init__(self):
        self.data = {}  # stage_id -> stats

    def start_stage(self, stage_id):
        if stage_id not in self.data:
            self.data[stage_id] = {
                "turns": 0,
                "player_down": 0,
                "enemy_defeated": 0,
                "clear": False
            }

    def add_turn(self, stage_id):
        if stage_id in self.data:
            self.data[stage_id]["turns"] += 1

    def add_enemy_defeat(self, stage_id, n=1):
        if stage_id in self.data:
            self.data[stage_id]["enemy_defeated"] += n

    def add_player_down(self, stage_id, n=1):
        if stage_id in self.data:
            self.data[stage_id]["player_down"] += n

    def mark_clear(self, stage_id):
        if stage_id in self.data:
            self.data[stage_id]["clear"] = True

    def get(self, stage_id):
        return self.data.get(stage_id, None)