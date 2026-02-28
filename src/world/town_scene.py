import pygame
from src.core.scene_manager import SceneBase
from src.battle.tactical_scene import TacticalScene

from src.rpg.party import Party
from src.rpg.inventory import Inventory
from src.ui.menu_party import PartyMenuUI
from src.ui.menu_inventory import InventoryMenuUI
from src.ui.menu_equipment import EquipmentMenuUI
from src.ui.menu_shop import ShopMenuUI
from src.ui.menu_quests import QuestMenuUI
from src.systems.shop_system import ShopSystem
from src.rpg.quest_log import QuestLog
from src.systems.quest_system import QuestSystem


class TownScene(SceneBase):
    STATE_MAIN = "main"
    STATE_PARTY = "party"
    STATE_INV = "inventory"
    STATE_EQUIP = "equipment"
    STATE_SHOP = "shop"
    STATE_QUEST = "quest"

    def __init__(
        self,
        screen,
        scene_manager,
        content_loader,
        stage_id,
        unlocked_stages,
        game_state=None
    ):
        self.screen = screen
        self.scene_manager = scene_manager
        self.content = content_loader
        self.stage_id = stage_id
        self.unlocked_stages = unlocked_stages
        self.game_state = game_state

        self.font = pygame.font.SysFont("simhei", 24)
        self.small = pygame.font.SysFont("simhei", 18)

        self.options = [
            "查看关卡信息",
            "队伍编成",
            "背包管理",
            "装备更换",
            "商店",
            "任务日志",
            "开始出击",
            "返回世界地图"
        ]

        self.selected = 0
        self.message = "欢迎来到整备营地。"
        self.state = self.STATE_MAIN
        self._option_rects = []

        # 初始化单位
        self.preview_units = self._build_preview_units(stage_id)

        # 队伍
        self.party = Party(max_deploy=3)
        self.party.set_all_members(self.preview_units)
        self.party.deployed_ids = [u.id for u in self.preview_units[:self.party.max_deploy]]

        # 背包与商店：优先使用 game_state 持有对象
        if self.game_state is not None and hasattr(self.game_state, "camp_inventory"):
            self.inventory = self.game_state.camp_inventory
        else:
            self.inventory = Inventory()
            self.inventory.add("potion_s", 3)
            self.inventory.add("antidote", 2)
            self.inventory.add("iron_sword", 1)
            self.inventory.add("iron_lance", 1)
            self.inventory.add("iron_bow", 1)
            self.inventory.add("iron_axe", 1)
            if self.game_state is not None:
                self.game_state.camp_inventory = self.inventory

        if self.game_state is not None and hasattr(self.game_state, "shop_system"):
            self.shop = self.game_state.shop_system
        else:
            self.shop = ShopSystem(initial_gold=1000)
            if self.game_state is not None:
                self.game_state.shop_system = self.shop

        # 任务
        if self.game_state is not None:
            self.quest_log = self.game_state.quest_log
            self.quest_system = self.game_state.quest_system
        else:
            self.quest_log = QuestLog()
            self.quest_system = QuestSystem(self.quest_log)
            self.quest_system.init_default_quests()

        # 子UI
        self.party_ui = PartyMenuUI()
        self.inv_ui = InventoryMenuUI()
        self.equip_ui = EquipmentMenuUI()
        self.shop_ui = ShopMenuUI()
        self.quest_ui = QuestMenuUI()

    def _build_preview_units(self, stage_id):
        stage = self.content.load_stage(stage_id)
        units = []
        if not stage:
            return units

        from src.rpg.unit import Unit
        from src.rpg.stats import Stats

        for u in stage.get("player_units", []):
            jc = self.content.classes[u["class_id"]]
            wp = self.content.weapons[u["weapon_id"]]
            st = u["stats"]
            sp = u["spawn"]
            obj = Unit(
                id=u["id"],
                name=u["name"],
                team="player",
                x=sp[0], y=sp[1],
                job=jc,
                base=Stats(
                    hp=st["hp"], str_=st["str"], mag=st["mag"], skl=st["skl"],
                    spd=st["spd"], lck=st["lck"], def_=st["def"], res=st["res"]
                ),
                weapon=wp
            )
            units.append(obj)
        return units

    def handle_event(self, event):
        if self.state == self.STATE_MAIN:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(self._option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = i
                        break
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = False
                for i, rect in enumerate(self._option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = i
                        clicked = True
                        break
                if not clicked:
                    return
                op = self.options[self.selected]
                if op == "查看关卡信息":
                    self._show_stage_info()
                elif op == "队伍编成":
                    self.state = self.STATE_PARTY
                    self.message = "进入队伍编成。Esc返回。"
                elif op == "背包管理":
                    self.state = self.STATE_INV
                    self.message = "进入背包管理。Esc返回。"
                elif op == "装备更换":
                    self.state = self.STATE_EQUIP
                    self.message = "进入装备更换。Esc返回。"
                elif op == "商店":
                    self.state = self.STATE_SHOP
                    self.message = "进入商店。Esc返回。"
                elif op == "任务日志":
                    self.state = self.STATE_QUEST
                    self.message = "进入任务日志。Esc返回。"
                elif op == "开始出击":
                    self._start_battle()
                elif op == "返回世界地图":
                    self.scene_manager.pop()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                op = self.options[self.selected]
                if op == "查看关卡信息":
                    self._show_stage_info()
                elif op == "队伍编成":
                    self.state = self.STATE_PARTY
                    self.message = "进入队伍编成。Esc返回。"
                elif op == "背包管理":
                    self.state = self.STATE_INV
                    self.message = "进入背包管理。Esc返回。"
                elif op == "装备更换":
                    self.state = self.STATE_EQUIP
                    self.message = "进入装备更换。Esc返回。"
                elif op == "商店":
                    self.state = self.STATE_SHOP
                    self.message = "进入商店。Esc返回。"
                elif op == "任务日志":
                    self.state = self.STATE_QUEST
                    self.message = "进入任务日志。Esc返回。"
                elif op == "开始出击":
                    self._start_battle()
                elif op == "返回世界地图":
                    self.scene_manager.pop()
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = self.STATE_MAIN
            self.message = "返回整备主菜单。"
            return

        if event.type != pygame.KEYDOWN:
            return

        if self.state == self.STATE_PARTY:
            self.party_ui.handle_key(event.key, self.party)
            return

        if self.state == self.STATE_INV:
            self.inv_ui.handle_key(event.key, self.inventory, self.party.all_members)
            return

        if self.state == self.STATE_EQUIP:
            self.equip_ui.handle_key(event.key, self.party.all_members, self.inventory, self.content.weapons)
            return

        if self.state == self.STATE_SHOP:
            before_gold = self.shop.gold
            self.shop_ui.handle_key(event.key, self.shop, self.inventory)
            if self.shop.gold < before_gold:
                self.quest_system.on_shop_buy()
            return

        if self.state == self.STATE_QUEST:
            self.quest_ui.handle_key(event.key, self.quest_log)
            return

    def _show_stage_info(self):
        stage = self.content.load_stage(self.stage_id)
        if not stage:
            self.message = "关卡数据不存在。"
            return
        en = len(stage.get("enemy_units", []))
        pl = len(self.party.deployed_ids)
        name = stage.get("name", self.stage_id)
        self.message = "关卡：%s | 出击人数:%d | 敌军人数:%d" % (name, pl, en)

    def _start_battle(self):
        # 统计启动
        if self.game_state is not None:
            self.game_state.chapter_stats.start_stage(self.stage_id)

        self.scene_manager.push(
            TacticalScene(
                self.screen,
                self.scene_manager,
                logger=None,
                stage_id=self.stage_id,
                content_loader=self.content,
                unlocked_stages=self.unlocked_stages,
                deploy_ids=self.party.deployed_ids,
                external_inventory=self.inventory,
                external_gold=self.shop.gold,
                game_state=self.game_state
            )
        )

    def update(self, dt):
        pass

    def draw(self):
        if self.state == self.STATE_PARTY:
            self.party_ui.draw(self.screen, self.party)
            return

        if self.state == self.STATE_INV:
            self.inv_ui.draw(self.screen, self.inventory)
            return

        if self.state == self.STATE_EQUIP:
            self.equip_ui.draw(self.screen, self.party.all_members, self.inventory, self.content.weapons)
            return

        if self.state == self.STATE_SHOP:
            self.shop_ui.draw(self.screen, self.shop, self.inventory)
            return

        if self.state == self.STATE_QUEST:
            self.quest_ui.draw(self.screen, self.quest_log)
            return

        self.screen.fill((52, 36, 26))

        title = self.font.render("整备营地", True, (255, 230, 120))
        sub = self.small.render("目标章节：%s" % self.stage_id, True, (230, 230, 230))
        self.screen.blit(title, (40, 30))
        self.screen.blit(sub, (40, 66))

        panel = pygame.Rect(40, 110, 560, 430)
        pygame.draw.rect(self.screen, (72, 50, 35), panel)
        pygame.draw.rect(self.screen, (150, 120, 90), panel, 2)

        y = 150
        self._option_rects = []
        for i, op in enumerate(self.options):
            rect = pygame.Rect(56, y - 2, 520, 30)
            self._option_rects.append(rect)
            color = (255, 230, 120) if i == self.selected else (235, 235, 235)
            if i == self.selected:
                pygame.draw.rect(self.screen, (90, 62, 44), rect)
            txt = self.small.render(op, True, color)
            self.screen.blit(txt, (60, y))
            y += 40

        info = pygame.Rect(630, 110, 580, 430)
        pygame.draw.rect(self.screen, (62, 45, 30), info)
        pygame.draw.rect(self.screen, (150, 120, 90), info, 2)

        line1 = self.small.render("上阵人数：%d / %d" % (len(self.party.deployed_ids), self.party.max_deploy), True, (230, 230, 230))
        line2 = self.small.render("金币：%dG" % self.shop.gold, True, (230, 230, 230))
        self.screen.blit(line1, (650, 140))
        self.screen.blit(line2, (650, 170))

        y2 = 220
        self.screen.blit(self.small.render("当前上阵名单：", True, (255, 230, 120)), (650, y2))
        y2 += 30

        dep_set = set(self.party.deployed_ids)
        for u in self.party.all_members:
            if u.id in dep_set:
                row = self.small.render("%s  %s  Lv%d" % (u.name, u.job.name, u.level), True, (230, 230, 230))
                self.screen.blit(row, (650, y2))
                y2 += 28

        msg = self.small.render(self.message, True, (230, 220, 180))
        self.screen.blit(msg, (40, 590))
