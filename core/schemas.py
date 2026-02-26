from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime, time as Time
import enum


class ScheduleType(enum.Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class BaseEvents(BaseModel):
    id: Optional[int] = None
    message: str
    schedule: ScheduleType
    date: Optional[datetime] = None
    time: Optional[Time] = None
    day_of_week: Optional[int] = Field(None, ge=0, le=6)
    dd: Optional[int] = Field(None, ge=1, le=31)
    mm_dd: Optional[str] = Field(None, pattern=r"^\d{2}-\d{2}$")

    @model_validator(mode="after")
    def validate_schedule_fields(self):
        "Validate that the required field is not None"
        required = {
            ScheduleType.ONCE: "date",
            ScheduleType.DAILY: "time",
            ScheduleType.WEEKLY: "day_of_week",
            ScheduleType.MONTHLY: "dd",
            ScheduleType.YEARLY: "mm_dd",
        }
        field = required[self.schedule]
        if getattr(self, field) is None:
            raise ValueError(f"'{field}' is required when schedule is '{self.schedule}'")
        return self
