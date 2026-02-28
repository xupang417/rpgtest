import json
from pathlib import Path


class Localization:
    def __init__(self, lang="zh-CN"):
        self.lang = lang
        self.texts = {}

    def load(self, path="data/localization/zh-CN.json"):
        p = Path(path)
        if p.exists():
            self.texts = json.loads(p.read_text(encoding="utf-8"))
        else:
            self.texts = {}

    def t(self, key: str, default=""):
        return self.texts.get(key, default or key)