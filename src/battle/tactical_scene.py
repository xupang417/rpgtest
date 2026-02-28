import pygame
from src.core.scene_manager import SceneBase
from src.battle.grid import GridMap
from src.battle.pathfinding import reachable_tiles, manhattan
from src.battle.combat_system import resolve_basic_attack
from src.ui.action_menu import ActionMenu
from src.rpg.unit import Unit
from src.rpg.stats import Stats


class TacticalScene(SceneBase):
    TILE_SIZE = 64

    def __init__(
        self,
        screen,
        scene_manager,
        logger,
        stage_id,
        content_loader,
        unlocked_stages,
        deploy_ids=None,
        external_inventory=None,
        external_gold=0,
        game_state=None,
    ):
        self.screen = screen
        self.scene_manager = scene_manager
        self.logger = logger
        self.stage_id = stage_id
        self.content = content_loader
        self.unlocked_stages = unlocked_stages
        self.game_state = game_state

        self.font = pygame.font.SysFont("simhei", 22)
        self.small = pygame.font.SysFont("simhei", 18)
        self.action_menu = ActionMenu(self.font, self.small)

        stage = self.content.load_stage(stage_id)
        map_data = stage.get("map", {})
        self.grid = GridMap(map_data.get("width", 12), map_data.get("height", 8))
        self.grid.apply_terrain_overrides(map_data.get("terrain_overrides", []))

        self.players = self._build_units(stage.get("player_units", []), "player", deploy_ids)
        self.enemies = self._build_units(stage.get("enemy_units", []), "enemy")

        self.turn_count = 1
        self.phase = "player"
        self.message = "玩家回合：鼠标左键选择/移动，右键取消。"

        self.selected_unit = None
        self.reachable = set()
        self.moved_unit = None
        self.pending_attack_targets = []
        self.game_finished = False

    def _build_units(self, entries, team, deploy_ids=None):
        result = []
        deploy = set(deploy_ids or [])
        for entry in entries:
            if team == "player" and deploy and entry["id"] not in deploy:
                continue
            job = self.content.classes[entry["class_id"]]
            weapon = self.content.weapons[entry["weapon_id"]]
            s = entry["stats"]
            unit = Unit(
                id=entry["id"],
                name=entry["name"],
                team=team,
                x=entry["spawn"][0],
                y=entry["spawn"][1],
                job=job,
                base=Stats(
                    hp=s["hp"],
                    str_=s["str"],
                    mag=s["mag"],
                    skl=s["skl"],
                    spd=s["spd"],
                    lck=s["lck"],
                    def_=s["def"],
                    res=s["res"],
                ),
                weapon=weapon,
            )
            result.append(unit)
        return result

    def _alive(self, units):
        return [u for u in units if u.alive]

    def _tile_to_pos(self, tx, ty):
        return tx * self.TILE_SIZE, ty * self.TILE_SIZE

    def _mouse_to_tile(self, pos):
        tx = pos[0] // self.TILE_SIZE
        ty = pos[1] // self.TILE_SIZE
        if self.grid.in_bounds(tx, ty):
            return tx, ty
        return None

    def _unit_at(self, tx, ty):
        for u in self._alive(self.players) + self._alive(self.enemies):
            if u.x == tx and u.y == ty:
                return u
        return None

    def _occupied_except(self, unit):
        occupied = set()
        for u in self._alive(self.players) + self._alive(self.enemies):
            if u is unit:
                continue
            occupied.add((u.x, u.y))
        return occupied

    def _in_attack_range(self, attacker, defender):
        d = manhattan(attacker.x, attacker.y, defender.x, defender.y)
        return attacker.range_min <= d <= attacker.range_max

    def _open_action_menu(self):
        x, y = self._tile_to_pos(self.moved_unit.x, self.moved_unit.y)
        options = ["待机", "取消"]
        targets = [e for e in self._alive(self.enemies) if self._in_attack_range(self.moved_unit, e)]
        self.pending_attack_targets = targets
        if targets:
            options = ["攻击", "待机", "取消"]
        self.action_menu.open(x + 8, y + 8, options)

    def _finish_player_action(self, unit):
        unit.acted = True
        self.selected_unit = None
        self.reachable = set()
        self.moved_unit = None
        self.action_menu.close()
        if all(u.acted for u in self._alive(self.players)):
            self._start_enemy_phase()

    def _cancel_selection(self):
        self.selected_unit = None
        self.reachable = set()
        self.message = "已取消选择。"

    def _start_enemy_phase(self):
        self.phase = "enemy"
        self.selected_unit = None
        self.reachable = set()
        self.action_menu.close()
        self.message = "敌人回合中..."
        self._run_enemy_turn()
        if not self.game_finished:
            self.phase = "player"
            self.turn_count += 1
            for unit in self._alive(self.players):
                unit.acted = False
            self.message = "玩家回合开始。"

    def _run_enemy_turn(self):
        for enemy in self._alive(self.enemies):
            targets = self._alive(self.players)
            if not targets:
                self._end_battle(victory=False)
                return
            in_range = [p for p in targets if self._in_attack_range(enemy, p)]
            if in_range:
                in_range.sort(key=lambda u: u.hp)
                target = in_range[0]
                td = self.grid.tile_def(target.x, target.y)
                resolve_basic_attack(enemy, target, td)
                continue
            target = min(targets, key=lambda u: manhattan(enemy.x, enemy.y, u.x, u.y))
            candidates = list(self.grid.neighbors4(enemy.x, enemy.y))
            candidates.sort(key=lambda p: manhattan(p[0], p[1], target.x, target.y))
            occupied = {(u.x, u.y) for u in self._alive(self.players) + self._alive(self.enemies) if u is not enemy}
            for nx, ny in candidates:
                if (nx, ny) in occupied:
                    continue
                enemy.x, enemy.y = nx, ny
                break

        if not self._alive(self.players):
            self._end_battle(victory=False)
        elif not self._alive(self.enemies):
            self._end_battle(victory=True)

    def _end_battle(self, victory: bool):
        self.game_finished = True
        if victory:
            next_stage = self.content.get_next_stage(self.stage_id)
            target_unlock = self.game_state.unlocked_stages if self.game_state else self.unlocked_stages
            if next_stage and next_stage not in target_unlock:
                target_unlock.append(next_stage)

            self.scene_manager.pop()
            if next_stage:
                from src.world.town_scene import TownScene

                self.scene_manager.replace(
                    TownScene(
                        self.screen,
                        self.scene_manager,
                        content_loader=self.content,
                        stage_id=next_stage,
                        unlocked_stages=target_unlock,
                        game_state=self.game_state,
                    )
                )
            return

        self.scene_manager.pop()

    def handle_event(self, event):
        if self.game_finished or self.phase != "player":
            return
        if event.type == pygame.MOUSEMOTION:
            self.action_menu.handle_mouse_move(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._on_left_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.action_menu.close()
            self._cancel_selection()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self._start_enemy_phase()

    def _on_left_click(self, pos):
        if self.action_menu.visible:
            action = self.action_menu.handle_mouse_click(pos)
            if action == "攻击" and self.pending_attack_targets:
                self.pending_attack_targets.sort(key=lambda u: u.hp)
                target = self.pending_attack_targets[0]
                td = self.grid.tile_def(target.x, target.y)
                resolve_basic_attack(self.moved_unit, target, td)
                self._finish_player_action(self.moved_unit)
                if not self._alive(self.enemies):
                    self._end_battle(victory=True)
            elif action in ("待机", "取消"):
                self._finish_player_action(self.moved_unit)
            return

        tile = self._mouse_to_tile(pos)
        if not tile:
            return
        tx, ty = tile

        if self.selected_unit and (tx, ty) in self.reachable:
            self.selected_unit.x = tx
            self.selected_unit.y = ty
            self.moved_unit = self.selected_unit
            self.selected_unit = None
            self.reachable = set()
            self._open_action_menu()
            return

        unit = self._unit_at(tx, ty)
        if unit and unit.team == "player" and unit.alive and not unit.acted:
            self.selected_unit = unit
            self.reachable = reachable_tiles(
                unit.x,
                unit.y,
                unit.job.move,
                self.grid,
                self._occupied_except(unit),
            )
            self.message = "已选择 %s" % unit.name

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((18, 24, 32))
        for y in range(self.grid.h):
            for x in range(self.grid.w):
                td = self.grid.tile_def(x, y)
                rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                pygame.draw.rect(self.screen, td.color, rect)
                pygame.draw.rect(self.screen, (45, 45, 45), rect, 1)

        for (x, y) in self.reachable:
            rect = pygame.Rect(x * self.TILE_SIZE + 8, y * self.TILE_SIZE + 8, self.TILE_SIZE - 16, self.TILE_SIZE - 16)
            pygame.draw.rect(self.screen, (80, 160, 240), rect, 2)

        for unit in self._alive(self.players):
            px, py = self._tile_to_pos(unit.x, unit.y)
            color = (80, 130, 255) if not unit.acted else (100, 100, 150)
            pygame.draw.circle(self.screen, color, (px + 32, py + 32), 20)
            self.screen.blit(self.small.render(unit.name[0], True, (255, 255, 255)), (px + 24, py + 20))
        for unit in self._alive(self.enemies):
            px, py = self._tile_to_pos(unit.x, unit.y)
            pygame.draw.circle(self.screen, (220, 90, 90), (px + 32, py + 32), 20)
            self.screen.blit(self.small.render(unit.name[0], True, (255, 255, 255)), (px + 24, py + 20))

        self.action_menu.draw(self.screen)
        info_rect = pygame.Rect(0, self.grid.h * self.TILE_SIZE, self.screen.get_width(), 64)
        pygame.draw.rect(self.screen, (24, 24, 40), info_rect)
        pygame.draw.rect(self.screen, (95, 95, 130), info_rect, 2)
        txt = "回合:%d 阶段:%s  %s" % (self.turn_count, self.phase, self.message)
        self.screen.blit(self.small.render(txt, True, (235, 235, 235)), (12, info_rect.y + 20))

