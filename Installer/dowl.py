
import copy
import json
import os
import threading
import urllib
import zipfile
import urllib.error as urle
from urllib import request
from tkinter import Frame, font as tkfont, filedialog as fd, Tk, Label, Button, PhotoImage, Text, Widget, END, \
    messagebox, ttk
from customWigets import BetterButton,Collor
import requests

targetLocation = ""

dic={}
def await_request(tk, comp=(),trgloc=""):
    global targetLocation,dic
    targetLocation=trgloc

    Err = [False]

    dic = {
        "n-dwl":False,
        "st-dwl": [False,0,0 ],
        "f-dwl": False,
        "chi":False,
        "st-unzip": False,
        "f-unzip": False,
        "st-reg": False,
        "fin": False,
        "last":False

    }
    tr = threading.Thread(target=get_updateRequest, args=(
    "https://packthecommand.000webhostapp.com/Software/Update/2lk67o30wu376sn27xajwj8289dsuih2z98dw8q9i2uh3e4ezu989dz8723197/version_data/mitive_dev.latest",
    Err, ))
    tr.start()

    def awaitChecker(tk,  Err,comp,workingLibrary={}):
        global dic
        status,mainFrame=comp
        if (Err[0] != False):
            return Err
            print("runtime 1321")

        if (dic["st-dwl"][0]==False):
            status.configure(text="Downloading files ...")


        if ((dic["st-dwl"][0])&(not dic["n-dwl"])):
            print(dic["st-dwl"][2], dic["st-dwl"][1])

            dic["n-dwl"]=True
            f = Frame(mainFrame, width=10)
            workingLibrary["f"]=f
            workingLibrary["pb"]=pb = ttk.Progressbar(
                f,
                orient='horizontal',
                mode='determinate',
                length=500,


            )
            pb.pack()


            #pb.start(500)
            f.pack()
            pass
        if (not dic["f-dwl"])&dic["n-dwl"]:
            #workingLibrary["pb"]['value'] = 100


            pass
            calc_now = ((dic["st-dwl"][2] / dic["st-dwl"][1])*100)//1
            workingLibrary["pb"]['value']=calc_now
            #print("calcing", calc_now)
        if (dic["f-dwl"])&(not dic["chi"]):
            dic["chi"]=True



            status.configure(text="dONE DOWNL ...")

        if (dic["chi"]&(not dic["fin"])):
            workingLibrary["pb"]['value'] = 0
            workingLibrary["pb"].configure(mode='indeterminate')
            workingLibrary["pb"].start(5)

        if (dic["fin"]&(not dic["last"])):
            dic["last"]=True
            status.configure(text="Finished Installation")
            workingLibrary["pb"].pack_forget()
            workingLibrary["f"].pack_forget()
            BetterButton(master=mainFrame, bg=Collor.bg_selected.value, text="Finish",
                         highlightcolor="black",
                         fg=Collor.fg_inverted.value,
                         command=tk.destroy).pack(
                side="bottom", anchor="se", padx=(0, 5), pady=(0, 5))




            """match rc[0]:
                case "st-dwl":
                    if workingLibrary
                        status.configure(text="Downloading-Files ...")
                        f=Frame(mainFrame,width=20)
                        pb = ttk.Progressbar(
                            f,
                            orient='horizontal',
                            mode='determinate',
                            length=result[1]

                        )
                        pb.pack()
                        workingLibrary[0]
                    pass
                case "f-dwl":
                    status.configure(text="Finished-Download ...")
                    pass
                case "st-unzip":
                    status.configure(text="Unzipping ...")
                    pass
                case "f-unzip":
                    status.configure(text="Done unzipping ...")
                    pass
                case "st-reg":
                    status.configure(text="Creating Key-elements ...")
                    pass

                case "--fin":
                    status.configure(text="Finished Installation")
                    BetterButton(master=mainFrame, bg=Collor.bg_selected.value, text="Finish",
                                 highlightcolor="black",
                                 fg=Collor.fg_inverted.value,
                                 command= tk.destroy).pack(
                        side="bottom",anchor="se", padx=(0, 5), pady=(0, 5))
                    print("done")"""


        tk.after(100, lambda: awaitChecker(tk,  Err,comp,workingLibrary))
    awaitChecker(tk,Err,comp)

def get_updateRequest(Url, Err=[False], ):

    global targetLocation,dic,data

    try:
        log = request.urlopen(Url)
    except urle.URLError:
        Err[0] = "Unable to reach server"
        return False
    tdata = log.read()
    tdata = tdata.decode('utf-8')
    tdata = tdata.replace("\n", "")
    print(tdata)
    data = json.loads(tdata)[0]
    update_version = float(data["version"])

    # with open("install_manifests.json", "w") as f:
    do_download(targetLocation, dic, Err)
    print(data)
    #    f.write(data)

    # return data


data = {}


# todo all
def do_download(installation_location, dic, Err=[False]):
    global localSpeck, data

    try:
        # with open("install_manifests.json", "r") as f:
        #    infos = json.load(f)[0]

        dowl_url = data["downl"]
        install_file = requests.get(dowl_url, stream=True)

    except Exception:

        Err[0] = "Error: Domane or side is offline (unable to get version-file)"
        return

    try:
        with open("installation_local_update.zip", "wb") as f:
            print("got_total_size")
            #lenF = len(install_file.content)
            #print(lenF)


            dic["st-dwl"][1] = int(install_file.headers["Content-Length"])+1

            dic["st-dwl"][2] = 1# done already size
            dic["st-dwl"][0] = True
            for installChunk in install_file.iter_content(chunk_size=1024):

                if installChunk:
                    dic["st-dwl"][2] += 1024
                    #print(dic["st-dwl"][2])
                    f.write(installChunk)
            dic["f-dwl"] = True
        print("start download")
    except Exception as e:
        print("Err", repr(e))
        Err[0] = "Error: Domane or side is offline (Unable to download Update package)."
        return
    try:
        try:
            os.mkdir(installation_location)
        except FileExistsError:
            pass
        dic["st-unzip"] = True
        with zipfile.ZipFile("installation_local_update.zip", 'r') as zip_ref:
            zip_ref.extractall(installation_location)
            print("e", installation_location)
        dic["f-unzip"] = True


    except Exception as e:
        print(e)
        Err[0] = "Error: Unable to Unzip files to target Location."
        return

    dic["st-reg"] = True
    cleanup()
    with open(installation_location + "\instance.spec", "w") as f:
        localSpeck = {"current_version": data["version"], "location": installation_location,
                      "Url": "https://packthecommand.000webhostapp.com/Software/Update/2lk67o30wu376sn27xajwj8289dsuih2z"+
                             "98dw8q9i2uh3e4ezu989dz8723197/version_data/mitive_dev.latest",
                      "overwrite": {"force_install": False}}

        json.dump([localSpeck], f)
    dic["fin"] = True
def cleanup():
    try:
        os.remove("installation_local_update.zip")
    except Exception:
        pass