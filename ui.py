from calendar import day_name, month_name
from data import open_file, load_calendar
from datetime import date
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU, relativedelta
from logic import build_week_events
from tkcalendar import Calendar
from tkinter import *
from tkinter import scrolledtext


def display_calendar(events, text):
    for i in range(7):
        text[i].config(state=NORMAL)

        for event in events[i]:
            text[i].insert(END, event[0] + '-' + event[1] + '\n')
            text[i].insert(END, event[2] + '\n', 'bold')

        text[i].config(state=DISABLED)


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

    month = month_name[date.today().month]
    year = date.today().year

    label_month = Label(bg=blue, font=('Arial', 16), text=str(month) + ' ' + str(year))
    label_month.grid(row=0, column=0, sticky=W, padx=10, pady=10)
    
    button = Button(
    window,
    bg=light_blue,
    command=lambda: on_open_file_clicked(text),
    font=('Arial', 10),
    text='Open an ICS file',
    )
    button.grid(row=0, column=7, sticky=E, padx=10, pady=10)

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

            weekdays[i].grid(row=1, column=i * 2, sticky=W, padx=(left, 5), pady=(10, 5))
            days[i].grid(row=1, column=i * 2 + 1, sticky=E, padx=(5, right), pady=(10, 5))
            text[i].grid(row=2, column=i * 2, columnspan=2, padx=(left, right), pady=(5, 5))

        else:
            if i == 4:
                left = 10
            elif i == 6:
                right = 10

            weekdays[i].grid(row=3, column=(i - 4) * 2, sticky=W, padx=(left, 5), pady=(5, 5))
            days[i].grid(row=3, column=(i - 4) * 2 + 1, sticky=E, padx=(5, right), pady=(5, 5))
            text[i].grid(row=4, column=(i - 4) * 2, rowspan=3, columnspan=2, padx=(left, right), pady=(5, 10))

        text[i].tag_configure('normal', font=('Arial', 10))
        text[i].tag_configure('bold', font=('Arial', 10, 'bold'))
        text[i].config(state=DISABLED)

    calendar = Calendar(window, selectmode='day', year=today.year, month=today.month, day=today.day)
    calendar.grid(row=3, column=6, rowspan=2, columnspan=2, padx=10, pady=10)

    return window, text


def on_open_file_clicked(text):
    file_path = open_file(text)
    data = load_calendar(file_path)
    events = build_week_events(data)
    display_calendar(events, text)


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