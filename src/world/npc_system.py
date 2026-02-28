class NPCSystem:
    """
    章节相关 NPC 与招募信息管理（轻量版）
    """
    def __init__(self, npc_data: dict | None = None):
        self.npc_data = npc_data or {}
        self.recruited_ids = set()
        self._npc_index = {}
        for npcs in self.npc_data.values():
            for npc in npcs:
                if npc.get("id"):
                    self._npc_index[npc["id"]] = npc

    def npcs_for_stage(self, stage_id: str) -> list[dict]:
        return list(self.npc_data.get(stage_id, []))

    def recruit(self, npc_id: str):
        self.recruited_ids.add(npc_id)

    def is_recruited(self, npc_id: str) -> bool:
        return npc_id in self.recruited_ids

    def recruit_to_party(self, npc_id: str, party, content):
        if self.is_recruited(npc_id):
            return None
        npc = self._npc_index.get(npc_id)
        if not npc:
            return None
        unit_cfg = npc.get("recruit_unit")
        if not unit_cfg:
            self.recruit(npc_id)
            return None

        from src.rpg.unit import Unit
        from src.rpg.stats import Stats

        class_id = unit_cfg.get("class_id")
        weapon_id = unit_cfg.get("weapon_id")
        if class_id not in content.classes or weapon_id not in content.weapons:
            return None
        st = unit_cfg.get("stats", {})
        spawn = unit_cfg.get("spawn", [0, 0])
        unit = Unit(
            id=npc_id,
            name=unit_cfg.get("name", npc.get("name", npc_id)),
            team="player",
            x=spawn[0],
            y=spawn[1],
            job=content.classes[class_id],
            base=Stats(
                hp=st.get("hp", 18),
                str_=st.get("str", 4),
                mag=st.get("mag", 4),
                skl=st.get("skl", 5),
                spd=st.get("spd", 5),
                lck=st.get("lck", 4),
                def_=st.get("def", 3),
                res=st.get("res", 5),
            ),
            weapon=content.weapons[weapon_id],
        )
        party.all_members.append(unit)
        self.recruit(npc_id)
        return unit
