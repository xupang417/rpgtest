class ClassChangeMenu:
    def __init__(self):
        self.unit_index = 0
        self.rule_index = 0
        self.message = "↑↓选择角色，←→选择转职路线，回车确认，Esc返回。"
        self._units = []
        self._promotions = []
        self._classes = {}
        self._skills = {}
        self._inventory = None

    def open(self, units, promotions, classes, skills, inventory):
        self._units = units or []
        self._promotions = promotions or []
        self._classes = classes or {}
        self._skills = skills or {}
        self._inventory = inventory
        self.unit_index = 0
        self.rule_index = 0

    def handle_key(self, key):
        if not self._units:
            self.message = "当前没有可转职角色。"
            return
        import pygame
        from src.rpg.promotion_system import find_promotion_option, do_promote

        if key == pygame.K_UP:
            self.unit_index = (self.unit_index - 1) % len(self._units)
            self.rule_index = 0
        elif key == pygame.K_DOWN:
            self.unit_index = (self.unit_index + 1) % len(self._units)
            self.rule_index = 0
        else:
            unit = self._units[self.unit_index]
            options = find_promotion_option(unit, self._promotions)
            if not options:
                self.message = f"{unit.name} 当前不可转职。"
                return
            if key == pygame.K_LEFT:
                self.rule_index = (self.rule_index - 1) % len(options)
            elif key == pygame.K_RIGHT:
                self.rule_index = (self.rule_index + 1) % len(options)
            elif key in (pygame.K_RETURN, pygame.K_SPACE):
                ok, msg = do_promote(
                    unit,
                    options[self.rule_index],
                    self._classes,
                    self._skills,
                    self._inventory,
                )
                self.message = msg

    def draw(self, screen):
        import pygame
        from src.rpg.promotion_system import find_promotion_option

        font = pygame.font.SysFont("simhei", 24)
        small = pygame.font.SysFont("simhei", 18)
        screen.fill((32, 28, 40))
        screen.blit(font.render("职业转职", True, (255, 230, 120)), (36, 30))

        y = 90
        for i, unit in enumerate(self._units):
            color = (255, 230, 120) if i == self.unit_index else (230, 230, 230)
            txt = f"{unit.name}  {unit.job.name}  Lv{unit.level}"
            screen.blit(small.render(txt, True, color), (40, y))
            y += 28

        if self._units:
            unit = self._units[self.unit_index]
            options = find_promotion_option(unit, self._promotions)
            screen.blit(small.render("可选路线：", True, (220, 220, 220)), (500, 90))
            oy = 120
            for i, r in enumerate(options):
                color = (255, 230, 120) if i == self.rule_index else (230, 230, 230)
                need = r.get("need_item", "无")
                txt = f"{r['from']} -> {r['to']}  需求道具:{need}"
                screen.blit(small.render(txt, True, color), (500, oy))
                oy += 28

        screen.blit(small.render(self.message, True, (220, 220, 220)), (36, 650))
