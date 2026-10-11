import json,os,pickle,getpass
path=os.path.expanduser("~/.varlang")
with open(path+"/settings.json","w") as f:
    data={"hidedunder":["hide dunders in lists",True],"tipson":["enable tips",True],"soundon":["enable sound",True]}
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
        "don't use this for exploits",
        "take care of yourself because somebody cares about you",
        "despite everything, it's still you",
        "ERROR 404",
        "you can start again tomorrow",
        "your worth isn't measured by your achievements",
        "you don't have to figure everything out today",
        "love yourself",
        "thank you for trying out this program",
        "your feelings matter",
        "you don't have to be perfect to be enough",
        "a bad day doesn't make a bad life",
        "you are more than your mistakes",
        "there is always room for one more at the table",
        f"thank you {getpass.getuser()}"]
    pickle.dump(data,f)
with open(path+"/valid.txt","w") as f:
    f.write("this file proves that you did the setup")