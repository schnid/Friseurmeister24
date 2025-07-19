from datetime import datetime
import caldav
from icalendar import Calendar, Event


class CalDavManager:
    def __init__(self, url: str, username: str, password: str):
        self.client = caldav.DAVClient(url, username=username, password=password)
        self.principal = self.client.principal()
        calendars = self.principal.calendars()
        self.calendar = calendars[0] if calendars else None

    def create_event(self, summary: str, start_dt: datetime, end_dt: datetime) -> None:
        if not self.calendar:
            raise RuntimeError("No calendar found")

        cal = Calendar()
        event = Event()
        event.add('summary', summary)
        event.add('dtstart', start_dt)
        event.add('dtend', end_dt)
        cal.add_component(event)
        self.calendar.add_event(cal.to_ical())

    def find_event(self, booking_id: str):
        if not self.calendar:
            return None
        results = self.calendar.date_search(datetime.now(), datetime.now().replace(year=datetime.now().year + 1))
        for ev in results:
            if booking_id in ev.vobject_instance.vevent.summary.value:
                return ev
        return None

    def delete_event(self, event) -> None:
        event.delete()
