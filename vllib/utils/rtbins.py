import ast,os
from ..utils.sound import play
SOCKET=os.path.expanduser("~/.varlang/runtime.sock")
send=None
sugvar=None
tokens=None
arga=None
argb=None
rundata=None
hidedunder=None
stop=None
running=None
client=None
class config:
    def upd(a,b,c,d,e,f,g,h,i,j):
        global send,sugvar,tokens,arga,argb,rundata,hidedunder,stop,running,client
        send,sugvar,tokens,arga,argb,rundata,hidedunder,stop,running,client=a,b,c,d,e,f,g,h,i,j
def help():
    send("""help - prints help
list - lists the variables
get - gets a variable's value
set - modifies the value of a variable
type - gets the type of the variable
exists - checks if variable exists
stop - stops runtime
call - calls a function
tune - tests ffplay""")
def list():
    result=[]
    for name,val in rundata.items():
        if (arga not in ("var","func") and arga is not None and arga not in name) or (name.startswith("__") and name.endswith("__") and hidedunder) or (not callable(rundata[name]) and arga=="func") or (callable(rundata[name]) and arga=="var"):
            continue
        result.append(f"{name} = {val!r}")
    if result:
        send("\n".join(result))
    else:
        send("[!] no data")
def get():
    if arga in rundata:
        send(repr(rundata[tokens[1]]))
    else:
        if sugvar(tokens[1]):
            suggest=f", did you mean {sugvar(tokens[1])}"
        else:
            suggest=""
        send("[X] variable not found"+suggest)
def set_():
    try:
        rundata[arga]=ast.literal_eval(tokens[2])
    except:
        rundata[tokens[1]]=tokens[2]
def type_():
    if tokens[1] in rundata:
        send(type(rundata[tokens[1]]).__name__)
    else:
        if sugvar(tokens[1]):
            suggest=f", did you mean {sugvar(tokens[1])}"
        else:
            suggest=""
        send("[X] variable not found"+suggest)
def exists():
    if tokens[1] in rundata:
        send("true")
    else:
        send("false")
def del_():
    if tokens[1] in rundata:
        del rundata[tokens[1]]
    else:
        if sugvar(tokens[1]):
            suggest=f", did you mean {sugvar(tokens[1])}"
        else:
            suggest=""
        send("[X] variable not found"+suggest)
def stop_():
    stop()
def stats():
    datas=len(rundata)
    status="running" if running else "stopped"
    connection="connected" if client else "disconnected"
    send(f"namespace entries: {datas}\nstatus: {status}\nconnection: {connection}\nsocket path: {SOCKET}")
def call():
    if tokens[1] in rundata:
        func=rundata[tokens[1]]
        if callable(func):
            args=[]
            for arg in tokens[2:]:
                try:
                    args.append(ast.literal_eval(arg))
                except:
                    args.append(arg)
            result=func(*args)
            send(repr(result))
        else:
            send("[X] function not callable")
    else:
        if sugvar(tokens[1]):
            suggest=f", did you mean {sugvar(tokens[1],datatype='func')}"
        else:
            suggest=""
        send("[X] function not in runtime"+suggest)
def tune():
    play()
    