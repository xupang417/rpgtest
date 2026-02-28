from typing import Optional, List


class SceneBase:
    """
    所有场景基类：
    - handle_event(event)
    - update(dt)
    - draw()
    - on_enter()
    - on_exit()
    """
    def handle_event(self, event):
        pass

    def update(self, dt: float):
        pass

    def draw(self):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass


class SceneManager:
    def __init__(self):
        self._stack: List[SceneBase] = []

    @property
    def current(self) -> Optional[SceneBase]:
        return self._stack[-1] if self._stack else None

    def push(self, scene: SceneBase):
        if self.current:
            self.current.on_exit()
        self._stack.append(scene)
        self.current.on_enter()

    def pop(self):
        if not self._stack:
            return
        self.current.on_exit()
        self._stack.pop()
        if self.current:
            self.current.on_enter()

    def replace(self, scene: SceneBase):
        self.pop()
        self.push(scene)

    def handle_event(self, event):
        if self.current:
            self.current.handle_event(event)

    def update(self, dt: float):
        if self.current:
            self.current.update(dt)

    def draw(self):
        if self.current:
            self.current.draw()