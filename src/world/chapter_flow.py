class ChapterFlow:
    """
    章节流程与已完成记录（轻量版）
    """
    def __init__(self):
        self.completed_stages = set()

    def mark_completed(self, stage_id: str):
        self.completed_stages.add(stage_id)

    def is_completed(self, stage_id: str) -> bool:
        return stage_id in self.completed_stages
