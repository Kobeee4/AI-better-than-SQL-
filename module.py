import os
import time
import socket
import ssl
import random
import re
import sys

class Shadow:
    def __init__(self, session_id=None):
        self.sid = session_id or str(int(time.time()))
        self.ua = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
        ]
        
        
        pre = [
            'admin','backup','users','config','db','main','master','data','vault','auth','creds','shadow','root','sql','sys','secure','login','member','private','store','web','app','core','base','archive','dump','sync','meta','financial','api','v1','v2','old','temp','test','client','server','local','remote','prod','dev','staff','internal','external','global','alpha','beta','finance','pay','node','cluster','edge','user_data','profile','session','secret','key','storage','cache','log','site','global','setup','recovery','billing','crm','portal','index','collection','warehouse','vault_key','master_db','access','engine'
        ]
        
        ext = ['.db', '.sqlite', '.sql', '.bin', '.dat', '.db3', '.sqlite3', '.bak', '.sav', '.mdb', '.cfg', '.log', '.json', '.tar.gz']
        
        var = ['', '_old', '_backup']
        
        

        self.t = [p + v + e for p in pre for v in var for e in ext]
        
        self.gp = f"/tmp/.{self.sid}" if os.path.exists("/tmp") else f"./.{self.sid}"

    def tos(self):
        os.system('clear')
        R, W, Y = '\033[31m', '\033[0m', '\033[33m'
        print(f"{R}SHADOW{W}")
        print("-" * 30)
        print(f"session_id: {self.sid}")
        print("-" * 30)
        print(f"{R}you agree to not use this for any bad use{W}")
        print("\nthis tool is for authorized testing only.")
        print("misuse is the sole responsibility of the user.")
        print("by typing 'yes' you accept all legal risks.")
        
        c = input(f"\nproceed? ({Y}yes{W}/{R}no{W}): ").lower().strip()
        if c != 'yes':
            sys.exit()
        os.system('clear')

    def request(self, url, method="GET", data=None):
        try:
            hst = url.split("//")[-1].split("/")[0]
            pth = "/" + "/".join(url.split("//")[-1].split("/")[1:])
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with socket.create_connection((hst, 443), timeout=10) as s:
                with ctx.wrap_socket(s, server_hostname=hst) as ss:
                    u = random.choice(self.ua)
                    req = f"{method} {pth} HTTP/1.1\r\nHost: {hst}\r\nUser-Agent: {u}\r\nConnection: close\r\n"
                    if data: req += f"Content-Length: {len(data)}\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{data}"
                    else: req += "\r\n"
                    ss.sendall(req.encode())
                    res = b""
                    while True:
                        chnk = ss.recv(4096)
                        if not chnk: break
                        res += chnk
                    return res
        except: return b"error"

    def solve(self, raw):
        try:
            d = raw.decode(errors='ignore')
            m = re.findall(r'(\d+[\+\-\*]\d+)', d)
            if m: return str(eval(m[0]))
            v = re.findall(r'name="captcha_val" value="(\w+)"', d)
            if v: return v[0]
        except: pass
        return "0"

    def breach(self, path):
        hits = []
        if not os.path.exists(path): return hits
        try:
            for root, dirs, files in os.walk(path):
                for f in files:
                    if f in self.t: hits.append(os.path.join(root, f))
                    else:
                        fp = os.path.join(root, f)
                        if os.path.getsize(fp) < 5000000:
                            with open(fp, 'rb') as x:
                                head = x.read(512)
                                if any(s in head for s in [b"SQLite", b"SQL", b"PK\x03\x04"]):
                                    hits.append(fp)
        except: pass
        return hits

    def log(self, msg):
        with open(self.gp, 'a') as f:
            f.write(f"[{time.ctime()}] {msg}\n")

if __name__ == "__main__":
    s = Shadow()
    s.tos()
    hits = s.breach(".")
    for hit in hits:
        s.log(hit)
