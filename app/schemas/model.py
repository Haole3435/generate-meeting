from pydantic import BaseModel
from typing import List

class MeetingMinutes(BaseModel):
    transcription: str
    general_summary: str
    abstract_summary: str
    key_points: List[str]
    action_items: List[str]
    sentiment: str


class MeetingMinutesResponse(MeetingMinutes):
    download_url: str