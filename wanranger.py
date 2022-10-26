from termcolor import cprint as cp
import subprocess
import multiprocessing.dummy as mp

running = []

class IP:
    def __init__(self, front):
        self.front = front
        self.reachable = []
        self.all_hosts = []
        if self.save_reachable_only = True

    def ping(self,rest_ip):
        ip = self.front + str(rest_ip)
        ping_reply = subprocess.run(["ping","-c","1", ip],stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        if ping_reply.returncode == 0:
            if ("unreachable" in str(ping_reply.stdout)):
                self.unreachable.append(ip)
            else:
                self.reachable.append(ip)

        elif ping_reply.returncode == 1:
            self.unreachable.append(ip)

    def save(self):
        # Sort the list to make it pretty
        self.reachable.sort()
        if self.save_reachable_only == True:
            with open("results_for_%s.txt","a") as res:
                for host in self.reachable:
                    res.write("Host - %s is reachable\n" % host)



#ips = ["185.152.%s.%s" %(I, X) for I in range(1,256) for X in range(1,256)]
#cp("%s" % (ips),"green")

Banner = "\n\n\t*****************\n" + \
             "\t* WAN-Ranger by *\n" + \
             "\t*  BloodiMooni  *\n" + \
             "\t*****************\n\n" + \
             "\n\tCTLR + C to exit\n\n"

while True:

    cp(Banner, "yellow")
    cp("IP-Range:","yellow")

    try:
        front = input()
        ip = IP(front)
        with open("result.txt","w+") as file:
            file.write("Scan start \n\n")

        pool = mp.Pool(254)
        pool.map(ip.ping,range(1,255))
        pool.close()
        pool.join()

        cp("\n ************ SCAN COMPLETE ************\n\n", "green")

    except KeyboardInterrupt:
        cp("\n\n[~] USER INTERRUPT - Exiting.","red")
        break
