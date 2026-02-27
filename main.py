from data import load
from ui import initialize_window

window, text = initialize_window()
load(text)
window.mainloop()