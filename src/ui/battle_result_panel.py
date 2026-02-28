import pygame


class BattleResultPanel:
    def __init__(self):
        self.visible = False
        self.font = pygame.font.SysFont("simhei", 28)
        self.small = pygame.font.SysFont("simhei", 18)
        self.result = {}

    def open(self, result_data: dict):
        self.visible = True
        self.result = result_data or {}

    def close(self):
        self.visible = False
        self.result = {}

    def draw(self, screen):
        if not self.visible:
            return

        sw, sh = screen.get_size()
        rect = pygame.Rect(170, 110, sw - 340, sh - 220)

        pygame.draw.rect(screen, (24, 24, 36), rect)
        pygame.draw.rect(screen, (130, 130, 170), rect, 2)

        title = self.font.render("战斗结算", True, (255, 230, 120))
        screen.blit(title, (rect.x + 20, rect.y + 16))

        stage = self.result.get("stage_id", "")
        gold = self.result.get("gold", 0)
        items = self.result.get("items", [])
        exp_summary = self.result.get("exp_summary", [])

        y = rect.y + 70
        screen.blit(self.small.render(f"关卡：{stage}", True, (230, 230, 230)), (rect.x + 20, y))
        y += 30
        screen.blit(self.small.render(f"获得金币：{gold}G", True, (230, 230, 230)), (rect.x + 20, y))
        y += 30

        item_txt = "、".join(items) if items else "无"
        screen.blit(self.small.render(f"获得物品：{item_txt}", True, (230, 230, 230)), (rect.x + 20, y))
        y += 40

        screen.blit(self.small.render("单位经验摘要：", True, (255, 230, 120)), (rect.x + 20, y))
        y += 30
        if not exp_summary:
            screen.blit(self.small.render("无", True, (230, 230, 230)), (rect.x + 30, y))
        else:
            for row in exp_summary[:10]:
                line = f"{row['name']}  Lv{row['level']}  EXP {row['exp']}/100"
                screen.blit(self.small.render(line, True, (230, 230, 230)), (rect.x + 30, y))
                y += 24

        hint = self.small.render("回车：确认并继续", True, (200, 220, 255))
        screen.blit(hint, (rect.right - 170, rect.bottom - 36))