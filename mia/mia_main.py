""" imports """
import tkinter as tk
from tkinter import ttk
from gui.gui import MainApplication

def main():
    """ app main function """
    root = tk.Tk()

    #let child elements resize
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_window = MainApplication(root)
    main_window.grid(sticky="nesw")

    root.winfo_toplevel().title("MIA")
    root.update()
    root.style = ttk.Style()
    root.style.theme_use('clam')

    width_screen = root.winfo_screenwidth()
    height_screen = root.winfo_screenheight()

    width = root.winfo_width()
    height = root.winfo_height()

    new_x = (width_screen/2) - (width/2)
    new_y = (height_screen/2) - (height/2)

    root.geometry('%dx%d+%d+%d' % (width, height, int(new_x), int(new_y)))
    root.resizable(False, False)

    root.iconbitmap('static/39567a-cool-24.ico')
    root.iconify()
    root.deiconify()

    root.protocol("WM_DELETE_WINDOW", main_window.on_closing)
    root.after(50, main_window.loaded())

    try:
        root.mainloop()
    except:
        root.destroy()

if __name__ == "__main__":
    """ main """
    main()

