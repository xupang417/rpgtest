from dataclasses import dataclass, field


@dataclass
class Party:
    all_members: list = field(default_factory=list)
    deployed_ids: list[str] = field(default_factory=list)
    max_deploy: int = 3

    def set_all_members(self, members: list):
        self.all_members = members

    def deployed_members(self):
        lookup = {u.id: u for u in self.all_members}
        return [lookup[i] for i in self.deployed_ids if i in lookup]

    def reserve_members(self):
        dep = set(self.deployed_ids)
        return [u for u in self.all_members if u.id not in dep]

    def toggle_deploy(self, unit_id: str) -> tuple[bool, str]:
        if unit_id in self.deployed_ids:
            self.deployed_ids.remove(unit_id)
            return True, f"{unit_id} 已从上阵名单移除。"
        if len(self.deployed_ids) >= self.max_deploy:
            return False, f"上阵人数已满（最多{self.max_deploy}人）。"
        self.deployed_ids.append(unit_id)
        return True, f"{unit_id} 已加入上阵名单。"