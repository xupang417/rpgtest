import pygame


class ActionMenu:
    """
    完整鼠标版行动菜单（中文）
    """
    def __init__(self, font, small):
        self.font = font
        self.small = small
        self.visible = False
        self.options = []
        self.selected = 0
        self.anchor = (0, 0)

        self._item_rects = []
        self._menu_rect = pygame.Rect(0, 0, 0, 0)

    def open(self, x, y, options=None):
        self.visible = True
        self.selected = 0
        self.anchor = (x, y)
        self.options = options[:] if options else ["攻击", "技能", "待机", "取消"]

    def close(self):
        self.visible = False
        self.options = []
        self._item_rects = []
        self._menu_rect = pygame.Rect(0, 0, 0, 0)

    def current_option(self):
        if not self.visible or not self.options:
            return None
        return self.options[self.selected]

    def _layout(self, screen):
        x, y = self.anchor
        w = 210
        h = 14 + len(self.options) * 30 + 10
        rect = pygame.Rect(x, y, w, h)

        sw, sh = screen.get_size()
        if rect.right > sw:
            rect.x = sw - w - 8
        if rect.bottom > sh:
            rect.y = sh - h - 8

        self._menu_rect = rect
        self._item_rects = []
        ty = rect.y + 10
        for _ in self.options:
            r = pygame.Rect(rect.x + 8, ty - 2, rect.width - 16, 26)
            self._item_rects.append(r)
            ty += 30

    def handle_mouse_move(self, pos):
        if not self.visible:
            return
        x, y = pos
        for i, r in enumerate(self._item_rects):
            if r.collidepoint(x, y):
                self.selected = i
                return

    def handle_mouse_click(self, pos):
        """
        返回:
        - None: 未点击到菜单项
        - str : 点击到的选项文本
        """
        if not self.visible:
            return None

        x, y = pos
        for i, r in enumerate(self._item_rects):
            if r.collidepoint(x, y):
                self.selected = i
                return self.options[i]
        return None

    def draw(self, screen):
        if not self.visible:
            return

        self._layout(screen)

        pygame.draw.rect(screen, (44, 44, 58), self._menu_rect)
        pygame.draw.rect(screen, (120, 120, 150), self._menu_rect, 2)

        ty = self._menu_rect.y + 10
        for i, op in enumerate(self.options):
            is_sel = (i == self.selected)
            if is_sel:
                pygame.draw.rect(screen, (80, 80, 110), self._item_rects[i])

            color = (255, 230, 120) if is_sel else (230, 230, 230)
            s = self.small.render(op, True, color)
            screen.blit(s, (self._menu_rect.x + 14, ty))
            ty += 30