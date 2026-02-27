from logic import build_week_events
from os.path import isfile
from tkinter import *
from tkinter import filedialog


def load(text):
    if isfile('saved_file_path.txt'):
        with open('saved_file_path.txt', 'r') as f:
            file_path = f.read().strip()
        if file_path:
            data = load_calendar(file_path)
            events = build_week_events(data)
            from ui import display_calendar  # optional if avoiding circular import
            display_calendar(events, text)

        f.close()


def load_calendar(file_path):
    with open(file_path, 'rb') as f:
        return f.read()


def open_file(text):
    file_path = filedialog.askopenfilename(
        filetypes=(('iCalendar', '*.ics'),),
        title='Open'
    )

    if file_path != '':
        save(file_path)
    
        for i in range(7):
            text[i].config(state=NORMAL)
            text[i].delete('1.0', END)

        #display_calendar(file_path)

    
    return file_path


def save(file_path):
    saved_file_path = open('saved_file_path.txt', 'w')
    saved_file_path.write(file_path)
    saved_file_path.close()