from datetime import date, datetime, timedelta, timezone
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU, relativedelta
from icalendar import Calendar
from tzlocal import get_localzone


def build_week_events(ical_bytes, selected_date):
    calendar = Calendar.from_ical(ical_bytes)

    events = [[] for _ in range(7)]

    for component in calendar.walk():
        if component.name == 'VEVENT':
            event_info, start_date = get_event_info(component)

            is_all_week_event = False
            for i in range(7):
                is_all_week_event = find_events_this_week(
                    start_date, events, event_info, i, is_all_week_event, selected_date
                )

    for i in range(7):
        for j in range(len(events[i])):
            if events[i][j][3] != '':
                events = split_multiple_day_events(events, i, j)

        events[i].sort()

    return events


def find_events_this_week(start_date, events, event_info, weekday_nr, is_all_week_event, selected_date):
    weekday_abbr = [MO, TU, WE, TH, FR, SA, SU]
    if (date.fromisoformat(start_date) < selected_date + relativedelta(weekday=MO(-1)) and
            date.fromisoformat(event_info[3]) > selected_date + relativedelta(weekday=SU(1)) and is_all_week_event is False):
        event_info = ['00:00', '23:59', event_info[2], str(selected_date + relativedelta(weekday=SU(1)))]
        events[0].append(event_info)
        is_all_week_event = True
    elif selected_date.weekday() > weekday_nr:
        if start_date == str(selected_date + relativedelta(weekday=weekday_abbr[weekday_nr](-1))):
            events[weekday_nr].append(event_info)
        elif (date.fromisoformat(start_date).isocalendar().week != selected_date.isocalendar().week and
              event_info[3] == str(selected_date + relativedelta(weekday=weekday_abbr[weekday_nr](-1)))):
            event_info[0] = '00:00'
            events[0].append(event_info)
    elif selected_date.weekday() <= weekday_nr:
        if start_date == str(selected_date + relativedelta(weekday=weekday_nr)):
            events[weekday_nr].append(event_info)
        elif (date.fromisoformat(start_date).isocalendar().week != selected_date.isocalendar().week and
              event_info[3] == str(selected_date + relativedelta(weekday=weekday_nr))):
            event_info[0] = '00:00'
            events[0].append(event_info)
    return is_all_week_event


def get_event_info(component):
    start = str(component.get('dtstart'))[10:26]
    end = str(component.get('dtend'))[10:26]

    local_timezone = get_localzone()

    if not (start[10] == ',' and end[10] == ','):
        start = datetime.fromisoformat(start)
        start = start.replace(tzinfo=timezone.utc)
        start_local = start.astimezone(local_timezone)
        end = datetime.fromisoformat(end)
        end = end.replace(tzinfo=timezone.utc)
        end_local = end.astimezone(local_timezone)
    else:
        start = start.replace(start, start[:10] + ' 00:00')
        start_local = start
        if end[:10] == str(date.fromisoformat(start[:10]) + relativedelta(days=+1)):
            end = end.replace(end, start[:10] + ' 23:59')
        else:
            day_before_end = str(date.fromisoformat(end[:10]) + relativedelta(days=-1))
            end = end.replace(end, day_before_end + ' 23:59')
        end_local = end

    start_date = str(start_local)[:10]
    start_time = str(start_local)[11:16]
    end_date = str(end_local)[:10]
    end_time = str(end_local)[11:16]

    if end_time == '00:00':
        end_date = str(date.fromisoformat(end_date) - timedelta(days=1))

    event_name = str(component.get('summary'))

    event_info = [start_time, end_time, event_name, end_date]

    # if start_date != end_date:
    #     event_info[3] = end_date

    return event_info, start_date


def split_multiple_day_events(events, weekday_nr, event_nr):
    end_date = date.fromisoformat(events[weekday_nr][event_nr][3])

    day_start = weekday_nr
    day_end = end_date.weekday()

    if day_end >= day_start:
        parts = day_end - day_start + 1
    else:
        parts = 7 - day_start

    if parts > 1:
        part_first = [events[weekday_nr][event_nr][0], '23:59', events[weekday_nr][event_nr][2], '']
        if parts > 2:
            for i in range(1, parts - 1):
                if (weekday_nr + i) < 7:
                    part_middle = ['00:00', '23:59', events[weekday_nr][event_nr][2], '']
                    events[weekday_nr + i].append(part_middle)
        if day_end >= day_start:
            part_last = ['00:00', events[weekday_nr][event_nr][1], events[weekday_nr][event_nr][2], '']
        else:
            part_last = ['00:00', '23:59', events[weekday_nr][event_nr][2], '']
        events[weekday_nr + parts - 1].append(part_last)
    else:
        part_first = events[weekday_nr][event_nr]

    events[weekday_nr][event_nr] = part_first

    return events