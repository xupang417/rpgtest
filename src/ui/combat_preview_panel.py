import pygame


class CombatPreviewPanel:
    def __init__(self):
        self.font = pygame.font.SysFont("simhei", 18)
        self.small = pygame.font.SysFont("simhei", 16)
        self.visible = False
        self.data = None

    def show(self, data: dict):
        self.visible = True
        self.data = data

    def hide(self):
        self.visible = False
        self.data = None

    def draw(self, screen):
        if not self.visible or not self.data:
            return

        rect = pygame.Rect(20, 20, 300, 170)
        pygame.draw.rect(screen, (24, 24, 36), rect)
        pygame.draw.rect(screen, (120, 120, 160), rect, 2)

        title = self.font.render("战斗预览", True, (255, 230, 120))
        screen.blit(title, (rect.x + 10, rect.y + 8))

        attacker = self.data.get("attacker", "我方")
        defender = self.data.get("defender", "敌方")
        hit = self.data.get("hit", 0)
        crit = self.data.get("crit", 0)
        dmg = self.data.get("damage", 0)
        counter = self.data.get("counter", "否")

        rows = [
            "攻击方：%s" % attacker,
            "防守方：%s" % defender,
            "预计命中：%d%%" % hit,
            "预计暴击：%d%%" % crit,
            "预计伤害：%d" % dmg,
            "可能反击：%s" % counter,
        ]

        y = rect.y + 42
        for row in rows:
            s = self.small.render(row, True, (230, 230, 230))
            screen.blit(s, (rect.x + 12, y))
            y += 21