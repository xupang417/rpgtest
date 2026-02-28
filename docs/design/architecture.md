# 项目架构（当前可运行形态）

## 场景流程

1. WorldMapScene（世界地图）
2. TownScene（整备营地）
3. TacticalScene（战棋战斗）
4. 战斗结算（BattleResultPanel）后返回 TownScene

## 整备营地模块

- 队伍编成：Party + PartyMenuUI
- 背包管理：Inventory + InventoryMenuUI
- 装备更换：EquipmentMenuUI
- 商店系统：ShopSystem + ShopMenuUI

## 战斗奖励闭环

- RewardSystem 产出金币/道具
- BattleResultPanel 显示
- 回写到整备层（背包/金币）

## 下一步建议

- 将 external_gold 改为传 ShopSystem 实例
- 在战斗中读取整备阶段装备后的武器
- 增加任务系统 UI 并在章节完成时更新状态
