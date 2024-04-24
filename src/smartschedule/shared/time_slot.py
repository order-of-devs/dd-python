from __future__ import annotations


from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True)
class TimeSlot:
    start: datetime
    end: datetime

    @staticmethod
    def empty() -> TimeSlot:
        return TimeSlot(
            datetime.min.replace(tzinfo=timezone.utc),
            datetime.min.replace(tzinfo=timezone.utc)
        )

    @staticmethod
    def create_daily_slot_at_utc(year: int, month: int, day: int) -> TimeSlot:
        return TimeSlot.create_slot_at_utc_of_duration(year, month, day, timedelta(days=1))

    @staticmethod
    def create_slot_at_utc_of_duration(year: int, month: int, day: int, duration: timedelta) -> TimeSlot:
        start = datetime(year, month, day, tzinfo=timezone.utc)
        return TimeSlot(start, start + duration)

    @staticmethod
    def create_monthly_slot_at_utc(year: int, month: int) -> TimeSlot:
        start = datetime(year, month, 1, tzinfo=timezone.utc)
        end = datetime(year, month+1, 1, tzinfo=timezone.utc) if month < 12 else datetime(year+1, 1, 1, tzinfo=timezone.utc)
        return TimeSlot(start, end)

    def overlaps_with(self, other: TimeSlot) -> bool:
        return self.start < other.end and self.end > other.start

    def is_within(self, other: TimeSlot) -> bool:
        return self.start >= other.start and self.end <= other.end

    def leftover_after_removing_common_with(self, other: TimeSlot) -> list[TimeSlot]:
        if other == self:
            return []
        if not self.overlaps_with(other):
            return [self, other]
        if self.start < other.start:
            yield TimeSlot(self.start, other.start)
        if other.start < self.start:
            yield TimeSlot(other.start, self.start)
        if self.end > other.end:
            yield TimeSlot(other.end, self.end)
        if other.end > self.end:
            yield TimeSlot(self.end, other.end)

    def common_part_with(self, other: TimeSlot) -> TimeSlot:
        if not self.overlaps_with(other):
            return TimeSlot.empty()
        return TimeSlot(max(self.start, other.start), min(self.end, other.end))

    def is_empty(self) -> bool:
        return self.start == self.end

    def duration(self) -> timedelta:
        return self.end - self.start

    def stretch(self, duration: timedelta) -> TimeSlot:
        return TimeSlot(self.start - duration, self.end + duration)
