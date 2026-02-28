class TravelSystem:
    """
    世界地图移动/章节跳转规则占位
    """
    def __init__(self):
        self.current_node = "王都"

    def can_travel(self, target_node: str, unlocked_nodes: list[str]) -> bool:
        return target_node in unlocked_nodes

    def travel_to(self, target_node: str, unlocked_nodes: list[str]) -> tuple[bool, str]:
        if not self.can_travel(target_node, unlocked_nodes):
            return False, f"尚未解锁目的地：{target_node}"
        self.current_node = target_node
        return True, f"已到达：{target_node}"