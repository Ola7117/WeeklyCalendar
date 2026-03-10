from datetime import date
from logic import build_week_events
from os.path import isfile
from tkinter import *
from tkinter import filedialog


def load(texts, selected_date=date.today()):
    for text in texts:
        text.config(state=NORMAL)
        text.delete("1.0", END)
        print(texts)
        text.config(state=DISABLED)

    if isfile('saved_file_path.txt'):
        with open('saved_file_path.txt', 'r') as f:
            file_path = f.read().strip()
        if file_path:
            data = load_calendar(file_path)
            events = build_week_events(data, selected_date)
            print(events)
            from ui import display_calendar
            display_calendar(events, texts)


def load_calendar(file_path):
    with open(file_path, 'rb') as f:
        return f.read()


def open_file(texts):
    file_path = filedialog.askopenfilename(
        filetypes=(('iCalendar', '*.ics'),),
        title='Open'
    )

    if file_path != '':
        save(file_path)
    
        for i in range(7):
            texts[i].config(state=NORMAL)
            texts[i].delete('1.0', END)

        #display_calendar(file_path)

    
    return file_path


def save(file_path):
    saved_file_path = open('saved_file_path.txt', 'w')
    saved_file_path.write(file_path)
    saved_file_path.close()