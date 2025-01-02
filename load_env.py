import os

def load_env(fname=".env"):
    
    data = []
    with open(fname,'r') as f:
        data = f.readlines()
    
    for l in data:
        if "=" in l:
            k, v = l.split("=")
        else:
            print(f"Invalid line: {l}, ignoring")
            continue
        os.environ[k] = v.strip()
