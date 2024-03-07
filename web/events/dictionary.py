"""
This module contains the dictionary of events.
"""
# Event Status
EVENT_STATUS = [
    ("open", "Open"),
    ("closed", "Closed"),
    ("canceled", "Canceled"),
    ("completed", "Completed"),
]

# Attendee Status
ATTENDEE_STATUS = [
    ("pending", "Pending"),
    ("accepted", "Accepted"),
    ("confirmed", "Confirmed"),
    ("declined", "Declined"),
    ("standby", "Standby"),
]

# Timezones
TIMEZONES = [
    ("US/Alaska", "US/Alaska (-08:00AKDT)"),
    ("US/Aleutian", "US/Aleutian (-09:00HDT)"),
    ("US/Arizona", "US/Arizona (-07:00MST)"),
    ("US/Central", "US/Central (-05:00CDT)"),
    ("US/East-Indiana", "US/East-Indiana (-04:00EDT)"),
    ("US/Eastern", "US/Eastern (-04:00EDT)"),
    ("US/Hawaii", "US/Hawaii (-10:00HST)"),
    ("US/Indiana-Starke", "US/Indiana-Starke (-05:00CDT)"),
    ("US/Michigan", "US/Michigan (-04:00EDT)"),
    ("US/Mountain", "US/Mountain (-06:00MDT)"),
    ("US/Pacific", "US/Pacific (-07:00PDT)"),
    ("US/Samoa", "US/Samoa (-11:00SST)"),
    ("UTC", "UTC (+00:00UTC)"),
]
