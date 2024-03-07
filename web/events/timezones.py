"""Timezone conversion for the event model"""
import pytz
from datetime import datetime

timezones = []
for tz in pytz.all_timezones:
    # Get the current time in this timezone
    now = datetime.now(pytz.timezone(tz))

    # Format the timezone offset
    offset_hours = now.strftime('%z')
    offset_minutes = now.strftime('%Z')
    offset = f"{offset_hours[:-2]}:{offset_hours[-2:]}{offset_minutes}"

    # Format the timezone name
    tz_name = f"{tz} ({offset})"

    # Add the timezone and offset to the list
    timezones.append((tz, tz_name))

print(timezones)
