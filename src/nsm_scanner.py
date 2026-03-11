# THIS WILL BE A TEST SCRIPT FOR NETBRUTER2.0



# UI IMPORTS
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
import pyfiglet


# NETWORK IMPORTS
import ipaddress, socket, requests
from scapy.all import IP, TCP, sr1


# ETC IMPORTS
import time, random, threading, sys, concurrent.futures; from pybloom_live import BloomFilter
from concurrent.futures import ThreadPoolExecutor, as_completed


# NSM IMPORTS
from nsm_database import File_Saver, Database

console = Console()
LOCK = threading.Lock()


class Mass_IP_Scanner_old():
    """This class will be responsible for finding active ips on user choosen port"""

    
    # ARGS
    country = False
    asn     = False
    lookup  = False

    all     = False
    save    = False
    bloom_size = 100000000


    # MODES
    iot = False
    nas = False
    router = False
    remote = False
    camera = False
    database = False


    # IPS
    #total_ips        = 0
    total_blocks     = []
    ips_from_block   = 0
    current_block    = False
    blocks_done      = 0
    bf_all = None



    @classmethod
    def _track_ip_blocks(cls):
        """Return a random IP from the current block"""

        try:

            if not hasattr(cls, "bf") or cls.bf is None:
                network = ipaddress.IPv4Network(cls.blocks[0])
                cls.bf = BloomFilter(capacity=network.num_addresses * 2, error_rate=0.001)
                cls.total_blocks = cls.blocks.copy()


            if cls.ips_from_block <= 0:

                if not cls.blocks:
                    if cls.scan: console.print(f"[bold green][+] Scan complete | Total IPv4s:[/bold green] {cls.scanned_ips} | Blocks: {len(cls.total_blocks)}")
                    cls.scan = False; return False


                cls.current_block = cls.blocks.pop(0)

                network = ipaddress.IPv4Network(cls.current_block)
                cls.ips_from_block = network.num_addresses

                cls.bf = BloomFilter(capacity=cls.ips_from_block * 2, error_rate=0.001)

                console.print(f"\n[bold green][*] Current IPv4 Block:[yellow] {cls.current_block}  -  IPv4 Addresses: {ipaddress.IPv4Network(cls.current_block).num_addresses}\n")                
                time.sleep(1)



            network = ipaddress.IPv4Network(cls.current_block)

            random_ip = ipaddress.IPv4Address(random.randint(int(network.network_address), int(network.broadcast_address)))

            if random_ip in cls.bf: return False

            cls.bf.add(random_ip)
            cls.ips_from_block -= 1; cls.scanned_ips += 1
            cls.last_scan += 1

            return str(random_ip)

        except Exception as e:
            console.print(f"[bold red]IP Exception:[/bold red] {e}")
            return False


    @classmethod
    def _generate_random_ip(cls, verbose=False):
        """This will generate a random ip and return it"""
        

        try:


            # I USUALLY DONT USE COMMENTS SINCE THERE FOR SKIDS
            # BUT THIS WAS EXTREMELY COMPLEX CODE TO DESIGN/DEBUG
            if cls.country:

                
                with LOCK:
                    return Mass_IP_Scanner._track_ip_blocks()


                
                """

                // THE METHOD BELOW IS NOW DEAPPRECIATED, WILL BE KEEPING FOR DOCUMENTATION

                network = [ipaddress.IPv4Network(str(block)) for block in cls.current_block]
                network = random.choice(network)

                # PICK A RANDOM NUMBER BETWEEN THE NETWORKS START AND END IP (AS INTEGERS) 
                # EXAMPLE --> 122.X.X.122  //  122 == START / 122 == END
                random_ip_int = random.randint(int(network.network_address), int(network.broadcast_address))

                # CONVERT THAT INTEGER BACK INTO A NORMAL X.X.X.X IPV4 ADDRESS
                random_ip     = ipaddress.IPv4Address(random_ip_int)
                
                """
                 

            else:
                
                with LOCK:
                    if cls.bf_all is None:
                        cls.bf_all = BloomFilter(capacity=cls.bloom_size, error_rate=0.001)

                    random_ip = (f"{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}")

                    if random_ip in cls.bf_all: return False
                    cls.bf_all.add(random_ip); cls.scanned_ips += 1

                    if verbose: console.print(f"[bold green]Generated IP:[bold yellow] {random_ip}")

                    return str(random_ip)



        except Exception as e: console.print(f"[bold red]Exception Error:[bold yellow] {e}"); return False
 
  
    @classmethod
    def _random_ip_validator(cls, ports, timeout=3, verbose=False):
        """This will validate random ip"""



        # COLORS
        c1 = "bold red"
        c2 = "bold yellow"
        c3 = "bold blue"
        c4 = "bold green"

        
        if not cls.scan: return False
        ip = Mass_IP_Scanner._generate_random_ip(verbose=False)
        if not ip: return


        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            
            try:
                

                for port in ports:
                    #pkt = IP(dst=ip)/TCP(dport=port, flags="S")
                    #result = sr1(pkt, timeout=timeout, verbose=0)
                    s.settimeout(timeout)
                    result = s.connect_ex((ip, int(port)))

                    if result == 0: #and result.haslayer(TCP) and result[TCP].flags == 0x12:
                         
                        with LOCK: 
                            if cls.save: cls.current_ips.append(ip)
                            cls.online_ips += 1
                        
                        Database.main(ip=ip, port=port, CONSOLE=console)


            except Exception as e: 
                Database.errors += 1
                console.print(f"[bold red]Exception Error:[bold yellow] {e}")
    
   
    @classmethod
    def _ip_threader(cls, ports, panel, max_workers=250, timeout=1):
        """This will start a multi-proccess thread"""

        # COLORS
        c1 = "bold red"
        c2 = "bold yellow"
        c3 = "bold blue"
        c4 = "bold green"
        c5 = "white"


        futures = []
        last_save = time.time()


        try: max_workers = int(max_workers)
        except Exception: max_workers = 250

        try: portz  = [int(port) for port in ports.split(',')]
        except Exception: portz = list(ports)
        
        #console.print("[bold green][*] Thread Pool initilized!")

    
        with ThreadPoolExecutor(max_workers=max_workers) as executor:

            try:

                while cls.scan:

                    
                    while len(futures) < max_workers and cls.scan:
                        futures.append(executor.submit(Mass_IP_Scanner._random_ip_validator, portz, timeout))


                    futures = [f for f in futures if not f.done()]  


                    if Database.country:  panel.renderable = (f"[{c1}]Filter: [{c2}]{Database.country}  -  [{c1}]Active IPs: [{c2}]{cls.online_ips} / {cls.scanned_ips}  -  [{c1}]Port(s): [{c2}]{portz}  -  [{c1}]Max Workers:[{c2}] {max_workers}  -  [{c1}]Errors:[{c2}] {Database.errors}  -  Developed by NSM Barii")
                    else: panel.renderable = (f"[{c1}]Active IPs: [{c2}]{cls.online_ips} / {cls.scanned_ips}  -  [{c1}]Port(s): [{c2}]{portz}  -  [{c1}]Max Workers:[{c2}] {max_workers}  -  [{c1}]Errors:[{c2}] {Database.errors}  -  Developed by NSM Barii")


                    if time.time() - last_save > 5 and cls.save:
                        with LOCK:
                            File_Saver.push_ips_found(data=cls.current_ips, CONSOLE=console, verbose=False)
                            last_save = time.time()
                            cls.current_ips = []

                    if cls.scanned_ips > 0 and cls.last_scan > 250000:
                        console.print(f"\n[bold yellow][!] Reinitializing ThreadPool!")
                        cls.scan = False
                        time.sleep(5)
                        return False

                sys.exit()

            except KeyboardInterrupt as e:
                console.print("[bold red][-] Killing ALL Threads...."); cls.scan=False
                executor.shutdown(wait=False, cancel_futures=True)
                exit()
            except Exception as e: console.print(f"[bold red]Exception Error:[bold yellow] {e}"); cls.scan=False; exit()


    @classmethod
    def _thread_handler(cls):
        """This method will be a mainter for _ip_threader()"""

        # OK SO OVER THE COURSE OF THE LAST COUPLE DAYS I HAVE BEEN RUNNING INTO A ISSUE WHERE I CAN SCAN A COUPLE MILLION IPS BUT AFTER A WHILE
        # THE THREADS GET CLOGGED AND STOP SCANNING WHICH IS A ISSUE
        # SO I WILL BE CREATING THIS METHOD WITH THE GOAL TO HAVE THIS BE A MAINTER RESPONSIBLE FOR KILLING THE THREADPOOL AND CREATING A NEW ON


        while True:

            current = time.time() - cls.last_scan

            if current > 30:

                console.print(f"[bold red][!] No progress detected reinitializing ThreadPool! ")

                cls.scan = False
                time.sleep(2)
                




    @classmethod
    def _main(cls, port, threads):
        """This will run class wide code"""

        
        cls.scan = True
        cls.scanned_ips = 0 
        cls.online_ips  = 0
        cls.current_ips = []

        
        print("\n")
        if cls.country: cls.blocks = Database.get_ip_block(country=cls.country, CONSOLE=console)
        if cls.save:    File_Saver.push_ips_found(data=False, CONSOLE=console)
        if cls.asn:     data, cls.blocks = Database.get_asn(country=cls.country, asns=cls.asn)

        if cls.country: Database.get_total_ips(blocks=cls.blocks)

        if not port:
            port = console.input("\n[bold yellow]Enter port to mass scan for!: ") or 80
            threads = console.input("[bold yellow]Enter Thread count!: ") or 250; print('\n')
        
        
        panel = Panel(renderable="[bold red]Mass IP Scanner", border_style="bold purple", expand=False)
        with Live(panel, console=console, refresh_per_second=4):
            while True:
                cls.scan = True; cls.last_scan   = 0
                Mass_IP_Scanner._ip_threader(ports=port, max_workers=threads or 250, panel=panel)





class Mass_IP_Scanner():
    """This class will be responsible for finding active ips on user choosen port"""

    
    # ARGS
    country = False
    asn     = False
    lookup  = False

    all     = False
    save    = False
    bloom_size = 100000000


    # MODES
    iot = False
    nas = False
    router = False
    remote = False
    camera = False
    database = False


    # IPS
    #total_ips        = 0
    total_blocks     = []
    ips_from_block   = 0
    current_block    = False
    blocks_done      = 0
    bf_all = None



    @classmethod
    def _track_ip_blocks(cls):
        """Return a random IP from the current block"""

        try:

            if not hasattr(cls, "bf") or cls.bf is None:
                network = ipaddress.IPv4Network(cls.blocks[0])
                cls.bf = BloomFilter(capacity=network.num_addresses * 2, error_rate=0.001)
                cls.total_blocks = cls.blocks.copy()


            if cls.ips_from_block <= 0:

                if not cls.blocks:
                    if cls.scan: console.print(f"[bold green][+] Scan complete | Total IPv4s:[/bold green] {cls.scanned_ips} | Blocks: {len(cls.total_blocks)}")
                    cls.scan = False; return False


                cls.current_block = cls.blocks.pop(0)

                network = ipaddress.IPv4Network(cls.current_block)
                cls.ips_from_block = network.num_addresses
                cls.total_ips = [ip for ip in network]

                console.print(f"\n[bold green][*] Current IPv4 Block:[yellow] {cls.current_block}  -  IPv4 Addresses: {ipaddress.IPv4Network(cls.current_block).num_addresses}\n")                
                time.sleep(1)


            random_ip = cls.total_ips.pop(0)

            cls.ips_from_block -= 1; cls.scanned_ips += 1; cls.last_scan += 1

            return str(random_ip)

        except Exception as e:
            console.print(f"[bold red]IP Exception:[/bold red] {e}")
            return False


    @classmethod
    def _generate_random_ip(cls, verbose=False):
        """This will generate a random ip and return it"""
        

        try:


            # I USUALLY DONT USE COMMENTS SINCE THERE FOR SKIDS
            # BUT THIS WAS EXTREMELY COMPLEX CODE TO DESIGN/DEBUG
            if cls.country:

                
                with LOCK:
                    return Mass_IP_Scanner._track_ip_blocks()


                
                """

                // THE METHOD BELOW IS NOW DEAPPRECIATED, WILL BE KEEPING FOR DOCUMENTATION

                network = [ipaddress.IPv4Network(str(block)) for block in cls.current_block]
                network = random.choice(network)

                # PICK A RANDOM NUMBER BETWEEN THE NETWORKS START AND END IP (AS INTEGERS) 
                # EXAMPLE --> 122.X.X.122  //  122 == START / 122 == END
                random_ip_int = random.randint(int(network.network_address), int(network.broadcast_address))

                # CONVERT THAT INTEGER BACK INTO A NORMAL X.X.X.X IPV4 ADDRESS
                random_ip     = ipaddress.IPv4Address(random_ip_int)
                
                """
                 

            else:
                
                with LOCK:
                    if cls.bf_all is None:
                        cls.bf_all = BloomFilter(capacity=cls.bloom_size, error_rate=0.001)

                    random_ip = (f"{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}")

                    if random_ip in cls.bf_all: return False
                    cls.bf_all.add(random_ip); cls.scanned_ips += 1

                    if verbose: console.print(f"[bold green]Generated IP:[bold yellow] {random_ip}")

                    return str(random_ip)



        except Exception as e: console.print(f"[bold red]Exception Error:[bold yellow] {e}"); return False
 
  
    @classmethod
    def _random_ip_validator(cls, ports, timeout=3, verbose=False):
        """This will validate random ip"""



        # COLORS
        c1 = "bold red"
        c2 = "bold yellow"
        c3 = "bold blue"
        c4 = "bold green"

        
        if not cls.scan: return False
        ip = Mass_IP_Scanner._generate_random_ip(verbose=False)
        if not ip: return


        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            
            try:
                

                for port in ports:
                    #pkt = IP(dst=ip)/TCP(dport=port, flags="S")
                    #result = sr1(pkt, timeout=timeout, verbose=0)
                    s.settimeout(timeout)
                    result = s.connect_ex((ip, int(port)))

                    if result == 0: #and result.haslayer(TCP) and result[TCP].flags == 0x12:
                         
                        with LOCK: 
                            if cls.save: cls.current_ips.append(ip)
                            cls.online_ips += 1
                        
                        Database.main(ip=ip, port=port, CONSOLE=console)


            except Exception as e: 
                Database.errors += 1
                console.print(f"[bold red]Exception Error:[bold yellow] {e}")
    
   
    @classmethod
    def _ip_threader(cls, ports, panel, max_workers=250, timeout=1):
        """This will start a multi-proccess thread"""

        # COLORS
        c1 = "bold red"
        c2 = "bold yellow"
        c3 = "bold blue"
        c4 = "bold green"
        c5 = "white"


        futures = []
        last_save = time.time()


        try: max_workers = int(max_workers)
        except Exception: max_workers = 250

        try: portz  = [int(port) for port in ports.split(',')]
        except Exception: portz = list(ports)
        
        #console.print("[bold green][*] Thread Pool initilized!")

    
        with ThreadPoolExecutor(max_workers=max_workers) as executor:

            try:

                while cls.scan:

                    
                    while len(futures) < max_workers and cls.scan:
                        futures.append(executor.submit(Mass_IP_Scanner._random_ip_validator, portz, timeout))


                    futures = [f for f in futures if not f.done()]  


                    if Database.country:  panel.renderable = (f"[{c1}]Filter: [{c2}]{Database.country}  -  [{c1}]Active IPs: [{c2}]{cls.online_ips} / {cls.scanned_ips}  -  [{c1}]Port(s): [{c2}]{portz}  -  [{c1}]Max Workers:[{c2}] {max_workers}  -  [{c1}]Errors:[{c2}] {Database.errors}  -  Developed by NSM Barii")
                    else: panel.renderable = (f"[{c1}]Active IPs: [{c2}]{cls.online_ips} / {cls.scanned_ips}  -  [{c1}]Port(s): [{c2}]{portz}  -  [{c1}]Max Workers:[{c2}] {max_workers}  -  [{c1}]Errors:[{c2}] {Database.errors}  -  Developed by NSM Barii")


                    if time.time() - last_save > 5 and cls.save:
                        with LOCK:
                            File_Saver.push_ips_found(data=cls.current_ips, CONSOLE=console, verbose=False)
                            last_save = time.time()
                            cls.current_ips = []

                    if cls.scanned_ips > 0 and cls.last_scan > 250000:
                        console.print(f"\n[bold yellow][!] Reinitializing ThreadPool!")
                        cls.scan = False
                        time.sleep(5)
                        return False

                sys.exit()

            except KeyboardInterrupt as e:
                console.print("[bold red][-] Killing ALL Threads...."); cls.scan=False
                executor.shutdown(wait=False, cancel_futures=True)
                exit()
            except Exception as e: console.print(f"[bold red]Exception Error:[bold yellow] {e}"); cls.scan=False; exit()




    @classmethod
    def _main(cls, port, threads):
        """This will run class wide code"""

        
        cls.scan = True
        cls.scanned_ips = 0 
        cls.online_ips  = 0
        cls.current_ips = []

        
        print("\n")
        if cls.country: cls.blocks = Database.get_ip_block(country=cls.country, CONSOLE=console)
        if cls.save:    File_Saver.push_ips_found(data=False, CONSOLE=console)
        if cls.asn:     data, cls.blocks = Database.get_asn(country=cls.country, asns=cls.asn)

        if cls.country: Database.get_total_ips(blocks=cls.blocks)

        if not port:
            port = console.input("\n[bold yellow]Enter port to mass scan for!: ") or 80
            threads = console.input("[bold yellow]Enter Thread count!: ") or 250; print('\n')
        
        
        panel = Panel(renderable="[bold red]Mass IP Scanner", border_style="bold purple", expand=False)
        with Live(panel, console=console, refresh_per_second=4):
            while True:
                cls.scan = True; cls.last_scan   = 0
                Mass_IP_Scanner._ip_threader(ports=port, max_workers=threads or 250, panel=panel)



if __name__ =="__main__":
    Mass_IP_Scanner._main()