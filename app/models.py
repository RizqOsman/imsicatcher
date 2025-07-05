from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IMSIRecord(BaseModel):
    imsi: str
    timestamp: datetime
    signal_strength: Optional[float] = None
    estimated_distance: Optional[float] = None

class IMSIBlacklistEntry(BaseModel):
    imsi: str
    label: Optional[str] = None

class IMSIStats(BaseModel):
    total: int
    average_signal: Optional[float]
    top_imsis: list[str]