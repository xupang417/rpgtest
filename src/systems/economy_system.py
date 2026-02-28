class EconomySystem:
    """
    经济系统占位（关卡奖励、任务奖励、通关奖励）
    """
    def __init__(self):
        self.gold = 0

    def add_reward(self, amount: int, reason: str = "奖励"):
        self.gold += amount
        return f"{reason}：+{amount}G（当前{self.gold}G）"

    def spend(self, amount: int):
        if self.gold < amount:
            return False, "金币不足。"
        self.gold -= amount
        return True, f"消费成功：-{amount}G（剩余{self.gold}G）"