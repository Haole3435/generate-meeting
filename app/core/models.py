from pydantic import BaseModel
from typing import List, Optional

class MeetingContent(BaseModel):
    raw_text: str
    file_path: Optional[str] = None
    media_type: str  # audio/text/video

class ProcessedMeeting(BaseModel):
    abstract_summary: str
    key_points: List[str]
    action_items: List[str]
    sentiment: str
    raw_data: MeetingContent