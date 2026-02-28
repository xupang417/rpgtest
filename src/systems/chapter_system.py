class ChapterSystem:
    """
    章节推进系统
    """
    def __init__(self):
        self.current_chapter = 1
        self.cleared_stages = []

    def mark_stage_cleared(self, stage_id: str):
        if stage_id not in self.cleared_stages:
            self.cleared_stages.append(stage_id)

    def try_advance_chapter(self):
        # 示例：清完前两关后升到第2章
        if "ch01_battle_01" in self.cleared_stages and "ch02_battle_01" in self.cleared_stages:
            self.current_chapter = max(self.current_chapter, 2)
            return True, "已推进到第2章。"
        return False, "章节推进条件未满足。"