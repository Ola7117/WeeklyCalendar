from calendar import *
from datetime import *
from dateutil.relativedelta import *
from icalendar import Calendar
from tkinter import *
from tkinter import filedialog


def open_calendar():

    file_path = filedialog.askopenfilename(
        title='Open',
        filetypes=(('iCalendar', '*.ics'),)
    )

    file = open(file_path, 'rb')
    calendar = Calendar.from_ical(file.read())
    today = date.today()

    for component in calendar.walk():
        if component.name == 'VEVENT':
            if str(component.get('dtstart'))[10:20] == str(today + relativedelta(weekday=MO)):
                text0.insert(END, component.get('summary'))
            elif str(component.get('dtstart'))[10:20] == str(today + relativedelta(weekday=TU)):
                text1.insert(END, component.get('summary'))
            elif str(component.get('dtstart'))[10:20] == str(today + relativedelta(weekday=WE)):
                text2.insert(END, component.get('summary'))
            elif str(component.get('dtstart'))[10:20] == str(today + relativedelta(weekday=TH)):
                text3.insert(END, component.get('summary'))
            elif str(component.get('dtstart'))[10:20] == str(today + relativedelta(weekday=FR)):
                text4.insert(END, component.get('summary'))
            elif str(component.get('dtstart'))[10:20] == str(today + relativedelta(weekday=SA)):
                text5.insert(END, component.get('summary'))
            elif str(component.get('dtstart'))[10:20] == str(today + relativedelta(weekday=SU)):
                text6.insert(END, component.get('summary'))

    file.close()


window = Tk()
window.title('Weekly Calendar')

label_w = Label(text='Weekly Calendar', font=('', 16))
label_w.grid(row=0, column=0, columnspan=7, padx=10, pady=10)

button = Button(
    window,
    text='Open a calendar file',
    command=open_calendar
)
button.grid(row=1, column=0, columnspan=7, padx=10, pady=10)

label0 = Label(text='Monday', font=('', 12))
label0.grid(row=2, column=0, padx=10, pady=10)

text0 = Text(height=20, width=15)
text0.grid(row=3, column=0, padx=10, pady=10)

label1 = Label(text='Tuesday', font=('', 12))
label1.grid(row=2, column=1, padx=10, pady=10)

text1 = Text(height=20, width=15)
text1.grid(row=3, column=1, padx=10, pady=10)

label2 = Label(text='Wednesday', font=('', 12))
label2.grid(row=2, column=2, padx=10, pady=10)

text2 = Text(height=20, width=15)
text2.grid(row=3, column=2, padx=10, pady=10)

label3 = Label(text='Thursday', font=('', 12))
label3.grid(row=2, column=3, padx=10, pady=10)

text3 = Text(height=20, width=15)
text3.grid(row=3, column=3, padx=10, pady=10)

label4 = Label(text='Friday', font=('', 12))
label4.grid(row=2, column=4, padx=10, pady=10)

text4 = Text(height=20, width=15)
text4.grid(row=3, column=4, padx=10, pady=10)

label5 = Label(text='Saturday', font=('', 12))
label5.grid(row=2, column=5, padx=10, pady=10)

text5 = Text(height=20, width=15)
text5.grid(row=3, column=5, padx=10, pady=10)

label6 = Label(text='Sunday', font=('', 12))
label6.grid(row=2, column=6, padx=10, pady=10)

text6 = Text(height=20, width=15)
text6.grid(row=3, column=6, padx=10, pady=10)

window.mainloop()
