from calendar import day_name
from datetime import date
from dateutil.relativedelta import relativedelta, MO
from icalendar import Calendar
from os.path import isfile
from tkinter import *
from tkinter import filedialog


def load():
    if isfile('saved_file_path.txt'):
        saved_file_path = open('saved_file_path.txt', 'r')
        file_path = saved_file_path.read()

        if file_path != '':
            display_calendar(file_path)

        saved_file_path.close()


def save(file_path):
    saved_file_path = open('saved_file_path.txt', 'w')
    saved_file_path.write(file_path)
    saved_file_path.close()


def get_event_info(component):
    event_start = str(component.get('dtstart'))[10:29]
    event_end = str(component.get('dtend'))[10:29]
    event_name = str(component.get('summary'))
    event_info = [event_start, event_end, event_name]
    return event_info


def find_events_this_week(start_date, events, event_info, weekday_nr):
    today = date.today()
    # if today.weekday() > weekday_nr and start_date == str(today + relativedelta(weekday=MO(-1))):
    #     events[weekday_nr].append(event_info)
    if start_date == str(today + relativedelta(weekday=weekday_nr)):
        events[weekday_nr].append(event_info)


def open_file():
    file_path = filedialog.askopenfilename(
        title='Open',
        filetypes=(('iCalendar', '*.ics'),)
    )

    save(file_path)

    for i in range(7):
        text[i].delete('1.0', END)

    display_calendar(file_path)


def display_calendar(file_path):
    file = open(file_path, 'rb')
    calendar = Calendar.from_ical(file.read())
    events = []

    for i in range(7):
        events.append([])

    for component in calendar.walk():
        if component.name == 'VEVENT':
            event_info = get_event_info(component)
            start_date = str(component.get('dtstart'))[10:20]

            for i in range(7):
                find_events_this_week(start_date, events, event_info, i)

    for i in range(7):
        events[i].sort()
        text[i].config(state=NORMAL)

    for event in range(len(events[2])):
        text[2].insert(END, events[2][event][0][11:] + '-')
        text[2].insert(END, events[2][event][1][11:] + '\n')
        text[2].insert(END, events[2][event][2] + '\n')
        #disabled text[]

    file.close()


if __name__ == '__main__':
    window = Tk()
    window.title('Weekly Calendar')
    window.resizable(False, False)

    weekdays = ()
    text = ()
    padding_right = 0

    for j in range(7):
        weekdays = weekdays + (Label(text=day_name[j], font=('', 12)),)
        text = text + (Text(height=10, width=30),)

        if j < 4:
            if j == 3:
                padding_right = 10

            weekdays[j].grid(row=0, column=j * 2, sticky=W, padx=10, pady=(10, 5))
            text[j].grid(row=1, column=j * 2, columnspan=2, padx=(10, padding_right), pady=5)
        else:
            weekdays[j].grid(row=2, column=(j - 4) * 2, sticky=W, padx=10, pady=5)
            text[j].grid(row=3, column=(j - 4) * 2, rowspan=3, columnspan=2, padx=(10, 0), pady=(5, 10))

        text[j].config(state=DISABLED)

    label_title = Label(text='Weekly Calendar', font=('', 16))
    label_title.grid(row=3, column=6, columnspan=2, padx=10, pady=10)

    label_month = Label(text='', font=('', 12))
    label_month.grid(row=4, column=6, columnspan=2, padx=10, pady=10)

    button = Button(
        window,
        text='Open an ICS file',
        command=open_file
    )
    button.grid(row=5, column=6, columnspan=2, padx=10, pady=10)

    load()
    window.mainloop()
