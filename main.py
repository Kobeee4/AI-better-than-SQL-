import os
import sys
import time
from module import Shadow

def banner():
    R, W, G = '\033[31m', '\033[0m', '\033[32m'
    os.system('clear')
    print(fr"""{R}
   ██████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗
  ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║
  ╚█████╗ ███████║███████║██║  ██║██║   ██║██║ █╗ ██║
   ╚═══██╗██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║
  ██████╔╝██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝
  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ {W}
    """)
    print(f" {G}v3.1{W} | {G}3,150+ targets loaded{W}")
    print(f" status: {G}bypass_active{W}\n")

def main():
    try: s = Shadow()
    except ImportError: sys.exit()
    s.tos()
    
    while True:
        banner()
        print(" [1] scan_filesystem")
        print(" [2] ghost_request (URL)")
        print(" [3] read_logs")
        print(" [4] wipe_session")
        print(" [0] exit")
        
        try: cmd = input(f"\nroot@shadow:# ").strip()
        except: break

        if cmd == '1':
            p = input("\npath: ") or "."
            hits = s.breach(p)
            if hits:
                print(f"\n\033[32m[!] {len(hits)} hits\033[0m")
                for h in hits: print(f"  -> {h}"); s.log(f"HIT:{h}")
            input("\n[enter]")

        elif cmd == '2':
            u = input("\ntarget_url: ")
            print("[*] bypassing cloudflare/security...")
            res = s.request(u)
            if res == b"error":
                print("\033[31m[!] failed\033[0m")
            else:
                print(f"\033[32m[!] {len(res)} bytes retrieved\033[0m")
                s.log(f"REQ_SUCCESS:{u}")
            input("\n[enter]")

        elif cmd == '3':
            if os.path.exists(s.gp):
                with open(s.gp, 'r') as f: print(f.read())
            input("\n[enter]")

        elif cmd == '4':
            if os.path.exists(s.gp): os.remove(s.gp)
            print("[*] session wiped")
            time.sleep(1)

        elif cmd == '0': sys.exit()
        os.system('clear')

if __name__ == "__main__":
    main()
