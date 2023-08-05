import os
from tkinter import filedialog

def SaveData():
    global Active_Module
    DefaultFile = [('HistoClean File', '*.hc')]
    SavePath = filedialog.asksaveasfilename(initialdir=os.getcwd(), filetypes=DefaultFile, defaultextension=DefaultFile)
    print(f"Saving data to {SavePath}")
    Data = []

    if Active_Module == "Patch":
        Data.append("Patch")
        # Data.append(SettingValues)

