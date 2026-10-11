import socket,curses,textwrap,threading,os
from ..utils.sound import play
SOCKET=os.path.expanduser("~/.varlang/runtime.sock")
tipon=False
tips=[]
client=None
running=True
output=[]
outlock=threading.Lock()
def recv():
    global running
    buffer=""
    while running:
        try:
            data=client.recv(65536)
            if not data:
                prnt("[!] runtime disconnected")
                play(sound="warning")
                running=False
                break
            buffer+=data.decode()
            while "\n" in buffer:
                line,buffer=buffer.split("\n",1)
                prnt(line)
        except:
            if running:
                prnt("[X] connection lost")
                play(sound="error")
            running=False
            break
def connect():
    global client
    client=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    client.connect(SOCKET)
    threading.Thread(target=recv,daemon=True).start()
def send(cmd):
    try:
        client.sendall((cmd+"\n").encode())
    except Exception as e:
        prnt(f"[X] FAILED TO SEND COMMAND.\nREASON: {e}")
        play(sound="error")
def prnt(txt):
    with outlock:
        output.extend(txt.splitlines())
def console():
    try:
        connect()
    except:
        print("[X] runtime isn't running")
        play(sound="error")
        return 1
    curses.wrapper(main)
def main(stdscr):
    global running
    curses.curs_set(1)
    stdscr.keypad(True)
    curses.halfdelay(1)
    cursor=0
    cmd=""
    scroll=0
    inpscroll=0
    #lol means last output length not laughing out loud
    lol=0
    while True:
        stdscr.clear()
        h,w=stdscr.getmaxyx()
        if h<10 or w<10:
            try:
                stdscr.addstr(0,0,"SMALL!")
            except:
                pass
            continue
        stdscr.addstr(0,0,"VarLang")
        stdscr.hline(1,0,curses.ACS_HLINE,w-1)
        with outlock:
            curout=output.copy()
        outh=h-4
        displines=[]
        for line in curout:
            displines.extend(textwrap.wrap(line,width=max(1,w-1))or[""])
        maxscroll=max(0,len(displines)-outh)
        if len(displines)>lol:
            scroll=maxscroll
            lol=len(displines)
        scroll=min(scroll,maxscroll)
        for i in range(outh):
            index=scroll+i
            if index>=len(displines):
                break
            stdscr.addstr(2+i,0,displines[index])
        stdscr.hline(h-2,0,curses.ACS_HLINE,w-1)
        visiw=max(1,w-3)
        if cursor<inpscroll:
            inpscroll=cursor
        if cursor>=inpscroll+visiw:
            inpscroll=cursor-visiw+1
        visicmd=cmd[inpscroll:inpscroll+visiw]
        stdscr.addstr(h-1,0,("> "+visicmd)[:max(1,w-1)])
        stdscr.move(h-1,2+cursor-inpscroll)
        key=stdscr.getch()
        if key==ord("\x1b"):
            break
        elif key==ord("\n"):
            if cmd:
                prnt(f"> {cmd}")
                result=send(cmd)
                cmd=""
                cursor=0
        elif key in (ord("\b"),curses.KEY_BACKSPACE,127):
            if cursor>0:
                cmd=cmd[:cursor-1]+cmd[cursor:]
                cursor-=1
        elif key==curses.KEY_UP:
            scroll=max(0,scroll-1)
        elif key==curses.KEY_DOWN:
            scroll=min(maxscroll,scroll+1)
        elif key==curses.KEY_LEFT:
            cursor=max(0,cursor-1)
        elif key==curses.KEY_RIGHT:
            cursor=min(len(cmd),cursor+1)
        elif key==ord("\x0c"):
            output.clear()
            scroll=0
            lol=0
        elif key:
            keyallow=False
            try:
                key=chr(key)
                keyallow=key.isprintable() and key.isascii()
            except:
                pass
            if keyallow:
                cmd=cmd[:cursor]+key+cmd[cursor:]
                cursor+=1
            

