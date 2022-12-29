import random
import sys
from tkinter import Frame, font as tkfont, filedialog as fd, Tk, Label, Button, PhotoImage, Text, Widget, END, \
    messagebox, ttk
from PIL import Image, ImageTk

from customWigets import Collor, BetterButton, optionButton, setMode, initialize

AppName = "Mitiv"
from dowl import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller -> path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def getPath():
    f = str(__file__)
    fs = f[::-1].split("\\", 1)[1]
    return fs[::-1]


resource_path(getPath())

StatikImage = []


class Settings:
    def __init__(self, path):
        self.path = path
        try:
            with open(path, "r") as f:

                self.settings = json.load(f)[0]
        except Exception:
            self.settings = {"mode": "dark",
                             "sofInfoFile": "local",
                             "findSofAuto": "disabled"}
            self.save()

    def save(self):
        with open(self.path, "w") as f:
            json.dump([self.settings], f)

    def get(self, key):
        return self.settings[key]


Seti = Settings("setings.json")
setMode(Seti.get("mode"))


gtk = Tk()
initialize()
MF: Frame = None
titelF = tkfont.Font(family="Bahnschrift", size=18, weight="bold")
font_size_large = tkfont.Font(family="Bahnschrift", size=18, weight="bold")
font_size_medium = tkfont.Font(family="Bahnschrift", size=12, weight="bold")


def createLabel1(master, text, textAncor="center") -> Label:
    global titelF, font_size_medium
    return Label(master, text=text, font=font_size_medium, anchor=textAncor, bg=Collor.bg.value, fg=Collor.fg.value)


def open_window():
    global gtk, titelF, MF
    tk = gtk
    tk.title(AppName + "-Installer")
    tk.resizable(False, False)
    i = PhotoImage(master=tk, file=resource_path("resources/this.png"))
    tk.iconphoto(False, i)
    tk.configure(background=Collor.bg.value)
    tk.wm_geometry("600x400+%d+%d" % (-800, -800))
    tk.option_add('*Font', '19')

    tk.wm_geometry("+%d+%d" % (tk.winfo_screenwidth() // 2.4, tk.winfo_screenheight() // 2.8))
    titelF = tkfont.Font(family="Bahnschrift", size=18, weight="bold")

    MF = MainFrame = Frame(gtk, width=tk.winfo_width(), height=tk.winfo_height(), bg=Collor.bg.value)
    tk.update()
    MainFrame.place(x=0, y=0, width=tk.winfo_width(), height=tk.winfo_height())
    headlineLabel = Label(MainFrame, bg=Collor.bg.value, width=20, height=1, text="User Licence Agreement",
                          fg=Collor.fg.value
                          , font=font_size_large)
    headlineLabel.pack(side="top")
    f = Frame(master=MF, bg="red")
    f.pack()

    t = TextBox(master=f, max_lines=1, disableHightBouncing=True, width=50, height=17)

    with open("resources/license.txt", "r", encoding="utf-8") as license:

        for line in license.readlines():
            if line.startswith(">>>"):
                # Todo
                pass
            t.insert("0.0", line)
    s = ttk.Scrollbar(f, orient="vertical", command=t.yview, )
    st = ttk.Style(f)
    st.theme_use("clam")
    st.configure("Vertical.TScrollbar", background=Collor.bg_selected.value, borderwidth=0,  #
                 bordercolor="black", arrowcolor=Collor.fg.value,
                 foreground=Collor.fg.value, lightcolor=Collor.bg.value, darkcolor=Collor.bg.value,
                 troughcolor=Collor.bg.value, gripcount=0,
                 arrowsize=16)
    st.configure("Horizontal.TProgressbar",background="#83C9F4", borderwidth=0,
                 bordercolor="black", lightcolor=Collor.bg.value, darkcolor=Collor.bg.value,
                 troughcolor=Collor.bg.value,)
    t.pack(side="left")
    t['yscrollcommand'] = s.set
    s.pack(side="right", fill="y", expand=True)
    f2 = Frame(MF, bg=Collor.bg.value)
    f2.pack(side="bottom", anchor="ne", padx=(0, 20), pady=(0, 5))

    def openInstallOptions(tk, MF, other):
        headlineLabel, f, f2 = other
        headlineLabel.configure(text="Installer-Options")
        f.pack_forget()
        f2.pack_forget()
        l1=Label(MainFrame, bg=Collor.bg.value, width=20, height=3, text="Installation-Options", fg=Collor.fg.value
                 , font=font_size_large)
        l1.pack(side="top", anchor="nw")

        customPathInput = TextBox(master=MainFrame, max_lines=1, disableHightBouncing=True, width=30, height=1,
                                  start=Seti.get("defuld_install_path"))

        def onChangeCustomInstallPath(n):
            if (n == 0):
                customPathInput.setDisabled(False)
                return
            customPathInput.setDisabled(True)
            pass

        o1 = optionButton(master=MainFrame, name="RegisterApp :", options=[" Yes ", "  No  "], chosen=0)
        o1.pack(side="top",
                anchor="nw",
                padx=(20, 0))
        o2 = optionButton(master=MainFrame, name="CustomInstallationPath :", options=[" Yes ", "  No  "], chosen=1,
                          onChange=onChangeCustomInstallPath)
        o2.pack(side="top",
                anchor="nw", padx=(20, 0))
        customPathInput.pack(side="top", anchor="nw", padx=(60, 0), pady=(5, 0))
        # setting_button = BetterButton(master=tk, image=createImage("resources/settings_64.png", 32, 32), bg=Collor.bg.value,
        #                              command=None)
        # setting_button.pack(side="right", anchor="ne")

        f2 = Frame(MF, bg=Collor.bg.value)
        f2.pack(side="bottom", anchor="ne", padx=(0, 20), pady=(0, 5))

        def startInstall(o1, o2, i1, f2, headlineLabel, MainFrame,l1:Label):
            global gtk
            headlineLabel.configure(text="Installing ...")
            o1.pack_forget(), o2.pack_forget(), i1.pack_forget(),
            f2.pack_forget()
            l1.configure(font=font_size_medium)

            await_request(gtk,comp=(l1,MainFrame),trgloc=i1.getValue())

            pass

        BetterButton(master=f2, bg=Collor.bg_selected.value, text="Previous", highlightcolor="black",
                     fg=Collor.fg_inverted.value,
                     command=None).pack(side="left", padx=(0, 4))
        BetterButton(master=f2, bg=Collor.bg_selected.value, text="Start Installation", highlightcolor="black",
                     fg=Collor.fg_inverted.value,
                     command=lambda: startInstall(o1, o2, customPathInput, f2, headlineLabel, MainFrame,l1)).pack(
            side="right")

    BetterButton(master=f2, bg=Collor.bg_selected.value, text="Accept", highlightcolor="black",
                 fg=Collor.fg_inverted.value, command=lambda: openInstallOptions(tk, MF, (headlineLabel, f, f2))).pack(
        side="left", padx=(0, 4))
    BetterButton(master=f2, bg=Collor.bg_selected.value, text="Decline", highlightcolor="black",
                 fg=Collor.fg_inverted.value, command=gtk.destroy).pack(side="right")

    def openAbout():
        w = retInAppWindow(titel=" About ")

        createLabel1(w, "").pack(anchor="w")
        createLabel1(w, "Developed by: ").pack(anchor="w")
        createLabel1(w, "PackTheCommand").pack(anchor="w", padx=(12, 0))
        createLabel1(w, "https://packthecommand.000webhostapp.com").pack(anchor="w", padx=(13, 0))
        createLabel1(w, "").pack(anchor="w")
        createLabel1(w, "Credits: ").pack(anchor="w")
        createLabel1(w, "Icons by ICONS8 ( https://icons8.de )", textAncor="w").pack(anchor="w", padx=(12, 0))

    AboutButton = BetterButton(master=tk, text="About", bg=Collor.bg.value,
                               command=openAbout)
    AboutButton.pack(side="right", anchor="ne")


def retPh(m):
    return Label(m, bg=Collor.bg.value, font=tkfont.Font(size=1))


def retInAppWindow(disableX=False, width=380, height=320, highlightbackground="black", titel="", offsetY=0):
    global openMenues, MF

    mFrame = Frame(MF, width=width, height=height, highlightbackground=highlightbackground, highlightthickness=1, bd=0,
                   bg=Collor.bg.value)
    x, y = calcCenterXY(mFrame, w=width, h=height, )
    mFrame.place(x=x, y=y - offsetY, width=width, height=height)

    f = Frame(mFrame, bg=Collor.bg_darker.value)

    f.pack(side="top", anchor="n", fill="x")
    titel = L = Label(f, bg=Collor.bg_darker.value, fg=Collor.fg.value, font=font_size_medium, text=titel, anchor="w")
    titel.pack(side="left", anchor="nw")
    if not disableX:
        B = Button(f, text="❌", relief="flat", bg=Collor.bg_darker.value, fg=Collor.fg.value,
                   command=lambda: mFrame.place_forget())
        B.pack(side="right", anchor="ne")

    return mFrame


w_on_begin = (None, None, None, None)

cursor: tuple[int, int] = ()  # cursor position at any time


def motion(event):
    global cursor
    cursor = event.x, event.y


gtk.bind('<Motion>', motion)


def displayErr(text="Invalid Input or Value Missing"):
    global gtk
    L = Label(gtk, text=text, font=font_size_large, width=25, height=1, bg=Collor.bg.value,
              highlightbackground=Collor.err_color.value, highlightthickness=2, bd=0, fg=Collor.err_color.value)

    L.place(x=0, y=0)

    def corecktPos(e):
        x, y = calcCenterXY(e)
        e.place_configure(x=x, y=y - 100)

    gtk.after(1, lambda: corecktPos(L))

    gtk.after(2000, L.place_forget)


def addApp(appFrame):
    f = retInAppWindow(titel=" (+) Add App-Profile")

    i1 = createInput(f, "Name: ", "?", width=20, max_lines=1, )

    i2 = createInput(f, "Icon: ", "none", width=20, button=True, max_lines=3,
                     button_command=lambda: getPathFile(i2, ("PNG-File", "*.png"),
                                                        "\\" + resource_path("\\resources\icons")),
                     buton_text="Open")

    i3 = createInput(f, "File: ", " ", width=20, button=True, max_lines=3,
                     button_command=lambda: getPathFile(i3, ("Spec-File", ".spec"), "\\" + resource_path("")),
                     buton_text="Open")

    BSave = Button(master=f, text="Save", relief="flat", bg=Collor.bg_darker.value, fg=Collor.fg.value,
                   command=lambda: save((i1, i2, i3), f), font=font_size_medium)

    BSave.pack(side="bottom", anchor="se", pady=(0, 5), padx=(0, 5))

    def getPathFile(i, ft, fileOfset=""):
        path = fd.askopenfilename(
            title='Open a file',
            initialdir=getPath() + fileOfset,
            filetypes=[ft])
        if path:
            i.setValue(path)

    def save(i, wind):
        global appList_json
        try:
            i1, i2, i3 = i

            newAppEntry = {
                "name": i1.getValue(),
                "file": i3.getValue(),
                "icon": i2.getValue()
            }

            while True:
                id = str(random.randint(1, 99999))
                if (id not in list(appList_json.keys())):
                    break

            appList_json[id] = newAppEntry
            saveAppList()

        except:
            displayErr("InstallationError")


appList_json = {}


def AppListPathInsertion(name):
    if Seti.get("sofInfoFile") == "global":
        nP = "C:\mitiv-installer\\" + name
        if (os.path.exists(nP)):
            return "C:\mitiv-installer\\" + name
    return name


def saveAppList():
    with open(AppListPathInsertion("appList.json"), "w") as f:
        json.dump([appList_json], f)


class FramePart(Frame):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.base_pos = 0


class app():
    def __init__(self, jsonSpecPath):
        self.jloc = jsonSpecPath
        with open(jsonSpecPath, "r") as f:
            self.spec = json.load(f)[0]

    def saveSpec(self):
        with open(self.jloc, "w") as f:
            json.dump([self.spec], f)

    def setVersion(self, version: float):
        self.spec["current_version"] = float(version)

    def setUrl(self, Url: str):
        self.spec["Url"] = Url

    def setInstallLocation(self, location):
        self.spec["location"] = location

    def setOverwrite(self, overwriteArgs):
        pass


def createImage(path, x, y):
    global StatikImage
    try:
        photo = Image.open(path)
    except:
        photo = Image.open(resource_path("resources/unknown_app_64.png"))
    i = ImageTk.PhotoImage(photo.resize((x, y)))
    StatikImage += [i]
    return i


openMenues = []


def createInput(master, name, insert=None, width2=20, width=None, button=False, buton_text=None, button_command=None,
                max_lines=4):
    L = Label(master, text=name, bg=Collor.bg.value, fg=Collor.fg.value, font=font_size_medium, width=20, anchor="w")
    L.pack(side="top", anchor="nw", fill="x")
    f = Frame(master, bg=Collor.bg.value)
    f.pack(side="top")
    t = TextBox(master=f, width2=width2, insertbackground=Collor.fg.value, start=insert, max_lines=max_lines)
    if (width):
        t.configure(width=width)
    t.pack(side="left", anchor="nw")
    if button:
        b = Button(f, text=buton_text, relief="flat", bg=Collor.bg_darker.value, fg=Collor.fg.value,
                   command=button_command)
        b.pack(side="left", anchor="ne")
    return t


class TextBox(Text):
    def __init__(self, max_lines, width2=0, disableHightBouncing=False, start=None, **kw):
        super().__init__(bg=Collor.bg_darker.value, fg=Collor.fg.value, font=font_size_medium, **kw)
        self.disableHightBouncing = disableHightBouncing
        self.bind("<Return>", self.e)
        self.widthNum = width2
        self.max_lines = max_lines
        if not disableHightBouncing:
            self.bind("<Key>", lambda u: gtk.after(10, self.updateHeight))
        if start:
            self.insert("0.0", start)
            if not disableHightBouncing:
                self.updateHeight()

    def e(self, u):
        return "break"

    def setValue(self, text):
        self.clear()
        self.insert("0.0", text)

    def updateHeight(self):
        le = len(self.getValue())
        h = 1 + (le // self.widthNum) // 2
        if h > self.max_lines:
            h = self.max_lines
        self.configure(height=h)
        # print(h)

        self.winfo_width()

    def getValue(self):
        return self.get("0.0", END).replace("\n", "")

    def clear(self):
        self.replace("0.0", END, "")

    def setDisabled(self, tr):
        if (tr):
            self["state"] = "disabled"
            self.configure(bg=Collor.bg.value)
            return
        self["state"] = "normal"
        self.configure(bg=Collor.bg_selected.value)


open_window()


def askQuestion(after, args):
    f = retInAppWindow(height=100, width=200, highlightbackground="#377896", titel="Are you sure?", offsetY=100)

    L = createLabel1(f, "Are you Sure ?")
    L.pack(anchor="n", side="top")
    bf = Frame(f, bg=Collor.bg.value)
    bf.pack(anchor="center", side="bottom")
    Byes = Button(master=bf, width=4, text="Yes", relief="flat", bg=Collor.bg_darker.value, fg=Collor.fg.value,
                  command=lambda: on_but_click(f, "yes", after, args), font=font_size_medium,
                  ).pack(side="left", anchor="e", pady=(0, 5),
                         padx=(0, 5))
    Bno = Button(master=bf, width=4, text="No", relief="flat", bg=Collor.bg_darker.value, fg=Collor.fg.value,
                 command=lambda: on_but_click(f, "no", after, args), font=font_size_medium,
                 ).pack(side="right", anchor="w", pady=(0, 5), padx=(0, 5))

    def on_but_click(w, ans, after, args):
        w.place_forget()
        after(ans, *args)


def calcCenterXY(widget: Widget, w=None, h=None) -> (int, int):
    global gtk

    if (not ((w != None) & (h != None))):
        w = widget.winfo_width()
        h = widget.winfo_height()
    else:
        w = w
        h = h

    ws_x = gtk.winfo_width()

    hs_y = gtk.winfo_height()

    fx = (ws_x // 2) - (w // 2)
    fy = (hs_y // 2) - (h // 2)

    return fx, fy


try:

    gtk.mainloop()
except Exception as e:
    messagebox.showerror("Application Guard", "Application or Required file Tree Corupted. Err: \n" + repr(e))
