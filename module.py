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
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        p = ['admin','backup','users','config','db','main','master','data','vault','auth','creds','shadow','root','sql','sys','secure','login','member','private','store','web','app','core','base','archive','dump','sync','meta','financial','api','v1','v2','old','temp','test']
        e = ['.db', '.sqlite', '.sql', '.bin', '.dat', '.db3', '.sqlite3', '.bak', '.sav', '.mdb', '.cfg', '.log', '.json', '.xml', '.tar.gz', '.zip']
        v = ['', '_old', '_backup']
        self.t = [x + z + y for x in p for z in v for y in e]
        self.gp = f"/tmp/.{self.sid}" if os.path.exists("/tmp") else f"./.{self.sid}"

    def tos(self):
        os.system('clear')
        R, W, Y = '\033[31m', '\033[0m', '\033[33m'
        print(f"{R}SHADOW{W}\n" + "-"*30 + f"\nsid: {self.sid}\n" + "-"*30)
        print(f"{R}you agree to not use this for any bad use{W}\n")
        c = input(f"proceed? ({Y}yes{W}/{R}no{W}): ").lower().strip()
        if c != 'yes': sys.exit()
        os.system('clear')

    def request(self, url, method="GET", data=None):
        try:
            hst = url.split("//")[-1].split("/")[0]
            pth = "/" + "/".join(url.split("//")[-1].split("/")[1:])
            ctx = ssl.create_default_context()
            ctx.set_ciphers('ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:AES128-GCM-SHA256:AES256-GCM-SHA384')
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((hst, 443), timeout=10) as s:
                with ctx.wrap_socket(s, server_hostname=hst) as ss:
                    req = (f"{method} {pth} HTTP/1.1\r\n"
                           f"Host: {hst}\r\n"
                           f"User-Agent: {self.ua}\r\n"
                           f"Accept: text/html,application/xhtml+xml,xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\n"
                           f"Accept-Language: en-US,en;q=0.5\r\n"
                           f"Upgrade-Insecure-Requests: 1\r\n"
                           f"Sec-Fetch-Dest: document\r\n"
                           f"Sec-Fetch-Mode: navigate\r\n"
                           f"Sec-Fetch-Site: none\r\n"
                           f"Sec-Fetch-User: ?1\r\n"
                           f"Connection: close\r\n\r\n")
                    ss.sendall(req.encode())
                    res = b""
                    while True:
                        chnk = ss.recv(4096)
                        if not chnk: break
                        res += chnk
                    
                    if b"CF-RAY" in res or b"cloudflare" in res.lower():
                        return self.solve_cf(res, url)
                    return res
        except: return b"error"

    def solve_cf(self, res, url):
        html = res.decode(errors='ignore')
        m = re.findall(r'(\d+[\+\-\*]\d+)', html)
        if m:
            sol = str(eval(m[0]))
            return self.request(f"{url}?answer={sol}")
        return res

    def solve(self, raw):
        try:
            d = raw.decode(errors='ignore')
            m = re.findall(r'(\d+[\+\-\*]\d+)', d)
            if m: return str(eval(m[0]))
        except: pass
        return "0"

    def breach(self, path):
        hits = []
        if not os.path.exists(path): return hits
        for root, dirs, files in os.walk(path):
            for f in files:
                if f in self.t: hits.append(os.path.join(root, f))
                else:
                    fp = os.path.join(root, f)
                    try:
                        if os.path.getsize(fp) < 5000000:
                            with open(fp, 'rb') as x:
                                h = x.read(512)
                                if any(s in h for s in [b"SQLite", b"SQL", b"PK\x03\x04"]): hits.append(fp)
                    except: pass
        return hits

    def log(self, msg):
        with open(self.gp, 'a') as f: f.write(f"[{time.ctime()}] {msg}\n")
