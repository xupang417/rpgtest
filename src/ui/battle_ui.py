import pygame
from src.ui.unit_info_panel import UnitInfoPanel
from src.ui.tile_info_panel import TileInfoPanel
from src.ui.turn_order_panel import TurnOrderPanel
from src.ui.action_menu import ActionMenu
from src.ui.menu_class_change import ClassChangeMenu
from src.ui.combat_preview_panel import CombatPreviewPanel


class BattleUI:
    def __init__(self):
        self.font = pygame.font.SysFont("simhei", 20)
        self.small = pygame.font.SysFont("simhei", 16)

        self.unit_info = UnitInfoPanel(self.font, self.small)
        self.tile_info = TileInfoPanel(self.small)
        self.turn_info = TurnOrderPanel(self.small)
        self.action_menu = ActionMenu(self.font, self.small)
        self.class_change_menu = ClassChangeMenu()
        self.preview_panel = CombatPreviewPanel()

    def draw(self, screen, ctx):
        sw, sh = screen.get_size()
        right_w = 320
        right_x = sw - right_w

        right_bg = pygame.Rect(right_x, 0, right_w, sh - 100)
        pygame.draw.rect(screen, (26, 26, 38), right_bg)
        pygame.draw.rect(screen, (90, 90, 120), right_bg, 2)

        rect_turn = pygame.Rect(right_x + 16, 20, right_w - 32, 70)
        rect_tile = pygame.Rect(right_x + 16, 100, right_w - 32, 100)
        rect_cursor = pygame.Rect(right_x + 16, 210, right_w - 32, 190)
        rect_selected = pygame.Rect(right_x + 16, 410, right_w - 32, 190)

        self.turn_info.draw(screen, rect_turn, ctx["phase"], ctx["turn_count"])
        self.tile_info.draw(screen, rect_tile, ctx["terrain"])
        self.unit_info.draw(screen, rect_cursor, ctx["cursor_unit"], title="光标单位")
        self.unit_info.draw(screen, rect_selected, ctx["selected_unit"], title="选中单位")

        msg_rect = pygame.Rect(0, sh - 100, sw, 100)
        pygame.draw.rect(screen, (32, 32, 44), msg_rect)
        pygame.draw.rect(screen, (95, 95, 130), msg_rect, 2)

        controls = "鼠标左键:确认  鼠标右键:取消  Enter:结束回合  P:转职  F5/F9:存读档"
        t1 = self.small.render(controls, True, (235, 235, 235))
        t2 = self.small.render(ctx["message"], True, (200, 200, 220))
        screen.blit(t1, (16, sh - 88))
        screen.blit(t2, (16, sh - 58))

        self.action_menu.draw(screen)
        self.class_change_menu.draw(screen)
        self.preview_panel.draw(screen)