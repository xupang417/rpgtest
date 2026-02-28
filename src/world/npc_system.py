class NPCSystem:
    """
    章节相关 NPC 与招募信息管理（轻量版）
    """
    def __init__(self, npc_data: dict | None = None):
        self.npc_data = npc_data or {}
        self.recruited_ids = set()

    def npcs_for_stage(self, stage_id: str) -> list[dict]:
        return list(self.npc_data.get(stage_id, []))

    def recruit(self, npc_id: str):
        self.recruited_ids.add(npc_id)

    def is_recruited(self, npc_id: str) -> bool:
        return npc_id in self.recruited_ids
