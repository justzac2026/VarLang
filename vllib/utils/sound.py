import subprocess,os
#just figured out i can make this as an alias
parent=os.path.dirname
PATH=f"{parent(parent(os.path.abspath(__file__)))}/assets/sounds"
def play(sound="success"):
    if not os.path.exists(os.path.abspath(f"{PATH}/{sound}.wav")):
        return
    subprocess.run(["ffplay","-nodisp","-autoexit",f"{PATH}/{sound}.wav"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)