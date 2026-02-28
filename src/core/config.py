import json
from pathlib import Path


class Config:
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.fps = 60
        self.window_title = "像素王国战棋RPG"

        self.master_volume = 80
        self.sfx_volume = 80
        self.window_mode = "窗口"

    def to_dict(self):
        return {
            "screen_width": self.screen_width,
            "screen_height": self.screen_height,
            "fps": self.fps,
            "window_title": self.window_title,
            "master_volume": self.master_volume,
            "sfx_volume": self.sfx_volume,
            "window_mode": self.window_mode,
        }

    @staticmethod
    def from_dict(data):
        c = Config()
        for k, v in data.items():
            if hasattr(c, k):
                setattr(c, k, v)
        return c


CFG_PATH = Path("config.json")


def load_config():
    if not CFG_PATH.exists():
        cfg = Config()
        save_config(cfg)
        return cfg

    raw = json.loads(CFG_PATH.read_text(encoding="utf-8"))
    return Config.from_dict(raw)


def save_config(cfg: Config):
    CFG_PATH.write_text(json.dumps(cfg.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")