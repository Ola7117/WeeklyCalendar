from data import load
from ui import initialize_window

window, texts = initialize_window()
load(texts)
window.mainloop()