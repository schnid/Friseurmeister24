import uuid
from datetime import datetime, timedelta

from caldav_manager import CalDavManager


class AppointmentManager:
    """Handle booking logic and interaction with CalDAV."""

    def __init__(self, caldav_manager: CalDavManager):
        self.caldav = caldav_manager

    def book_appointment(self, service: str, start_dt: datetime) -> str:
        end_dt = start_dt + timedelta(minutes=30)
        booking_id = str(uuid.uuid4())[:8]
        summary = f"{service} ({booking_id})"
        self.caldav.create_event(summary, start_dt, end_dt)
        return booking_id

    def cancel_appointment(self, booking_id: str) -> bool:
        event = self.caldav.find_event(booking_id)
        if event:
            self.caldav.delete_event(event)
            return True
        return False
