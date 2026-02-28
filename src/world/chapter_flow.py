class ChapterFlow:
    """
    章节流程与已完成记录（轻量版）
    """
    def __init__(self):
        self.completed_stages = []

    def mark_completed(self, stage_id: str):
        if stage_id not in self.completed_stages:
            self.completed_stages.append(stage_id)

    def is_completed(self, stage_id: str) -> bool:
        return stage_id in self.completed_stages
