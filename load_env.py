import os

def load_env(fname=".env"):
    
    data = []
    with open(fname,'r') as f:
        data = f.readlines()
    
    for l in data:
        k, v = l.split("=")
        os.environ[k] = v.strip()
