from calendar import day_name, month_name
from datetime import date, datetime, time
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU, relativedelta
from icalendar import Calendar
from os.path import isfile
from tkinter import *
from tkinter import filedialog


def display_calendar(file_path):
    file = open(file_path, 'rb')
    calendar = Calendar.from_ical(file.read())
    events = []

    for i in range(7):
        events.append([])

    for component in calendar.walk():
        if component.name == 'VEVENT':
            event_info, date_start = get_event_info(component)

            for i in range(7):
                find_events_this_week(date_start, events, event_info, i)

    for i in range(7):
        events[i].sort()
        textboxes[i].config(state=NORMAL)

    for i in range(7):
        for j in range(len(events[i])):
            if events[i][j][3] != '':
                events = split_multiple_day_events(events, i, j)
            textboxes[i].insert(END, events[i][j][0] + '-' + events[i][j][1] + '\n' + events[i][j][2] + '\n')
        textboxes[i].config(state=DISABLED)

    file.close()


def find_events_this_week(date_start, events, event_info, weekday_nr):
    weekday_abbr = [MO, TU, WE, TH, FR, SA, SU]
    today = date.today()
    if today.weekday() > weekday_nr and date_start == str(today + relativedelta(weekday=weekday_abbr[weekday_nr](-1))):
        events[weekday_nr].append(event_info)
    elif today.weekday() <= weekday_nr and date_start == str(today + relativedelta(weekday=weekday_nr)):
        events[weekday_nr].append(event_info)


def get_event_info(component):
    time_start = str(component.get('dtstart'))[21:26]
    time_end = str(component.get('dtend'))[21:26]
    event_name = str(component.get('summary'))

    date_start = str(component.get('dtstart'))[10:20]
    date_end = str(component.get('dtend'))[10:20]

    if time_start[0] == ' ' and time_end[0] == ' ':
        time_start = str(time(0, 0))[:5]
        time_end = str(time(23, 59))[:5]
        date_end = date_start

    event_info = [time_start, time_end, event_name, '']

    if date_start != date_end:
        event_info[3] = date_end

    return event_info, date_start


def initialize_window():
    window = Tk()
    window.title('Weekly Calendar')
    window.resizable(False, False)

    weekdays = ()
    days = ()
    text = ()
    left = 5
    right = 5

    day_numbers = update_days_numbers()

    for i in range(7):
        weekdays = weekdays + (Label(text=day_name[i], font=('', 12)),)
        days = days + (Label(text=day_numbers[i], font=('', 12)),)
        text = text + (Text(height=10, width=30),)

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

        text[i].config(state=DISABLED)

    label_title = Label(text='Weekly Calendar', font=('', 16))
    label_title.grid(row=3, column=6, columnspan=2, padx=10, pady=10)

    month = month_name[date.today().month]
    year = date.today().year

    label_month = Label(text=str(month) + ' ' + str(year), font=('', 12))
    label_month.grid(row=4, column=6, columnspan=2, padx=10, pady=10)

    button = Button(
        window,
        text='Open an ICS file',
        command=open_file
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
        title='Open',
        filetypes=(('iCalendar', '*.ics'),)
    )

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
    parts = day_end - day_start + 1
    part_first = [events[weekday_nr][event_nr][0], str(time(23, 59))[:5],
                  events[weekday_nr][event_nr][2], '']
    part_last = [str(time(0, 0))[:5], events[weekday_nr][event_nr][1],
                 events[weekday_nr][event_nr][2], '']

    if parts > 2:
        for i in range(1, parts - 1):
            part_middle = [str(time(0, 0))[:5], str(time(23, 59))[:5],
                           events[weekday_nr][event_nr][2], '']
            events[weekday_nr + i].append(part_middle)

    events[weekday_nr][event_nr] = part_first
    events[weekday_nr + parts - 1].append(part_last)

    return events


def update_days_numbers():
    day_numbers = [0] * 7
    weekday_abbr = [MO, TU, WE, TH, FR, SA, SU]
    today = date.today()

    for i in range(7):
        if today.weekday() > i:
            day_numbers[i] = str(today + relativedelta(weekday=weekday_abbr[i](-1)))[8:11]
        else:
            day_numbers[i] = str(today + relativedelta(weekday=i))[8:11]

    return day_numbers


if __name__ == '__main__':
    program, textboxes = initialize_window()
    load()
    program.mainloop()
