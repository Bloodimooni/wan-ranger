import time, subprocess, sys
# Importing more libraries, if they don't exist we try to install them using pip
try:
    from termcolor import cprint as cp
except:
    subprocess.run(["pip","install","termcolor"])
try:
    import multiprocessing.dummy as mp
except:
    subprocess.run(["pip","install","multiprocessing"])


class IP:
    def __init__(self, front, save_reachable_only):
        self.front = front
        self.reachable = []
        self.unreachable = []
        self.save_reachable_only = True

    def ping(self,host):
        ip = self.front + str(host)
        ping_reply = subprocess.run(["ping","-c","1", ip],stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        if ping_reply.returncode == 0:
            if ("unreachable" in str(ping_reply.stdout)):
                self.unreachable.append(host)
            else:
                self.reachable.append(host)

        elif ping_reply.returncode == 1:
            self.unreachable.append(host)

    def save(self):
        with open("results_for_%s.txt" % self.front,"w+") as file:
            file.write("Scan start \n\n")

        if self.save_reachable_only == True:
            with open("results_for_%s.txt" % self.front,"a") as res:
                for host in self.reachable:
                    res.write("Host - %s%s is reachable\n" % (self.front,host))
        else:
            with open("results_for_%s.txt" % self.front,"a") as res:
                res.write("\t ++ alive hosts ++\n")
                for host in self.reachable:
                    res.write("Host - %s%s is reachable\n" % (self.front,host))
                res.write("\n\t -- down hosts --\n")
                for host in self.unreachable:
                    res.write("Host - %s%s is unreachable\n" % (self.front,host))





def clear():
    print("\n"*100)

Banner = "\n\n\t*****************\n" + \
             "\t* WAN-Ranger by *\n" + \
             "\t*  BloodiMooni  *\n" + \
             "\t*****************\n\n" + \
             "\n\tCTLR + C to exit\n\n"



while True:
    try:
        clear()
        cp(Banner, "yellow")

        cp("IP-Range:","yellow")
        front = input()

        cp("Only save reachable hosts? (yes/no)","yellow")
        reachable_only = input()

        if "y" in reachable_only.lower():
            reachable_only = True
        else:
            reachable_only = False

        ip = IP(front,reachable_only)
        pool = mp.Pool(254)
        pool.map(ip.ping,range(1,255))
        pool.close()
        pool.join()
        ip.reachable.sort()
        ip.unreachable.sort()

        cp("\n\t++ reachable ++","green")
        for host in ip.reachable:
            cp("[+] Host : %s%s is up" % (ip.front,host), "green")

        cp("\n\t-- unreachable --", "red")
        for host in ip.unreachable:
            cp("[-] Host : %s%s is down" % (ip.front,host), "red")

        cp("\n ************ SCAN COMPLETE ************\n\n", "yellow")
        ip.save()
        break

    except KeyboardInterrupt:
        cp("\n\n[~] USER INTERRUPT - Exiting.","red")
        break
