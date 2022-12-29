import enum
from tkinter import Frame, Label, font as tkfont, Button


mode="dark"
def setMode(mo):
    global mode
    mode=mo
font_size_large = None
font_size_medium = None
def initialize():
    global font_size_medium,font_size_large
    font_size_large = tkfont.Font(family="Bahnschrift", size=18, weight="bold")
    font_size_medium = tkfont.Font(family="Bahnschrift", size=12, weight="bold")


class optionButton(Frame):
    def __init__(self, name, chosen: int = None, chosenStr=None, onChange=None, options=[], **kw):
        super().__init__(**kw)
        self.names = options
        self.optItems = []
        self.onChange = onChange
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
        if self.onChange != None:
            self.onChange(n)
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


class Collor(enum.Enum):
    if mode == "dark":
        bg = "#232327"
        bg_darker = "#151517"
        fg = "silver"
        fg_inverted = "#161616"
        bg_cancel = "#3d3d3d"
        bg_reinst = "#212121"
        bg_selected = "#80868a"
        fg_reinst = "#181818"
        err_color = "#AA1F2B"
    else:
        bg = "#E0E0E0"
        bg_darker = "#94999c"
        fg = "#161616"
        fg_inverted = "silver"
        bg_cancel = bg
        bg_selected = "#505457"
        bg_reinst = "#CECECE"
        fg_reinst = "#B5B5B5"
        err_color = "#FF4460"


class BetterButton(Button):
    def __init__(self, bg=Collor.bg_darker.value, fg=Collor.fg.value, **kn):
        super().__init__(bg=bg, fg=fg,
                         highlightbackground=Collor.err_color.value, highlightthickness=1, bd=0, font=font_size_medium,
                         **kn)
