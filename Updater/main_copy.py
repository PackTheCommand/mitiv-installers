import json
import os
import threading
import tkinter.ttk
from tkinter import Tk, ttk, Label, Button
from tkhtmlview import HTMLLabel
import requests
import urllib.request
import zipfile



def Update(installation_location):
    def check_for_Updates(curent_version:str):
        Url=r"https://packthecommand.000webhostapp.com/Software/Update/2lk67o30wu376sn27xajwj8289dsuih2z98dw8q9i2uh3e4ezu989dz8723197/version_data/mitive_dev.latest"
        log=urllib.request.urlopen(Url)


        data=log.read()
        data=data.decode('utf-8')
        data=data.replace("\n","")
        print(data)
        latest_log = json.loads(data)[0]
        update_version=float(latest_log["version"])
        if update_version > float(curent_version):
            with open("update_mainfest.json","w") as f:
                f.write(data)
            return (True,update_version)
        return (False,update_version)


    def do_Update(args,Err=False):
        dic={"finisched_download":False,
             "progress":0,
             "finisched_Moving":False,
             "point":0,
             "version":(args[0],args[1]),
             "Error":False
             }
        try:
            with open("update_mainfest.json","r")as f:
                infos=json.load(f)[0]
                dowl_url=infos["downl"]
            """install_file = urllib.request.urlopen(dowl_url)
            len=install_file.length"""
            install_file = requests.get(dowl_url,stream=True)
        except Exception:
            dic["Error"]="Error: Domane or side is offline (unable to get version-file)"
            return

        try:
            with open("installation_local_update.zip","wb") as f:
                lenF=len(install_file.content)
                print(lenF)
                dic["total"]=lenF
                t=threading.Thread(target=updateInfo_window,args=(dic,))
                t.start()

                if Err:
                    dic["Error"] = "Newest version already installed"
                    return
                for data in install_file.iter_content(chunk_size=1024):

                    if data:
                        dic["progress"]+=1024
                        f.write(data)
                dic["finisched_download"] =True
        except Exception:
            dic["Error"]="Error: Domane or side is offline (Unable to download Update package)."
            return
        try:
            with zipfile.ZipFile("installation_local_update.zip", 'r') as zip_ref:
                zip_ref.extractall(installation_location)
            dic["finisched_Moving"]=True
            args[2]["curent_version"]=newV

        except Exception as e:
            print(e)
            dic["Error"]="Error: Unable to Unzip files to target Location."
            return

        with open("instance.spec", "w") as f:
            instance_info=[{"current_version":args[1]}]
            json.dump(instance_info,f)



#---------------------------------------------------
    with open("instance.spec","r") as f:
        softwareSpec=json.load(f)[0]
        cv=softwareSpec["current_version"]
    tr,newV=check_for_Updates(cv)

    if tr:


        do_Update((cv,newV,softwareSpec))


    else:
        do_Update((cv,newV,softwareSpec),Err=True)
    try:
        os.remove("installation_local_update.zip")
    except Exception:
        pass
def null():
    pass
def updateInfo_window(data):
    tk=Tk()
    v1,v2=data["version"]
    tk.resizable(False,False)
    tk.protocol("WM_DELETE_WINDOW", null)
    try:
        i=tkinter.PhotoImage(master=tk,file="icon.png")
        tk.iconphoto(False,i)
    except Exception:
        pass
    tk.title(f"Update {v1} -> {v2}")
    tk.configure(cursor="wait")
    tk.wm_geometry("300x200+%d+%d"% (tk.winfo_screenwidth()//2.4,tk.winfo_screenheight()//2.8))
    L=Label(tk,text="Update",font=tkinter.font.Font(family="Bahnschrift",size=18,weight="bold"),bg="#232327",fg="silver")
    LI = Label(tk, text="...Download",
              font=tkinter.font.Font(family="Bahnschrift", size=12, weight="bold"), bg="#232327", fg="silver")
    tk.configure(background="#232327")
    L.pack(side="top")
    LI.pack(side="top")
    pb = ttk.Progressbar(
        tk,
        orient='horizontal',
        mode='determinate',
        length=data["total"]
    )
    B=Button(tk,text="Close",font=tkinter.font.Font(family="Bahnschrift",size=10,weight="bold"),relief="solid",command=tk.destroy,bg="#3d3d3d",fg="silver")
    B.pack(side="bottom",anchor="se")
    pb.pack(fill="x",side="bottom")
    c = (B,LI,L)
    B["state"] = "disabled"

    tk.after(1000,lambda :update_Progress(tk,pb,data,c))
    tk.mainloop()
def update_Progress(tk,pb:tkinter.ttk.Progressbar,data,c):
    pb['value'] =data["progress"]
    tk.after(1000, lambda: update_Progress(tk, pb, data,c))
    err=data["Error"]
    if err:
        pb.pack_forget()
        c[1].configure(text=err)

        c[2].configure(text="Unable to Update")
        c[0]["state"] = "active"
        tk.configure(cursor="")
        return
    if(data["finisched_download"]):
        if(data["point"]<1):
            c[1].configure(text="...installing")
            c[0].configure(highlightcolor="blue")
            data["point"] = 1
        else:
            if(data["finisched_Moving"]):

                c[0]["state"] = "active"
                tk.configure(cursor="")
                c[1].configure(text="✓ Done")
Update(r"C:\Users\ctind\PycharmProjects\Experimental\sned_recicve\install\\")


