import socket,threading,os,json,time,pickle,random,difflib,inspect,shlex
from ..utils import rtbins
from ..utils.sound import play
from ..utils.cache import cache
CMDS={name.rstrip("_"):val for name,val in vars(rtbins).items() if not name.startswith("__") and not name.endswith("__") and inspect.isfunction(val) and name!="config"}
SOCKET=os.path.expanduser("~/.varlang/runtime.sock")
running=True
rundata={}
client=None
clientlock=threading.Lock()
with open(os.path.expanduser("~/.varlang/settings.json"),"r") as f:
    data=json.load(f)
    hidedunder=data["hidedunder"][1]
    tipson=data["tipson"][1]
with open(os.path.expanduser("~/.varlang/tips.pkl"),"rb") as f:
    tips=pickle.load(f)

def tipper():
    while running:
        time.sleep(60)
        if not running:
            break
        send("[?] "+random.choice(tips))

def sugvar(name,datatype=None):
    names=[]
    for n in rundata:
        if (datatype=="func" and callable(rundata[n])) or (datatype=="var" and not callable(rundata[n])) or (not datatype):
            names.append(n)
    matches=difflib.get_close_matches(name,names,n=1,cutoff=0.5)
    if matches:
        return matches[0]
    return None

def send(msg):
    global client
    if client is None:
        return
    try:
        with clientlock:
            client.sendall((msg+"\n").encode())
    except Exception as e:
        print(f"[X] FATAL ERROR OCCURED.\nREASON: {e}")
        play(sound="error")

def run(filename):
    global rundata
    try:
        code=cache(filename)
        exec(code,rundata)
    except Exception as e:
        send(f"[X] FATAL ERROR OCCURED.\nREASON: {e}")
        play(sound="error")
    finally:
        stop()

def stop():
    global running
    running=False

def handlecmd(cmd):
    try:
        tokens=shlex.split(cmd)
        if not tokens:
            return
        inst=tokens[0]
        arga=tokens[1] if len(tokens)>1 else None
        argb=tokens[2] if len(tokens)>2 else None
        rtbins.config.upd(send,sugvar,tokens,arga,argb,rundata,hidedunder,stop,running,client)
        if inst in CMDS:
            CMDS[inst]()
        else:
            send("[X] command not found")
            play(sound="error")
    except Exception as e:
        send(f"[X] {e}")
        play(sound="error")

def handlecli(conn):
    global client
    client=conn
    try:
        while running:
            data=conn.recv(65536)
            if not data:
                break
            cmd=data.decode().strip()
            handlecmd(cmd)
    except Exception as e:
        print(f"[X] FATAL ERROR OCCURED. \nREASON: {e}")
        play(sound="error")

def runtime(filename):
    global rundata,running
    rundata={}
    running=True
    threading.Thread(target=run,args=(filename,),daemon=True).start()
    if os.path.exists(SOCKET):
        os.remove(SOCKET)
    server=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    server.bind(SOCKET)
    server.listen()
    if tipson:
        threading.Thread(target=tipper,daemon=True).start()
    print("[+] runtime started!")
    play()
    while running:
        try:
            conn,_=server.accept()
        except:
            if not running:
                break
        threading.Thread(target=handlecli,args=(conn,),daemon=True).start()
    server.close()
    if os.path.exists(SOCKET):
        os.remove(SOCKET)
    print("[+] runtime stopped")
    play()