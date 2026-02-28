from dataclasses import dataclass, field


@dataclass
class Inventory:
    items: dict[str, int] = field(default_factory=dict)

    def add(self, item_id: str, count: int = 1):
        self.items[item_id] = self.items.get(item_id, 0) + count

    def add_many(self, item_ids: list[str]):
        for iid in item_ids:
            self.add(iid, 1)

    def has(self, item_id: str, count: int = 1) -> bool:
        return self.items.get(item_id, 0) >= count

    def consume(self, item_id: str, count: int = 1) -> bool:
        if not self.has(item_id, count):
            return False
        self.items[item_id] -= count
        if self.items[item_id] <= 0:
            del self.items[item_id]
        return True

    def list_items(self):
        return sorted(self.items.items(), key=lambda x: x[0])

    def to_dict(self):
        return dict(self.items)

    @staticmethod
    def from_dict(data: dict):
        inv = Inventory()
        inv.items = dict(data or {})
        return inv