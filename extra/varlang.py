#!/usr/bin/env python3
import os,sys
sys.path.insert(0,os.path.expanduser("~/.local/lib"))
from vllib.main import main
if __name__=="__main__":
    raise SystemExit(main())