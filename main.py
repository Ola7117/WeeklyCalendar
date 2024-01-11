from calendar import day_name, month_name
from datetime import date, datetime, timedelta, timezone
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU, relativedelta
from icalendar import Calendar
from os.path import isfile
from tkinter import *
from tkinter import filedialog, scrolledtext
from tzlocal import get_localzone


def display_calendar(file_path):
    file = open(file_path, 'rb')
    calendar = Calendar.from_ical(file.read())
    events = []

    for i in range(7):
        events.append([])

    for component in calendar.walk():
        if component.name == 'VEVENT':
            event_info, start_date = get_event_info(component)

            for i in range(7):
                find_events_this_week(start_date, events, event_info, i)

    for i in range(7):
        for j in range(len(events[i])):
            if events[i][j][3] != '':
                events = split_multiple_day_events(events, i, j)
        textboxes[i].config(state=NORMAL)

    for i in range(7):
        events[i].sort()
        for j in range(len(events[i])):
            textboxes[i].insert(END, events[i][j][0] + '-' + events[i][j][1] + '\n', 'normal')
            textboxes[i].insert(END, events[i][j][2] + '\n', 'bold')
        textboxes[i].config(state=DISABLED)

    file.close()


def find_events_this_week(start_date, events, event_info, weekday_nr):
    weekday_abbr = [MO, TU, WE, TH, FR, SA, SU]
    today = date.today()
    if today.weekday() > weekday_nr:
        if start_date == str(today + relativedelta(weekday=weekday_abbr[weekday_nr](-1))):
            events[weekday_nr].append(event_info)
        elif (date.fromisoformat(start_date).isocalendar().week != today.isocalendar().week and
              event_info[3] == str(today + relativedelta(weekday=weekday_abbr[weekday_nr](-1)))):
            event_info[0] = '00:00'
            events[0].append(event_info)
    elif today.weekday() <= weekday_nr:
        if start_date == str(today + relativedelta(weekday=weekday_nr)):
            events[weekday_nr].append(event_info)
        elif (date.fromisoformat(start_date).isocalendar().week != today.isocalendar().week and
              event_info[3] == str(today + relativedelta(weekday=weekday_nr))):
            event_info[0] = '00:00'
            events[0].append(event_info)


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
        if str(component.get('summary')) == 'Narty':
            print(end[:10])
            print(str(date.fromisoformat(start[:10]) + relativedelta(days=+1)))
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

    event_info = [start_time, end_time, event_name, '']

    if start_date != end_date:
        event_info[3] = end_date

    return event_info, start_date


def initialize_window():
    window = Tk()
    window.title('Weekly Calendar')
    window.resizable(False, False)
    blue = '#b3e6ff'
    light_blue = '#e6f7ff'
    dark_blue = '#005580'
    window.configure(bg=blue)

    day_numbers, today = update_day_numbers()

    weekdays = ()
    days = ()
    text = ()
    left = 5
    right = 5

    for i in range(7):
        if day_name[i] != today.strftime('%A'):
            weekdays = weekdays + (Label(bg=blue, font=('Arial', 12), text=day_name[i]),)
        else:
            weekdays = weekdays + (Label(bg=blue, fg=dark_blue, font=('Arial', 12, 'bold'), text=day_name[i]),)

        if str(day_numbers[i]) != str(today.day):
            days = days + (Label(bg=blue, font=('Arial', 12), text=day_numbers[i]),)
        else:
            days = days + (Label(bg=blue, fg=dark_blue, font=('Arial', 12, 'bold'), text=day_numbers[i]),)

        text = text + (scrolledtext.ScrolledText(bg=light_blue, height=10, width=30),)

        if i < 4:
            if i == 0:
                left = 10
            elif i == 3:
                right = 10

            weekdays[i].grid(row=0, column=i * 2, sticky=W, padx=(left, 5), pady=(10, 5))
            days[i].grid(row=0, column=i * 2 + 1, sticky=E, padx=(5, right), pady=(10, 5))
            text[i].grid(row=1, column=i * 2, columnspan=2, padx=(left, right), pady=(5, 5))

        else:
            if i == 4:
                left = 10
            elif i == 6:
                right = 10

            weekdays[i].grid(row=2, column=(i - 4) * 2, sticky=W, padx=(left, 5), pady=(5, 5))
            days[i].grid(row=2, column=(i - 4) * 2 + 1, sticky=E, padx=(5, right), pady=(5, 5))
            text[i].grid(row=3, column=(i - 4) * 2, rowspan=3, columnspan=2, padx=(left, right), pady=(5, 10))

        text[i].tag_configure('normal', font=('Arial', 10))
        text[i].tag_configure('bold', font=('Arial', 10, 'bold'))
        text[i].config(state=DISABLED)

    label_title = Label(bg=blue, font=('Arial', 16), text='Weekly Calendar')
    label_title.grid(row=3, column=6, columnspan=2, padx=10, pady=10)
    label_title.configure()

    month = month_name[date.today().month]
    year = date.today().year

    label_month = Label(bg=blue, font=('Arial', 12), text=str(month) + ' ' + str(year))
    label_month.grid(row=4, column=6, columnspan=2, padx=10, pady=10)

    button = Button(
        window,
        bg=light_blue,
        command=open_file,
        font=('Arial', 10),
        text='Open an ICS file',
    )
    button.grid(row=5, column=6, columnspan=2, padx=10, pady=10)

    return window, text


def load():
    if isfile('saved_file_path.txt'):
        saved_file_path = open('saved_file_path.txt', 'r')
        file_path = saved_file_path.read()

        if file_path != '':
            display_calendar(file_path)

        saved_file_path.close()


def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=(('iCalendar', '*.ics'),),
        title='Open'
    )

    if file_path != '':
        save(file_path)

        for i in range(7):
            textboxes[i].config(state=NORMAL)
            textboxes[i].delete('1.0', END)

        display_calendar(file_path)


def save(file_path):
    saved_file_path = open('saved_file_path.txt', 'w')
    saved_file_path.write(file_path)
    saved_file_path.close()


def split_multiple_day_events(events, weekday_nr, event_nr):
    day_start = weekday_nr
    day_end = (datetime.fromisoformat(events[weekday_nr][event_nr][3])).weekday()
    parts = abs(day_end - day_start + 1)

    if parts > 1:
        part_first = [events[weekday_nr][event_nr][0], '23:59',
                      events[weekday_nr][event_nr][2], '']
        if parts > 2:
            for i in range(1, parts - 1):
                if (weekday_nr + i) < 7:
                    part_middle = ['00:00', '23:59',
                                   events[weekday_nr][event_nr][2], '']
                    events[weekday_nr + i].append(part_middle)
        if (weekday_nr + parts - 1) < 7:
            part_last = ['00:00', events[weekday_nr][event_nr][1],
                         events[weekday_nr][event_nr][2], '']
            events[weekday_nr + parts - 1].append(part_last)
    else:
        part_first = events[weekday_nr][event_nr]

    events[weekday_nr][event_nr] = part_first

    return events


def update_day_numbers():
    day_numbers = [0] * 7
    weekday_abbr = [MO, TU, WE, TH, FR, SA, SU]
    today = date.today()

    for i in range(7):
        if today.weekday() > i:
            day_numbers[i] = str(today + relativedelta(weekday=weekday_abbr[i](-1)))[8:11]
        else:
            day_numbers[i] = str(today + relativedelta(weekday=i))[8:11]

    return day_numbers, today


if __name__ == '__main__':
    program, textboxes = initialize_window()
    load()
    program.mainloop()
