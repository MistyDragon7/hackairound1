from uagents import Agent

from tkinter import *

window = Tk()
window.title("Temperature alert bot")
window.configure(bg="yellow")
label = Label(window, text = '''Welcome to Tempy, the temperature alert bot!! Please choose from options given: ''', font = ('Comic Sans MS', 12), bg = 'yellow')
label.grid(column = 1, row = 0)
def get_temp_alerts(event):
    from agents.tempy.tempy import tempy as tempy_agent
    if __name__ == "__main__":
        tempy_agent.run()
button1 = Button(window, text = "Set a new Temperature Alert", font = ("Comic Sans MS", 12), relief = "groove", bg = "black", fg = "white")
button1.bind("<Button-1>", get_temp_alerts)
button1.grid(column = 0, row = 1)
window.mainloop()

