import tkinter as tk
from tkinter import ttk
from gui.gui import MainApplication

def main():
    root = tk.Tk()

    #let child elements resize
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    MainApplication(root).grid(sticky="nesw")

    root.winfo_toplevel().title("MIA")
    root.update()
    root.style = ttk.Style()
    root.style.theme_use('clam')

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    w = root.winfo_width()
    h = root.winfo_height()

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w,h,x,y))
    root.resizable(False, False)

    root.iconbitmap('39567a-cool-24.ico')
    root.iconify()
    root.deiconify()
    root.mainloop()

if __name__ == "__main__":
    """ """
    main()