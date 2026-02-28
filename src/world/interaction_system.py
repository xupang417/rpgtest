class InteractionSystem:
    """
    非战斗交互辅助：从 NPC 配置中提取可展示文本
    """
    @staticmethod
    def get_stage_npc_lines(npcs: list[dict]) -> list[str]:
        lines = []
        for npc in npcs:
            name = npc.get("name", "NPC")
            role = npc.get("role", "居民")
            line = npc.get("line", "")
            lines.append(f"{name}（{role}）：{line}".strip())
        return lines
