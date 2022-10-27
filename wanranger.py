import time, subprocess, sys, os
from sys import platform

try:
    from termcolor import cprint as cp
except:
    subprocess.run(["pip","install","termcolor"])
try:
    import multiprocessing.dummy as mp
except:
    subprocess.run(["pip","install","multiprocessing"])


class IP:
    def __init__(self, ip_address, save_file):
        self.ip_address = ip_address
        self.host_address = self.ip_address.split(".")
        self.reachable = []
        self.unreachable = []
        self.save_file = save_file

    def ping(self,host):
        host_ip = "%s.%s.%s.%s" % (self.host_address[0],self.host_address[1],self.host_address[2],str(int(self.host_address[3])+host))
        ping_reply = subprocess.run(["ping","-c","1", "%s" % host_ip],stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        if ping_reply.returncode == 0:
            if ("unreachable" in str(ping_reply.stdout)):
                self.unreachable.append(host)
            else:
                self.reachable.append(host)

        elif ping_reply.returncode == 1:
            self.unreachable.append(host)

    def save(self):
        if self.save_file == True and len(self.reachable) > 0:
            with open("results_for_%s.txt" % self.ip_address ,"a") as res:
                res.write("\t## Scan for %s ##\n\n" % self.ip_address)
                res.write("\t ++ alive hosts ++\n")
                for host in self.reachable:
                    res.write("Host - %s.%s.%s.%s is reachable\n" % (self.host_address[0],self.host_address[1],self.host_address[2],host))


    def figure_out_type(self):
        if self.host_address[2] == "0" and self.host_address[3] == "0":
            return 16

        elif self.host_address[2] != "0" and self.host_address[3] == "0":
            return 24


def scan_16(ip,ip_address):
    for I in range(0,256):
        ip.host_address[2] = str(I)
        try:
            cp("[~] Started scan for %s.%s.%s.%s/16" % (ip.host_address[0],ip.host_address[1],ip.host_address[2],"0"),"green")
            pool = mp.Pool(254)
            pool.map(ip.ping,range(1,255))
            pool.close()
            pool.join()
            ip.reachable.sort()
            ip.unreachable.sort()

            if not len(ip.reachable) == 0:
                cp("\n\t++ Alive Hosts ++","green")
                for host in ip.reachable:
                    cp("[+] Host : %s.%s.%s.%s is up" % (ip.host_address[0],ip.host_address[1],ip.host_address[2],host), "green")

            else:
                cp("\n\t-- No alive hosts found --", "red")

            cp("\n ************ SCAN COMPLETE ************\n\n", "yellow")
            ip.save()
            ip.reachable = []
            ip.unreachable = []

        except KeyboardInterrupt:
            cp("\n\n[~] USER INTERRUPT - Exiting.","red")
            sys.exit(0)


def scan_24(ip,ip_address):
    try:
        cp("[~] Started scan for %s/24" % ip.ip_address,"green")
        pool = mp.Pool(254)
        pool.map(ip.ping,range(1,255))
        pool.close()
        pool.join()
        ip.reachable.sort()
        ip.unreachable.sort()

        cp("\n\t++ reachable ++","green")
        for host in ip.reachable:
            cp("[+] Host : %s.%s.%s.%s is up" % (ip.host_address[0],ip.host_address[1],ip.host_address[2],host), "green")

        cp("\n\t-- unreachable --", "red")
        for host in ip.unreachable:
            cp("[-] Host : %s.%s.%s.%s is down" % (ip.host_address[0],ip.host_address[1],ip.host_address[2],host), "red")

        cp("\n ************ SCAN COMPLETE ************\n\n", "yellow")
        ip.save()
        return True

    except KeyboardInterrupt:
        cp("\n\n[~] USER INTERRUPT - Exiting.","red")
        sys.exit(0)


Banner = '''
__      __ ___    _  _              ___     ___    _  _     ___     ___     ___
\ \    / //   \  | \| |     o O O  | _ \   /   \  | \| |   / __|   | __|   | _ \\
 \ \/\/ / | - |  | .` |    o       |   /   | - |  | .` |  | (_ |   | _|    |   /
  \_/\_/  |_|_|  |_|\_|   TS__[O]  |_|_\   |_|_|  |_|\_|   \___|   |___|   |_|_\\
_|"""""|_|"""""|_|"""""| {======|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|
"`-0-0-'"`-0-0-'"`-0-0-'./o--000'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'
                            MADE BY BloodiMooni#1001
'''

def banner(Banner,title=""):
    if platform == "linux" or platform == "linux2":
        os.system("clear")
    elif platform == "darwin":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")
    cp(Banner,"yellow")


try:
    banner(Banner)
    ip_address = sys.argv[1]
    save_file = sys.argv[2]

    ip = IP(ip_address,save_file)
    if "y" in save_file.lower():
        ip.save_file = True
        with open("results_for_%s.txt" % ip.ip_address ,"w+") as f:
            f.write("#########\tBeginning of scan for %s\t#########" % ip.ip_address)
    else:
        ip.save_file = False
    if ip.figure_out_type() == 24:
        scan_24(ip,ip_address)
    elif ip.figure_out_type() == 16:
        scan_16(ip,ip_address)

except:
    cp("Commandline arguments gave an error.","red")
    sys.exit(1)
