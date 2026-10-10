import curses,json,os
items={}
path=os.path.expanduser("~/.varlang/settings.json")
def settings():
    global items
    with open(path,"r") as f:
        items=json.load(f)
    curses.wrapper(main)
def main(stdscr):
    stdscr.keypad(True)
    selected=0
    while True:
        stdscr.clear()
        h,w=stdscr.getmaxyx()
        if w<10 or h<10:
            stdscr.addstr(0,0,"SMALL!")
        stdscr.addstr(0,0,"VarLang")
        stdscr.hline(1,0,curses.ACS_HLINE,w-1)
        lines=[]
        for _,val in items.items():
            lines.append(f"{val[0]} : {val[1]}")
        sy=(h-len(lines))//2
        for i,item in enumerate(lines):
            y=sy+i
            x=(w-len(item))//2
            if i==selected:
                stdscr.addstr(y,x,"> "+item,curses.A_REVERSE)
            else:
                stdscr.addstr(y,x,item)
        key=stdscr.getch()
        if key==ord("\x1b"):
            with open(path,"w") as f:
                json.dump(items,f)
            break
        if key==curses.KEY_UP:
            selected=(selected-1)%len(items)
        if key==curses.KEY_DOWN:
            selected=(selected+1)%len(items)
        if key==ord("\n"):
            name=list(items)[selected]
            items[name][1]=not items[name][1]