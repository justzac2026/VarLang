import json,os,pickle
path=os.path.expanduser("~/.varlang")
with open(path+"/settings.json","w") as f:
    data={"hidedunder":["hide dunders in lists",True],"tipson":["enable tips",True]}
    json.dump(data,f)
with open(path+"/tips.pkl","wb") as f:
    data=["VarLang was supposed to be a coding language",
        "sockets are like friendships, they bond wirelessly and wirefully",
        "seeing [+] means it succeeded",
        "seeing [!] means you are warned",
        "seeing [?] means its a tip!",
        "seeing [X] means something went wrong",
        "the program runs on hopes and dreams",
        "bugs are temporary, VarLang is forever!",
        "tips sealed in a pickle jar",
        "TIP NOT FOUND",
        "NULL",
        "so much threads",
        "use Esc in console, CTRL+C in runtime",
        f"don't use this for exploits"]
    pickle.dump(data,f)
with open(path+"/valid.txt","w") as f:
    f.write("this file proves that you did the setup")
with open(path+"/path.txt","w") as f:
    f.write(os.path.dirname(os.getcwd())+"/vllib")