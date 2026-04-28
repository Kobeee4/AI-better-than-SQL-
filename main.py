import os
import sys
import time
from module import Shadow

def banner():
    R, W, G = '\033[31m', '\033[0m', '\033[32m'
    os.system('clear')
    print(f"""{R}
   ██████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗
  ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║
  ╚█████╗ ███████║███████║██║  ██║██║   ██║██║ █╗ ██║
   ╚═══██╗██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║
  ██████╔╝██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝
  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ {W}
    """)
    print(f" {G}v1{W} | {G}ts "better" than sql{W}")
    print(f" status: {G}bypass_active{W}\n")

def main():
    s = Shadow()
    
    # mandatory agreement
    s.tos()
    
    while True:
        banner()
        print(f" [1] scan_filesystem")
        print(f" [2] ghost_request")
        print(f" [3] read_logs")
        print(f" [4] wipe_session")
        print(f" [0] exit")
        
        try:
            cmd = input(f"\nroot@shadow:# ").strip()
        except EOFError:
            break

        if cmd == '1':
            p = input("\npath: ") or "."
            print(f"[*] crawling {p}...")
            time.sleep(0.5)
            hits = s.breach(p)
            if hits:
                print(f"\n\033[32m[!] identified {len(hits)} targets:\033[0m")
                for h in hits:
                    print(f"  -> {h}")
                    s.log(f"HIT:{h}")
            else:
                print("\n[-] no signatures found.")
            input("\n[enter]")

        elif cmd == '2':
            u = input("\ntarget_url: ")
            print(f"[*] sending stealth_pkt to {u}...")
            res = s.request(u)
            if res == b"error":
                print("\033[31m[!] failed\033[0m")
            else:
                print(f"\033[32m[!] success\033[0m | {len(res)} bytes")
                if b"captcha" in res.lower():
                    print(f"[*] captcha_detected: solving...")
                    print(f"[*] sol: {s.solve(res)}")
                s.log(f"REQ:{u}")
            input("\n[enter]")

        elif cmd == '3':
            if os.path.exists(s.gp):
                print(f"\n--- {s.gp} ---")
                with open(s.gp, 'r') as f:
                    print(f.read())
            else:
                print("\n[-] no logs")
            input("\n[enter]")

        elif cmd == '4':
            confirm = input("\nconfirm wipe? (y/n): ")
            if confirm.lower() == 'y':
                if os.path.exists(s.gp):
                    os.remove(s.gp)
                print("[*] wiped")
                time.sleep(1)

        elif cmd == '0':
            sys.exit()

        os.system('clear')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] killed")
        sys.exit()
