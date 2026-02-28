def find_promotion_option(unit, promotion_rules: list[dict]):
    """
    返回可用转职规则 list（可能多个）
    """
    opts = []
    for r in promotion_rules:
        if r["from"] == unit.job.id and unit.level >= r["need_level"]:
            opts.append(r)
    return opts


def can_promote(unit, rule: dict, inventory) -> tuple[bool, str]:
    if unit.job.id != rule["from"]:
        return False, "当前职业不符合转职条件。"
    if unit.level < rule["need_level"]:
        return False, f"等级不足，需要Lv{rule['need_level']}。"
    item_id = rule.get("need_item")
    if item_id and not inventory.has(item_id, 1):
        return False, f"缺少转职道具：{item_id}。"
    return True, "可转职"


def do_promote(unit, rule: dict, classes: dict, skills: dict, inventory):
    ok, msg = can_promote(unit, rule, inventory)
    if not ok:
        return False, msg

    to_class_id = rule["to"]
    if to_class_id not in classes:
        return False, f"目标职业不存在：{to_class_id}"

    # 消耗道具
    need_item = rule.get("need_item")
    if need_item:
        if not inventory.consume(need_item, 1):
            return False, "道具消耗失败。"

    # 切职业
    unit.job = classes[to_class_id]

    # 属性加成
    bonus = rule.get("bonus", {})
    unit.max_hp += bonus.get("hp", 0)
    unit.hp = min(unit.max_hp, unit.hp + bonus.get("hp", 0))
    unit.base.str_ += bonus.get("str", 0)
    unit.base.mag += bonus.get("mag", 0)
    unit.base.skl += bonus.get("skl", 0)
    unit.base.spd += bonus.get("spd", 0)
    unit.base.lck += bonus.get("lck", 0)
    unit.base.def_ += bonus.get("def", 0)
    unit.base.res += bonus.get("res", 0)

    # 学技能
    for sid in rule.get("learn_skills", []):
        sk = skills.get(sid)
        if sk and all(old.id != sid for old in unit.skills):
            unit.skills.append(sk)

    return True, f"{unit.name} 已转职为【{unit.job.name}】！"
