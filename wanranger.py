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
        current_ip = "%s.%s.%s.%s" % (self.host_address[0],self.host_address[1],self.host_address[2],"0")
        if self.save_file == True and len(self.reachable) > 0:
            with open("results_for_%s.txt" % current_ip ,"w+") as res:
                res.write("\t## Scan for %s ##\n\n" % self.ip_address)
                res.write("\t ++ alive hosts ++\n")
                for host in self.reachable:
                    res.write("Host - %s.%s.%s.%s is reachable\n" % (self.host_address[0],self.host_address[1],self.host_address[2],host))


    def figure_out_type(self):
        if self.host_address[2] == "0" and self.host_address[3] == "0":
            #cp("We have a B class network here.","blue")
            return 16

        elif self.host_address[2] != "0" and self.host_address[3] == "0":
            #cp("We have a C class network here.","blue")
            return 24


def clear():
    print("\n"*100)


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
                #for host in ip.unreachable:
                    #cp("[-] Host : %s.%s.%s.%s is down" % (ip.host_address[0],ip.host_address[1],ip.host_address[2],host), "red")

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


Banner = "\n\n\t*****************\n" + \
             "\t* WAN-Ranger by *\n" + \
             "\t*  BloodiMooni  *\n" + \
             "\t*****************\n\n" + \
             "\n\tCTLR + C to exit\n\n"


#try:
clear()
cp(Banner, "yellow")
ip_address = sys.argv[1]
save_file = sys.argv[2]

ip = IP(ip_address,save_file)
if "y" in save_file.lower():
    ip.save_file = True
else:
    ip.save_file = False
if ip.figure_out_type() == 24:
    scan_24(ip,ip_address)
elif ip.figure_out_type() == 16:
    scan_16(ip,ip_address)

#except:
#    cp("Commandline arguments gave an error.","red")
#    sys.exit(1)
