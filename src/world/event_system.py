import json
from pathlib import Path


class EventSystem:
    """
    简易事件系统：
    - 按章节ID读取事件列表
    - 支持一次性事件标记
    """
    def __init__(self, event_file="data/story/main_story.json"):
        self.event_file = Path(event_file)
        self.data = {}
        self.triggered = set()

        if self.event_file.exists():
            raw = json.loads(self.event_file.read_text(encoding="utf-8"))
            self.data = raw.get("story", {})

    def get_events(self, event_key: str):
        return self.data.get(event_key, [])

    def trigger_once(self, event_id: str) -> bool:
        if event_id in self.triggered:
            return False
        self.triggered.add(event_id)
        return True