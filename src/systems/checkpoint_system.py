from src.core.save_system import save_game


class CheckpointSystem:
    """
    检查点自动存档
    """
    def auto_save(self, slot: int, data: dict, reason="检查点"):
        save_game(slot, data)
        return f"已自动存档（槽{slot}）：{reason}"