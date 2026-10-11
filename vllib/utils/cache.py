import hashlib,marshal,os
PATH=os.path.expanduser("~/.varlang/cache")
os.makedirs(PATH,exist_ok=True)
def cache(filename):
    with open(filename,"rb") as f:
        src=f.read()
    srchash=hashlib.sha256(src).hexdigest()
    cachefile=os.path.join(PATH,srchash)
    if os.path.exists(cachefile):
        try:
            with open(cachefile,"rb") as f:
                return marshal.loads(f.read())
        except:
            pass
    code=compile(src,filename,"exec")
    with open(cachefile,"wb") as f:
        marshal.dump(code,f)
    return code


