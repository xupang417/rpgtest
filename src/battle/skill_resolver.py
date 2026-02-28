import random


def _calc_magic_damage(attacker, defender, power: float):
    atk = int(attacker.mag * power)
    d = atk - defender.res
    return max(0, d)


def _calc_physical_damage(attacker, defender, terrain, power: float):
    atk = int((attacker.str_ + attacker.might) * power)
    d = atk - (defender.def_ + terrain.defense)
    return max(0, d)


def cast_skill(caster, target, skill, terrain):
    """
    返回:
    {
      "ok": bool,
      "text": str,
      "damage": int,
      "heal": int,
      "defeated": bool
    }
    """
    if caster.sp < skill.cost:
        return {"ok": False, "text": f"{caster.name} 技力不足！", "damage": 0, "heal": 0, "defeated": False}

    caster.sp -= skill.cost

    if skill.kind == "heal":
        val = max(1, int((caster.mag + 5) * skill.power))
        before = target.hp
        target.hp = min(target.max_hp, target.hp + val)
        return {
            "ok": True,
            "text": f"{caster.name} 对 {target.name} 施放 {skill.name}，恢复 {target.hp - before} 点生命。",
            "damage": 0,
            "heal": target.hp - before,
            "defeated": False
        }

    if skill.kind == "attack":
        dmg = _calc_magic_damage(caster, target, skill.power)
        # 简化命中（技能固定90）
        if random.randint(1, 100) > 90:
            return {"ok": True, "text": f"{caster.name} 的 {skill.name} 未命中。", "damage": 0, "heal": 0, "defeated": False}
        target.hp -= dmg
        defeated = target.hp <= 0
        if defeated:
            target.hp = 0
            target.alive = False
        return {
            "ok": True,
            "text": f"{caster.name} 使用 {skill.name} 对 {target.name} 造成 {dmg} 点伤害。",
            "damage": dmg,
            "heal": 0,
            "defeated": defeated
        }

    if skill.kind == "attack_status":
        dmg = _calc_physical_damage(caster, target, terrain, skill.power)
        target.hp -= dmg
        defeated = target.hp <= 0
        if defeated:
            target.hp = 0
            target.alive = False
        if (not defeated) and skill.status:
            target.statuses[skill.status] = skill.status_turns
            txt = f"{caster.name} 使用 {skill.name} 造成 {dmg} 伤害，并附加【{skill.status}】{skill.status_turns}回合。"
        else:
            txt = f"{caster.name} 使用 {skill.name} 造成 {dmg} 伤害。"
        return {"ok": True, "text": txt, "damage": dmg, "heal": 0, "defeated": defeated}

    return {"ok": False, "text": f"未知技能类型：{skill.kind}", "damage": 0, "heal": 0, "defeated": False}