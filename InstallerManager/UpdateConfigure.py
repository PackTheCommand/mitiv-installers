import random
import sys
import os
from tkinter import Frame, font as tkfont, filedialog as fd, Tk, Label, Button, PhotoImage, Text, Widget, END, \
    messagebox
import enum
import json
from PIL import Image, ImageTk


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
mode = Seti.get("mode")


class Collor(enum.Enum):
    if mode == "dark":
        bg = "#232327"
        bg_darker = "#151517"
        fg = "silver"
        bg_cancel = "#3d3d3d"
        bg_reinst = "#212121"
        bg_selected = "#80868a"
        fg_reinst = "#181818"
        err_color = "#AA1F2B"
    else:
        bg = "#E0E0E0"
        bg_darker = "#94999c"
        fg = "#161616"
        bg_cancel = bg
        bg_selected = "#505457"
        bg_reinst = "#CECECE"
        fg_reinst = "#B5B5B5"
        err_color = "#FF4460"


gtk = Tk()
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
    tk.title("Update-Config")
    tk.resizable(False, False)
    i = PhotoImage(master=tk, file=resource_path("resources/this.png"))
    tk.iconphoto(False, i)
    tk.configure(background=Collor.bg.value)
    tk.wm_geometry("500x500+%d+%d" % (-800, -800))
    tk.option_add('*Font', '19')
    # tk.wm_attributes("-transparentcolor", "#000000")
    # tk.resizable(False, False)
    tk.wm_geometry("+%d+%d" % (tk.winfo_screenwidth() // 2.4, tk.winfo_screenheight() // 2.8))
    titelF = tkfont.Font(family="Bahnschrift", size=18, weight="bold")

    # Label(tk, font=titelF, bg=collor.bg.value, fg=collor.fg.value, ).pack(side="top")

    # tL = Label(font=titelF, bg=collor.bg.value, fg=collor.fg.value, text="Checking for updates")
    # tL.pack(side="top")
    MF = MainFrame = Frame(gtk, width=tk.winfo_width(), height=tk.winfo_height(), bg=Collor.bg.value)
    tk.update()
    MainFrame.place(x=0, y=0, width=tk.winfo_width(), height=tk.winfo_height())
    Label(MainFrame, bg=Collor.bg.value, width=20, height=3, text="Updater Configuration", fg=Collor.fg.value
          , font=font_size_large).pack(side="top")
    appFrame = Frame(MainFrame, bg=Collor.bg.value, width=1000)
    appFrame.pack(anchor="center")
    bAdd = Button(appFrame, text="➕", bg=Collor.bg_darker.value, fg=Collor.fg.value,
                  highlightbackground=Collor.err_color.value, highlightthickness=1, bd=0, font=font_size_medium,
                  command=lambda: addApp(appFrame)
                  )
    bAdd.pack(side="bottom", fill="x")
    loadApps(appFrame)
    setting_button = BetterButton(master=tk, image=createImage("resources/settings_64.png", 32, 32), bg=Collor.bg.value,
                                command=openSetings)
    setting_button.pack(side="right", anchor="ne")

    titelF = tkfont.Font(family="Bahnschrift", size=18, weight="bold")
    subInfo = tkfont.Font(family="Bahnschrift", size=12, weight="bold")
    # v1, v2 = data["version"]
    # tk.title(f"Ver {v1} -> {v2}")

    # L = Label(tk, text="Update", font=titelF, bg=collor.bg.value, fg=collor.fg.value)
    # LI = Label(tk, text="... update in progress",

    # L.pack(side="top")
    # LI.pack(side="top")
    tk.after(50, lambda: None)

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
    AboutButton.pack(side="left", anchor="nw")


def retPh(m):
    return Label(m, bg=Collor.bg.value, font=tkfont.Font(size=1))


def openSetings():
    w = retInAppWindow(height=400, titel="  Setings")

    o1 = optionButton(master=w, name="Display-Mode:", options=["dark", "light"], chosenStr=Seti.get("mode"))
    o1.pack()
    retPh(w).pack()
    o2 = optionButton(master=w, name="SoftwareInfoFile:", options=["local", "global"],
                      chosenStr=Seti.get("sofInfoFile"))
    o2.pack()
    o3 = optionButton(master=w, name="FindSoftwareAutomatically", options=["enabled", "disabled"],
                      chosenStr=Seti.get("findSofAuto"))
    o3.pack()
    BSave = Button(master=w, text="Save", relief="flat", bg=Collor.bg_darker.value, fg=Collor.fg.value,
                   command=lambda: save(o1, o2, o3, w), font=font_size_medium)

    BSave.pack(side="bottom", anchor="se", pady=(0, 5), padx=(0, 5))

    def save(o1, o2, o3, w):
        Seti.settings["mode"] = o1.getSelectedItem()
        Seti.settings["sofInfoFile"] = o2.getSelectedItem()
        Seti.settings["findSofAuto"] = o3.getSelectedItem()
        Seti.save()
        w.place_forget()


class optionButton(Frame):
    def __init__(self, name, chosen: int = None, chosenStr=None, options=[], **kw):
        super().__init__(**kw)
        self.names = options
        self.optItems = []

        n = 0
        self.selected = -1
        b = Label(master=self, text=name + " ", bg=Collor.bg.value, fg=Collor.fg.value, font=font_size_medium)

        b.pack(side="left", anchor="ne")

        print(f"{n=}")
        for o in options:
            b = Label(master=self, text=o, bg=Collor.bg_selected.value, fg=Collor.bg_darker.value,
                      highlightbackground=Collor.bg_darker.value, font=font_size_medium, highlightthickness=2, bd=0)

            b.bind("<Button-1>", lambda u, num=n: self.setSelected(n=num))

            b.pack(side="left", anchor="ne")

            self.optItems += [b]

            n += 1
        if chosen != None:
            self.setSelected(chosen)

        if chosenStr != None:
            self.setSelectedStr(chosenStr)

    def setSelected(self, n):

        self.selected = n
        for nu, item in enumerate(self.optItems):

            if (nu == n):
                item.configure(bg=Collor.bg.value, fg=Collor.fg.value, highlightbackground=Collor.fg.value)
                continue
            item.configure(bg=Collor.bg_selected.value, fg=Collor.bg_darker.value,
                           highlightbackground=Collor.bg_darker.value)
        return n
        pass

    def setSelectedStr(self, str):

        for n, s in enumerate(self.names):
            b = self.optItems[n]

            if (s == str):
                self.selected = n
                b.configure(bg=Collor.bg.value, fg=Collor.fg.value, highlightbackground=Collor.fg.value)
                continue
            b.configure(bg=Collor.bg_selected.value, fg=Collor.bg_darker.value,
                        highlightbackground=Collor.bg_darker.value)

        pass

    def getSelectedItem(self):
        print(self.selected)
        if self.selected == -1:
            return None

        return self.names[self.selected]


class BetterButton(Button):
    def __init__(self, bg=Collor.bg_darker.value, fg=Collor.fg.value, **kn):
        super().__init__(bg=bg, fg=fg,
                         highlightbackground=Collor.err_color.value, highlightthickness=1, bd=0, font=font_size_medium,
                         **kn)


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

            ico = i2.getValue()

            if (ico != ""):
                createAppBar(id, appFrame, i1.getValue(), image=ico, appPath=i3.getValue())
            else:
                createAppBar(id, appFrame, i1.getValue(), appPath=i3.getValue())

            appList_json[id] = newAppEntry
            saveAppList()
            wind.place_forget()
        except:
            displayErr("Invalid Input or Value Missing")


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


def loadApps(appFrame):
    global appList_json
    try:

        with open(AppListPathInsertion("appList.json"), "r") as f:
            appList_json = json.load(f)[0]
    except Exception:
        f = open("appList.json", "w")
        f.write("[{}]")
        with open("appList.json", "r") as f:
            appList_json = json.load(f)[0]
    # print(appList_json)
    for key in appList_json.keys():
        appC = appList_json[key]
        # print(appC)
        ico = appC["icon"]
        try:
            if (ico):
                createAppBar(key, appFrame, appC["name"], appPath=appC["file"], image=ico)
            else:
                createAppBar(key, appFrame, appC["name"], appPath=appC["file"])
        except Exception:
            pass


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


def createAppBar(e_id, master, text: str = "<Name>", image=resource_path("resources/unknown_app_64.png"),
                 appPath=resource_path("instance.spec")) -> Button:
    global gtk, StatikImage
    if (appPath == ""):
        appPath = resource_path("instance.spec")
    f = FramePart(master=master, highlightbackground="black", width=100, highlightthickness=1, bd=0, bg=Collor.bg.value)
    Name = createLabel1(f, " " + text)
    Button()
    try:
        photo = Image.open(image)
    except:

        photo = Image.open(resource_path("resources/unknown_app_64.png"))

    i = ImageTk.PhotoImage(photo.resize((25, 25)))

    StatikImage += [i]
    ico = Label(f, image=i, bg=Collor.bg.value)
    ico.pack(side="left", anchor="w")
    Name.pack(side="left", anchor="w")
    a = app(appPath)
    menu = Button(f, text="...", bg=Collor.bg.value, fg=Collor.fg.value, highlightbackground="black",
                  highlightthickness=1, bd=0, font=font_size_medium, command=lambda: openEditor(a))
    L = Label(f, bg=Collor.bg.value, width="5").pack(side="left", anchor="w")
    dwl = Button(f, text=" 🚀 ", bg=Collor.bg.value, fg=Collor.fg.value, border=0, font=font_size_medium)
    remove = Button(f, text="🗑", bg=Collor.bg.value, fg=Collor.fg.value, border=0, font=font_size_medium,
                    command=lambda: askQuestion(removeInstallEnty, (e_id, f)))
    L = Label(f, bg=Collor.bg.value)

    # progress = createLabel1(f, "?")
    dwl.pack(side="right", anchor="e")
    remove.pack(side="right", anchor="e")
    menu.pack(side="right", anchor="e")
    # progress.pack(side="right", anchor="e")

    f.pack(side="top", fill="x")

    return dwl


def removeInstallEnty(answ, e_id, frame):
    global appList_json
    if answ == "no":
        return
    frame.pack_forget()
    appList_json.pop(e_id)
    saveAppList()


open_window()

openMenues = []


def openEditor(app):
    global openMenues, MF

    mFrame = Frame(MF, width=380, height=320, highlightbackground="black", highlightthickness=1, bd=0,
                   bg=Collor.bg.value)
    x, y = calcCenterXY(mFrame, w=380, h=320, )
    mFrame.place(x=x, y=y, width=380, height=320)

    f = Frame(mFrame, bg=Collor.bg_darker.value)
    f.pack(side="top", anchor="n", fill="x")

    B = Button(f, text="❌", relief="flat", bg=Collor.bg_darker.value, fg=Collor.fg.value,
               command=lambda: mFrame.place_forget())
    B.pack(side="right", anchor="ne")
    L3 = Label(f, text="Edit-Properties", relief="flat", bg=Collor.bg_darker.value, fg=Collor.fg.value,
               font=font_size_medium)
    L3.pack(side="left", anchor="nw")
    i1 = createInput(mFrame, "Version: ", str(app.spec["current_version"]), width=5, max_lines=1)
    i2 = createInput(mFrame, "Url :", app.spec["Url"], max_lines=4)
    i3 = createInput(mFrame, "Location :", app.spec["location"], max_lines=3)
    BSave = Button(master=mFrame, text="Save", relief="flat", bg=Collor.bg_darker.value, fg=Collor.fg.value,
                   command=lambda: saveInputConf(mFrame, app, (i1, i2, i3)), font=font_size_medium)
    BSave.pack(side="bottom", anchor="se", pady=(0, 5), padx=(0, 5))


def saveInputConf(frame, app, inputs):
    i1, i2, i3 = inputs
    try:
        app.setVersion(i1.getValue())
        app.setUrl(i2.getValue())
        app.setInstallLocation(i3.getValue())
        app.saveSpec()

        frame.place_forget()


    except Exception:

        displayErr("  Unable to Save at -> [057]  ")
        pass  # TODO


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
    def __init__(self, max_lines, width2=0, start=None, **kw):
        super().__init__(bg=Collor.bg_darker.value, fg=Collor.fg.value, font=font_size_medium, **kw)
        self.bind("<Return>", self.e)
        self.widthNum = width2
        self.max_lines = max_lines
        self.bind("<Key>", lambda u: gtk.after(10, self.updateHeight))
        if start:
            self.insert("0.0", start)
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
