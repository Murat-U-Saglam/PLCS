import tkinter as tk  # Tkinter
import tkinter.messagebox as tm  # Tkinter Message Box
import os  # OsModule
import websiteHandler
import cookieGrabber as cookieGrabberf
from tkinter import filedialog
from pathlib import Path
from toolTip import CreateToolTip

Title = ("Verdana", 30)
Text = ("Calibri", 12)


class PasswordManager(tk.Tk):
    def __init__(self, *args,
                 **kwargs):  # initialization class constantly running. Args= pass through variables kwargs=pass through libaries/dictionaries
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (startPage, viewSnapShots, cookieGrabber):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(startPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class startPage(tk.Frame):  # The log in page
    def __init__(self, parent,
                 controller):  # __init__ makes sure that this class is accessibly to the whole program whenever
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.viewSnapshotBtn = tk.Button(self, text="NeverForgetter", fg="red", command=lambda: controller.show_frame(
            viewSnapShots))  # controller is used to swap the frames
        self.viewSnapshotBtn.grid(row=1, column=1)

        self.viewSnapshotBtn = tk.Button(self, text="CookieGrabber", fg="red", command=lambda: controller.show_frame(
            cookieGrabber))  # controller is used to swap the frames
        self.viewSnapshotBtn.grid(row=1, column=2)


class cookieGrabber(tk.Frame):  # SignUp frame for creating an account
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        cookieGrabberf.startSession()

        def getCookies():
            URL = self.entryURL.get()  # get the values from the URL entry
            cookieGrabberf.getCookies(URL)

        def setCookies():
            URL = self.entryURL.get()  # get the values from the URL entry
            cookieName = self.entryCookieName.get()
            cookieValue = self.entryCookieValue.get()
            cookieGrabberf.setCookies(URL, cookieName, cookieValue)

        def wipeCookies():
            cookieGrabberf.wipeCookies()

        def saveCookieSession():
            URL = self.entryURL.get()  # get the values from the URL entry
            cookieGrabberf.saveCookieSession(URL)

        def restoreCookieSession():
            URL = self.entryURL.get()  # get the values from the URL entry
            cookieGrabberf.restoreCookieSession(URL)

        def onEnter(text, button):
            button.configure(text=text)

        # Creating TKinter OBJ
        self.labelURL = tk.Label(self, text="URL")
        self.entryURL = tk.Entry(self)
        self.labelCookieName = tk.Label(self, text="Cookie Name")
        self.entryCookieName = tk.Entry(self)
        self.labelCookieValue = tk.Label(self, text="Cookie Value")
        self.entryCookieValue = tk.Entry(self)

        # Placing the Tkinter OBJs
        self.labelURL.grid(row=0, sticky="e")
        self.entryURL.grid(row=0, column=1)
        self.labelCookieName.grid(row=1, sticky="e")
        self.entryCookieName.grid(row=1, column=1)
        self.labelCookieValue.grid(row=2, sticky="e")
        self.entryCookieValue.grid(row=2, column=1)

        self.getCookiesBTN = tk.Button(self, text="Get Cookies", fg='white',
                                       bg="#263D42",
                                       command=getCookies)
        CreateToolTip(widget=self.getCookiesBTN, text="Gets the cookies that a website is requesting\nvia a http request")
        self.getCookiesBTN.grid(row=8, column=1)

        self.setCookiesBTN = tk.Button(self, text="Set Cookies", fg='white',
                                       bg="#263D42",
                                       command=setCookies)
        CreateToolTip(widget=self.setCookiesBTN, text="Applies the cookies entered to the cookieJar")
        self.setCookiesBTN.grid(row=9, column=1)

        self.wipeCookiesBTN = tk.Button(self, text="Wipe Cookies", fg='white',
                                        bg="#263D42",
                                        command=wipeCookies)
        CreateToolTip(widget=self.wipeCookiesBTN, text="Wipes the cookies from the current session")
        self.wipeCookiesBTN.grid(row=10, column=1)

        self.saveCookiesBTN = tk.Button(self, text="Save Cookies", fg='white',
                                        bg="#263D42",
                                        command=saveCookieSession)
        CreateToolTip(widget=self.saveCookiesBTN, text="Saves the cookies from the current cookieJar")
        self.saveCookiesBTN.grid(row=11, column=1)

        self.restoreCookiesBTN = tk.Button(self, text="Restore Cookies", fg='white',
                                        bg="#263D42",
                                        command=restoreCookieSession)
        CreateToolTip(widget=self.restoreCookiesBTN, text="Restores the cookie from the Persistent cookieJar")
        self.restoreCookiesBTN.grid(row=12, column=1)

        self.viewSnapshotBtn = tk.Button(self, text="Go home", fg="red", command=lambda: controller.show_frame(
            startPage))  # controller is used to swap the frames
        CreateToolTip(widget=self.viewSnapshotBtn, text="Go back to the home page to switch toolkits")
        self.viewSnapshotBtn.grid(row=13, column=1)


class viewSnapShots(tk.Frame):  # SignUp frame for creating an account
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def viewSnapshot():
            self.fileName = filedialog.askopenfilename(initialdir=os.getcwd() + "/Snapshots", title="Select file",
                                                       filetypes=(("gzip", "*.gz"), ("all files", "*.*")))
            websiteHandler.viewSnapshot(self.fileName)

        def compareSnapshot():
            self.fileName = filedialog.askopenfilename(initialdir=os.getcwd() + "/Snapshots",
                                                       title="Pick a snapshot to compare with current url",
                                                       filetypes=(("gzip", "*.gz"), ("all files", "*.*")))
            fileName = Path(self.fileName).name
            URL = self.entryURL.get()  # get the values from the URL entry
            if websiteHandler.compareSnapshot(URL, fileName) == 0:
                tm.showinfo("No Change", "There is no difference in the files")

        def compareSnapshotAndSave():
            self.fileName = filedialog.askopenfilename(initialdir=os.getcwd() + "/Snapshots",
                                                       title="Pick a snapshot to compare with current url",
                                                       filetypes=(("gzip", "*.gz"), ("all files", "*.*")))
            fileName = Path(self.fileName).name
            URL = self.entryURL.get()  # get the values from the URL entry
            if websiteHandler.compareSnapshotAndSave(URL, fileName) == 0:
                tm.showinfo("No Change", "There is no difference in the files")

        def takeSnapshot():
            URL = self.entryURL.get()  # get the values from the URL entry
            websiteHandler.takeSnapShot(URL)
            tm.showinfo("Snapshot Complete", "A snapshot has been created of the current instance of the URL entered")

        # Creating TKinter OBJ
        self.labelURL = tk.Label(self, text="URL")
        self.entryURL = tk.Entry(self)

        # Placing the Tkinter OBJs
        self.labelURL.grid(row=0, sticky="e")
        self.entryURL.grid(row=0, column=1)

        self.takeSnapshotBtn = tk.Button(self, text="Take Snapshot", fg='white', bg="#263D42",
                                         command=takeSnapshot)
        CreateToolTip(widget=self.takeSnapshotBtn, text="Hover text!")
        self.takeSnapshotBtn.grid(row=4, column=1)

        self.openFile = tk.Button(self, text="Restore snapshot", fg='white', bg="#263D42", command=viewSnapshot)
        CreateToolTip(widget=self.openFile, text="Hover text!")
        self.openFile.grid(row=5, column=1)

        self.compareFile = tk.Button(self, text="Compare snapshot", fg='white', bg="#263D42", command=compareSnapshot)
        CreateToolTip(widget=self.compareFile, text="Hover text!")
        self.compareFile.grid(row=6, column=1)

        self.compareFileAndSave = tk.Button(self, text="Compare snapshot and Save current snapshot", fg='white',
                                            bg="#263D42",
                                            command=compareSnapshotAndSave)
        CreateToolTip(widget=self.compareFileAndSave, text="Hover text!")
        self.compareFileAndSave.grid(row=7, column=1)

        self.viewSnapshotBtn = tk.Button(self, text="Go home", fg="red", command=lambda: controller.show_frame(
            startPage))  # controller is used to swap the frames
        CreateToolTip(widget=self.viewSnapshotBtn, text="Hover text!")
        self.viewSnapshotBtn.grid(row=8, column=1)


app = PasswordManager()  # giving a variable name to the password manger.
app.title("Murat Saglam's Cookie and Site Manager")
app.geometry("720x405")
app.mainloop()
