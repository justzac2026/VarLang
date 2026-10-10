import argparse,os
from .cmds.console import console
from .cmds.runtime import runtime
from .cmds.settings import settings
def main():
    with open(os.path.expanduser("~/.varlang/valid.txt"),"r") as f:
        if f.read()!="this file proves that you did the setup":
            print("[X] whoops! you didn't do the setup right? do the commands below this message\ncd <varlang path>\nchmod +x setup\n./setup --needed")
            return
    parser=argparse.ArgumentParser(description="VarLang - Lightweight Python runtime debugger")
    subparsers=parser.add_subparsers(dest="cmd")
    cmds={"runtime":{"func":runtime,"help":"starts runtime for a program","args":[("filename",{"help":"choose a program to run"})]},
        "console":{"func":console,"help":"starts up the console for runtime debugging","args":[]},
        "settings":{"func":settings,"help":"lets you change settings","args":[]}}
    for name,data in cmds.items():
        subparser=subparsers.add_parser(name,help=data.get("help",""))
        for argname, options in data.get("args",[]):
            subparser.add_argument(argname,**options)
        subparser.set_defaults(func=data["func"],command_data=data)
    args=parser.parse_args()
    if not hasattr(args,"func"):
        parser.print_help()
        return
    data=args.command_data
    vals=[getattr(args,options.get("dest",argname.lstrip("-").replace("-","_"))) for argname,options in data.get("args",[])]
    return args.func(*vals)
if __name__=="__main__":
    raise SystemExit(main())