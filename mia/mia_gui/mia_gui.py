import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as tkfd
from time import time, localtime, strftime
from config import Config
import datetime


#############################################################################################
# Tooltip class taken from http://code.activestate.com/recipes/576688-tooltip-for-tkinter/  #
# Written by Pete Garcin, github: rawktron                                                  #
#############################################################################################
class ToolTip( Toplevel ):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor
    """
    def __init__( self, wdgt, msg=None, msgFunc=None, delay=1, follow=True ):
        """
        Initialize the ToolTip

        Arguments:
          wdgt: The widget this ToolTip is assigned to
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        self.parent = self.wdgt.master                                          # The parent of the ToolTip is the parent of the ToolTips widget
        Toplevel.__init__( self, self.parent, bg='black', padx=1, pady=1 )      # Initalise the Toplevel
        self.withdraw()                                                         # Hide initially
        self.overrideredirect( True )                                           # The ToolTip Toplevel should have no frame or title bar

        self.msgVar = StringVar()                                               # The msgVar will contain the text displayed by the ToolTip
        if msg == None:
            self.msgVar.set( 'No message provided' )
        else:
            self.msgVar.set( msg )
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        Message( self, textvariable=self.msgVar, bg='#FFFFDD',
                 aspect=1000 ).grid()                                           # The test of the ToolTip is displayed in a Message widget
        self.wdgt.bind( '<Enter>', self.spawn, '+' )                            # Add bindings to the widget.  This will NOT override bindings that the widget already has
        self.wdgt.bind( '<Leave>', self.hide, '+' )
        self.wdgt.bind( '<Motion>', self.move, '+' )

    def spawn( self, event=None ):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget

        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        self.after( int( self.delay * 1000 ), self.show )                       # The after function takes a time argument in miliseconds

    def show( self ):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move( self, event ):
        """
        Processes motion within the widget.

        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        if self.follow == False:                                                # If the follow flag is not set, motion within the widget will make the ToolTip dissapear
            self.withdraw()
            self.visible = 1
        self.geometry( '+%i+%i' % ( event.x_root+10, event.y_root+10 ) )        # Offset the ToolTip 10x10 pixes southwest of the pointer
        try:
            self.msgVar.set( self.msgFunc() )                                   # Try to call the message function.  Will not change the message if the message function is None or the message function fails
        except:
            pass
        self.after( int( self.delay * 1000 ), self.show )

    def hide( self, event=None ):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget

        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()


class SettingsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.initialize()

    def pick_dst_btn_clicked(self):
        """ """
        folder_name = tkfd.askdirectory()
        if(folder_name):
            #enable textbox to allow insertion
            self.dst_field.configure(state="normal")
            self.dst_field.insert("0.0", str(folder_name))
            ToolTip(self.dst_field, str(folder_name))
            #disable to prevent direct user input
            self.dst_field.configure(state="disabled")
        else:
            print("No folder selected!")

    def interval_val_changed(self, value):
        """ """
        ## set val in settings
        print(value)

    def parallelize_checked(self):
        """ """
        if self.parallelize.get():
            #paralellize is checked
            print("RAGE IT!")
        else:
            #paralellize is unchecked
            print("THROTTLE BACK AAAHHHH")

    def add_src_folder(self):
        folder_name = tkfd.askdirectory()
        if(folder_name):
            srcs = self.src_list.get(0, END)
            if folder_name not in srcs:
                self.src_list.insert(END, folder_name)
        else:
            print("No folder selected!")

    def del_src_btn_clicked(self):
        lb = self.src_list
        #lambda lb=self.src_list: lb.delete(ANCHOR)
        selected = lb.curselection()
        if selected:
            lb.delete(selected)
        else:
            messagebox.showinfo("No sources selected", "You must select a source to remove one.")

        #lambda lb=self.src_list: lb.delete(ANCHOR)

    def choose_readw_loc(self):
        """ """
        file_name = tkfd.askopenfile()
        if(file_name):
            self.exe_field.configure(state="normal")
            #text box index location is noted by "row.column"
            self.exe_field.insert("0.0", str(file_name.name))
            ToolTip(self.exe_field, str(file_name.name))
            self.exe_field.configure(state="disabled")

    def initialize(self):
        """ """
        #### SOURCE FOLDER WIDGETS & BUTTONS #####
        self.src_lbl = tk.Label(self, text="Source Folders")
        #sets background of this element to be the same background as the parent color
        #note that self["bg"] returns parents background color.
        #More generally, widget["bg"]. Alternate way of writing this is self.src_lbl["bg"] = self["bg"]
        self.src_lbl.configure(background=self["bg"])

        #padx=(left,right) <- pads the cell with tuple for left/right pad
        #pady=(top, bottom) <- pads the cell with tuple for top/bottom pad
        self.src_lbl.grid(row=0, column=0, columnspan=3, padx=20, pady=(0,0), sticky=W)

        #self.src_scrll = Scrollbar(self, orient=VERTICAL)

        ##listbox, this maintains a list of clickable items - these will be the source folders
        ##height is set to 5x the height of a label, should be able to view 5 source folders in a window
        self.src_list = tk.Listbox(self, height=5)#, yscrollcommand=self.src_scrll.set)
        self.src_list.grid(row=1, column = 0, rowspan=2, padx=20, pady=0, sticky="we")

        #self.src_scrll.config(command=self.src_list.yview)
        #self.src_scrll.grid(row=1, column=0)

        self.src_list.insert(END, "C:/Sample/Directory")
        ##end listbox
        self.add_src_btn = tk.Button(
            self, text="Add Folder", width=15, command=self.add_src_folder
        )

        # find default button height################
        self.btn_height = self.add_src_btn.winfo_height()
        ############################################

        self.del_src_btn = tk.Button(
            self, text="Remove Folder", width=15,
            command=self.del_src_btn_clicked
        )
        self.add_src_btn.grid(row=1, column=2, padx=20, sticky=N)
        self.del_src_btn.grid(row=2, column=2, padx=20, pady=(20,0), sticky=S)
        #Style().configure("TButton", padding=(10,10,10,10))

        ### END SOURCE FOLDERS WIDGETS & BUTTONS ###


        ### start pick_exe section ###
        self.exe_lbl = tk.Label(self, text="ReAdW.exe Location")
        self.exe_lbl.configure(background=self["bg"])
        self.exe_lbl.grid(row=3, column = 0, padx=20, pady=(0,0), sticky="ew")

        self.exe_field = tk.Text(self, height=self.btn_height, width=50, state="disabled")
        self.exe_field.grid(row=4, column=0, columnspan=1, padx=20, sticky="ew")
        self.exe_field.configure(background="lightgray")

        self.pick_exe_btn = tk.Button(
            self, text="Choose Location", width=15, command=self.choose_readw_loc
        )
        self.pick_exe_btn.grid(row=4, column=2)

        ### END pick_exe section ###

        ### start pick destination section ###
        ##Note columnspan=2, this tells the grid manaeger to span this widget over 2
        ##It will appear centered in row 0 and row 1.
        self.dst_lbl = tk.Label(self, text="Destination")
        self.dst_lbl.configure(background=self["bg"])
        self.dst_lbl.grid(row=5, column=0, columnspan=2, padx=20, pady=0, sticky="w")

        self.dst_field = tk.Text(self, height=self.btn_height, width=50, state="disabled")
        self.dst_field.grid(row=6, column = 0, columnspan=1, padx=20, pady=(0,20), sticky="ew")
        self.dst_field.configure(background="lightgray")

        self.pick_dst_btn = tk.Button(
            self, text="Choose Destination", width=15, command=self.pick_dst_btn_clicked
        )
        self.pick_dst_btn.grid(row=6, column=2, pady=(0,20))
        ###end pick desitnation section ###

        ### start interval section ###
        self.interval_lbl = tk.Label(self, text="Transfer Interval (Minutes)")
        self.interval_lbl.configure(background=self["bg"])
        self.interval_lbl.grid(row=7, column=0, columnspan=2, padx=20, pady=0, sticky="w")

        self.interval_slider = tk.Scale(self, from_=5, to=45, orient=HORIZONTAL, command=self.interval_val_changed)
        self.interval_slider.grid(row=8, column=0, padx=20, pady=(0,20), sticky="ew")

        ### end interval section ###

        self.parallel_frame = tk.Frame(self)
        self.parallel_frame.grid(row=8, column=2)

        self.parallelize = tk.IntVar()


        self.parallel_lbl = tk.Label(self.parallel_frame, text="Parallelize")
        self.parallel_lbl.grid(row=0, column=0, padx=(0,10))

        self.parallel_chkbx = tk.Checkbutton(self.parallel_frame, variable=self.parallelize, command=self.parallelize_checked)
        self.parallel_chkbx.grid(row=0, column=1, padx=(10,10))


class Controls(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.initialize()

    def stop_mia(self):
        """ """
        self.stop_btn.configure(state="disabled")
        self.restart_btn.configure(state="disabled")
        self.parent.update_status("Just as I was ... learning ... to love.... (shutting down)")
        #do mia stop
        self.start_btn.configure(state="normal")

    def start_mia(self):
        """ """
        self.start_btn.configure(state="disabled")
        #do mia start
        #read new config variables and start up
        self.parent.update_status("Booting up!")
        self.stop_btn.configure(state="normal")
        self.restart_btn.configure(state="normal")

    def restart_mia(self):
        """ """
        self.parent.update_status("Restarting!")
        #do mia restart
        #read new config variables
        #could probably just call start then stop

    def initialize(self):
        ### default to disabled, enable when stop is pressed ###
        self.start_btn = tk.Button(
            self, text="Start Mia", width=15, command=self.start_mia,
        )

        self.stop_btn = tk.Button(
            self, text="Stop Mia", width=15, command=self.stop_mia, state="disabled"
        )
        self.restart_btn = tk.Button(
            self, text="Restart Mia", width=15, command=self.restart_mia, state="disabled"
        )

        self.start_btn.grid(row=0, column=0, columnspan=1, padx=(50,40), pady=(20,20))
        self.stop_btn.grid(row=0, column=1, columnspan=1, padx=(20,20), pady=(20,20))
        self.restart_btn.grid(row=0, column=2, columnspan=1, padx=(40,50), pady=(20,20))
        ### end control button settings ###


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.config = Config()
        self.initialize()

    def update_status(self, msg):
        """ """
        msg = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S - ') + msg
        self.status_list_box.insert(0, msg)

    def initialize(self):
        self.grid(sticky="nesw")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        for i in range(0, 15):
            self.rowconfigure(i, weight=1)

        ## horizontal lines by title
        sep = ttk.Separator(self, orient=HORIZONTAL)
        sep.grid(row=0,column=0,sticky="ew", padx=(80,0))
        sep2 = ttk.Separator(self, orient=HORIZONTAL)
        sep2.grid(row=0,column=2, sticky="ew", padx=(0,80))

        ##w.create_rectangle(50, 25, 150, 75, fill="blue")

        self.main_lbl = tk.Label(self, text="Mia!")
        self.main_lbl.grid(row=0, column=1)
        self.main_lbl.config(font=("Garamond", 32))

        self.settings_frame = SettingsFrame(self, background=self.parent["bg"])
        self.settings_frame.grid(row=1, column=0, columnspan=3)

        self.ctrl_frame = Controls(self, highlightbackground='darkgray', highlightcolor='darkgray', highlightthickness=1)
        self.ctrl_frame.grid(row=2, column=0, columnspan=3, pady=(0,20))

        self.status_frame = tk.Frame(self, highlightbackground='darkgray', highlightcolor='darkgray', highlightthickness=1)
        self.status_frame.grid(row=3, column=0, columnspan=3, sticky="ew")

        self.status_frame.columnconfigure(0, weight=1)

        self.status_lbl = tk.Label(self.status_frame, text="Status", width=15)
        self.status_lbl.grid(row=0,column=0)

        #status list box holds 5 items (change with width=x)
        self.status_list_box = tk.Listbox(self.status_frame, background=self["bg"], height=10)
        self.status_list_box.grid(row=1,column=0, columnspan=3, sticky="nsew")

if __name__ == "__main__":
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
