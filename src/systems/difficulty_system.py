class DifficultySystem:
    """
    难度修正占位：普通/困难
    """
    def __init__(self, mode="normal"):
        self.mode = mode

    def enemy_hp_multiplier(self):
        return 1.0 if self.mode == "normal" else 1.2

    def enemy_atk_multiplier(self):
        return 1.0 if self.mode == "normal" else 1.15

    def exp_multiplier(self):
        return 1.0 if self.mode == "normal" else 1.1