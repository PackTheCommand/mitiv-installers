import enum
from tkinter import font as tkfont
import json
import os
import threading
import tkinter.ttk
from tkinter import Tk, ttk, Label, Button,messagebox

import requests
import urllib.request
import urllib.error as urle
import zipfile

#from sys import argv

localSpeck=None
localSpeck=None

mode = "dark"


class collor(enum.Enum):
    if mode == "dark":
        bg = "#232327"
        bg_darker = "#232327"
        fg = "silver"
        bg_cancel = "#3d3d3d"
        bg_reinst = "#212121"
        fg_reinst = "#181818"
    else:
        bg = "#E0E0E0"
        bg_darker = bg
        fg = "#161616"
        bg_cancel = bg
        bg_reinst = "#CECECE"
        fg_reinst = "#B5B5B5"


def check_for_Updates(curent_version: str, return_values,Url):

    try:
        log = urllib.request.urlopen(Url)
    except urle.URLError:
        return_values[0] = (False, -404.0)
        return
    data = log.read()
    data = data.decode('utf-8')
    data = data.replace("\n", "")
    print(data)
    latest_log = json.loads(data)[0]
    update_version = float(latest_log["version"])
    if update_version > float(curent_version):
        with open("update_mainfest.json", "w") as f:
            f.write(data)
        return_values[0] = (True, update_version)
        return
    return_values[0] = (False, update_version)
    return


installation_location = None


def do_Update(args, Err=False):
    global installation_location, closeButton,localSpeck
    dic = {"finisched_download": False,
           "progress": 0,
           "finisched_Moving": False,
           "point": 0,
           "version": (args[0], args[1]),
           "Error": False
           }


    try:
        with open("update_mainfest.json", "r") as f:
            infos = json.load(f)[0]
            dowl_url = infos["downl"]
        """install_file = urllib.request.urlopen(dowl_url)
        len=install_file.length"""
        install_file = requests.get(dowl_url, stream=True)
    except Exception:
        dic["Error"] = "Error: Domane or side is offline (unable to get version-file)"
        return

    try:
        with open("installation_local_update.zip", "wb") as f:
            lenF = len(install_file.content)
            print(lenF)
            dic["total"] = lenF
            t = threading.Thread(target=updateInfo_window, args=(dic,))
            t.start()

            if Err:
                dic["Error"] = "Newest version already installed"
                return
            for data in install_file.iter_content(chunk_size=1024):

                if data:
                    dic["progress"] += 1024
                    f.write(data)
            dic["finisched_download"] = True
    except Exception:
        dic["Error"] = "Error: Domane or side is offline (Unable to download Update package)."
        return
    try:
        closeButton["state"] = "disabled"
        with zipfile.ZipFile("installation_local_update.zip", 'r') as zip_ref:
            zip_ref.extractall(installation_location)
            print("e",installation_location)
        dic["finisched_Moving"] = True


    except Exception as e:
        print(e)
        dic["Error"] = "Error: Unable to Unzip files to target Location."
        return

    with open("instance.spec", "w") as f:
        print(localSpeck)
        localSpeck["current_version"]=args[1]

        json.dump([localSpeck], f)
    closeButton.configure(text="close")


# ---------------------------------------------------
def cleanup():
    try:
        os.remove("installation_local_update.zip")
    except Exception:
        pass


def null():
    pass


gtk = None
closeButton:list = None
BU = None


def open_window(install_location_):
    global closeButton


    tk = Tk()
    tk.title("Update")
    tk.configure(background=collor.bg.value)
    tk.wm_geometry("260x280+%d+%d" % (-800, -800))

    tk.resizable(False, False)
    tk.after(50, lambda: open_window_2(tk))
    tk.mainloop()


buttonFrame = None


def open_window_2(tk):
    global gtk, closeButton, buttonFrame
    gtk = tk
    subInfo = tkfont.Font(family="Bahnschrift", size=12, weight="bold")
    tk.wm_geometry("+%d+%d" % (tk.winfo_screenwidth() // 2.4, tk.winfo_screenheight() // 2.8))
    titelF = tkfont.Font(family="Bahnschrift", size=18, weight="bold")

    labout=Label(tk,text="about", font=subInfo, bg=collor.bg.value, fg=collor.fg.value, )
    labout.pack(side="top",anchor="ne")
    def temp_show_creadits(u):#
        tkinter.messagebox.showinfo("Credits (Temp)","Developed by: \n"+
                                    " PackTheCommand \n"+
                                    "Icons By :\n"+
                                    "  ICONS8 ( https://icons8.de ) ")


    labout.bind("<Button-1>",temp_show_creadits)


    tL = Label(font=titelF, bg=collor.bg.value, fg=collor.fg.value, text="Checking for updates")
    tL.pack(side="top")
    buttonFrame = tkinter.Frame(tk, bg=collor.bg.value)
    buttonFrame.pack(side="bottom", anchor="n", fill="x")
    B = Button(buttonFrame, text="cancel", font=tkfont.Font(family="Bahnschrift", size=12, weight="bold"),
               relief="solid",
               command=tk.destroy, bg=collor.bg_cancel.value, fg=collor.fg.value, )
    B.pack(side="right", anchor="e", padx=(0, 3), pady=(0, 3))
    tk.after(50, lambda: open_window_3(tk, tL, B))
    closeButton = B


def open_window_3(tk, tL, B):
    global mode,localSpeck,installation_location
    subInfo = tkfont.Font(family="Bahnschrift", size=12, weight="bold")

    try:
        i = tkinter.PhotoImage(master=tk, file="icon.png")
        tk.iconphoto(False, i)
    except Exception:
        pass
    try:
        with open("instance.spec", "r") as f:
            localSpeck=softwareSpec = json.load(f)[0]
            Url=softwareSpec["Url"]
            installation_location=softwareSpec["location"]
            cv = softwareSpec["current_version"]
        liste_ret = [False]
    except Exception as e:
        print(e)
        tL.configure(text="Unable to Update", )
        L = Label(font=subInfo, bg=collor.bg.value, fg=collor.fg.value, text="Aplication-spec file missing or curupted")
        return
    t = threading.Thread(target=send_request_for_update_info, args=(liste_ret, cv,Url))
    t.start()
    if mode == "dark":

        loading_photo_img_list = [
            tkinter.PhotoImage(master=tk, file="resources/L0.png", ),
            tkinter.PhotoImage(master=tk, file="resources/L1.png"),
            tkinter.PhotoImage(master=tk, file="resources/L2.png"),
            tkinter.PhotoImage(master=tk, file="resources/L3.png"),
        ]
    else:
        loading_photo_img_list = [
            tkinter.PhotoImage(master=tk, file="resources/L0_l.png", ),
            tkinter.PhotoImage(master=tk, file="resources/L1_l.png"),
            tkinter.PhotoImage(master=tk, file="resources/L2_l.png"),
            tkinter.PhotoImage(master=tk, file="resources/L3_l.png"),
        ]
    LodingL = Label(tk, image=loading_photo_img_list[0], borderwidth=0)
    LodingL.pack(side="top", pady=(30, 0))
    tk.after(100,
             lambda: wait_request_result(liste_ret, cv, tL, tk, softwareSpec, 0, loading_photo_img_list, LodingL, 0))


def wait_request_result(L, cv, tL, tk, softwareSpec, lodingImg_state, loading_img_list, LodingL, img_now):
    result_request = L[0]
    lodingImg_state += 1

    if result_request:
        tr, newV = result_request
        comp = (tL, tk, cv, softwareSpec)
        after_Update_url_request(tr, newV, comp)
        LodingL.pack_forget()
        loading_img_list.clear()
        return

    if ((lodingImg_state // 10) != img_now):

        img_now += 1

        LodingL.configure(image=loading_img_list[img_now])
    elif lodingImg_state == 0:

        LodingL.configure(image=loading_img_list[img_now])

    if lodingImg_state == 39:
        lodingImg_state = -1
        img_now = 0

    tk.after(100, lambda: wait_request_result(L, cv, tL, tk, softwareSpec, lodingImg_state, loading_img_list, LodingL,
                                              img_now))


def send_request_for_update_info(L, cv,url):
    # tr, newV =
    check_for_Updates(cv, L,url)


def after_Update_url_request(tr, newV, comp):
    global BU, buttonFrame
    subInfo = tkfont.Font(family="Bahnschrift", size=12, weight="bold")
    tL, tk, cv, softwareSpec = comp
    data = (tr, newV, softwareSpec)
    closeButton.configure(text="close")
    if tr:
        tk.configure(cursor="")
        tL.configure(text="Update Avalable")
        Linfo = Label(tk, text="Do you want to Update?", bg=collor.bg.value, fg=collor.fg.value)
        Linfo.pack(side="top")

        def on_update_button_click(B, tL, Linfo, data):
            global BU, closeButton
            tk.protocol("WM_DELETE_WINDOW", null)
            closeButton.configure(text="cancel")

            tr, newV, softwareSpec = data
            tL.pack_forget()
            Linfo.pack_forget()
            BU.pack_forget()

            do_Update((cv, newV, softwareSpec))

        B1 = Button(tk, font=subInfo, text="Update",
                    command=lambda: on_update_button_click(closeButton, tL, Linfo, data),
                    bg=collor.bg_darker.value, fg=collor.fg.value, relief="solid")
        BU = B1
        B1.pack(side="top", anchor="center")
    else:
        if (newV == -404.0):
            tL.configure(text="Error")
            Linfo = Label(tk, text="Unable to reach Update-URL", bg=collor.bg.value, fg=collor.fg.value, )
            Linfo.pack(side="top")
            tk.configure(cursor="")
            return

        def on_install_aniway_button_click(B, tL, Linfo, data):
            global BU, closeButton
            tk.protocol("WM_DELETE_WINDOW", null)
            closeButton.configure(text="cancel")
            tr, newV, softwareSpec = data
            tL.pack_forget()
            Linfo.pack_forget()
            BU.pack_forget()
            closeButton["state"] = "disabled"

            do_Update((cv, newV, softwareSpec))

        tL.configure(text="No Updates Found")

        Linfo = Label(tk, text="You are on the newest version", bg=collor.bg.value, fg=collor.fg.value, )
        Linfo.pack(side="top")
        tk.configure(cursor="")
        B1 = Button(buttonFrame, font=subInfo, text="Reinstall",
                    command=lambda: on_install_aniway_button_click(closeButton, tL, Linfo, data), borderwidth=0,
                    bg=collor.bg_reinst.value, fg=collor.fg_reinst.value, relief="solid")
        B1.pack(side="left", anchor="w", padx=(3, 0), pady=(0, 1))
        BU = B1


def updateInfo_window(data):
    global gtk, closeButton
    tk = gtk
    titelF = tkfont.Font(family="Bahnschrift", size=18, weight="bold")
    subInfo = tkfont.Font(family="Bahnschrift", size=12, weight="bold")
    v1, v2 = data["version"]
    tk.title(f"Ver {v1} -> {v2}")

    L = Label(tk, text="Update", font=titelF, bg=collor.bg.value, fg=collor.fg.value)
    LI = Label(tk, text="... update in progress",
               font=subInfo, bg=collor.bg.value, fg=collor.fg.value)

    L.pack(side="top")
    LI.pack(side="top")
    pb = ttk.Progressbar(
        tk,
        orient='horizontal',
        mode='determinate',
        length=data["total"]
    )

    pb.pack(fill="x", side="bottom")
    c = (closeButton, LI, L)

    tk.after(100, lambda: update_Progress(tk, pb, data, c, True))


def update_Progress(tk, pb: tkinter.ttk.Progressbar, data, c, first=False):
    global closeButton

    tk.after(500, lambda: update_Progress(tk, pb, data, c))

    if (not first) & (data["finisched_download"]):
        if (data["point"] < 1):
            c[1].configure(text="...installing")

            data["point"] = 1
        else:
            if (data["finisched_Moving"]):
                c[1].configure(text="... cleaning up")
                cleanup()

                closeButton["state"] = "active"
                tk.configure(cursor="")
                c[1].configure(text="✓ Done")
                tk.protocol("WM_DELETE_WINDOW", tk.destroy)
    else:
        err = data["Error"]
        p = pb['value'] = data["progress"]

        prozent = ((data["total"] / p) * 100) // 1
        print(data["total"] / 10, p, ":", prozent)
        if (prozent > 100.0):
            prozent = 100.0
        c[1].configure(text=f"{prozent}%...downloading")


open_window(r"C:\Users\ctind\PycharmProjects\Experimental\sned_recicve\install\\")
