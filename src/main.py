# THIS MODULE WILL RUN MODULER CODE FROM HERE



# ETC IMPORTS
import argparse, sys


# UI IMPORTS
from rich.console import Console
from rich.panel import Panel
console = Console()


# NSM IMPORTS
from nsm_scanner import Mass_IP_Scanner
from nsm_database import Database





class Program_Vars():
    """This will be used to pass vars from argparse to a class that stores them"""


    api_key_ipinfo = False




class Main():
    """This wil launch program wide logic"""


    data = (
    "\n [bold cyan]Mass IP Scanning Framework[/bold cyan]"
    "\n\n   [bold yellow]Find Vulnerable Devices[/bold yellow]"
    "\n\n    [bold magenta]Made by NSM-Barii[/bold magenta]\n"
)

    panel = Panel(renderable=data, expand=False, style="bold red")


    parser = argparse.ArgumentParser(
        description="Mass IP Scanning framework meant to find vulnerable devices left uncheck open to the internet"
    )

    parser.add_argument("-p", help="Port to scan.")
    parser.add_argument("-t", help="Maximum number of threads to spawn.")

    parser.add_argument("--save", action="store_true", help="Save all active IPs to database/ips.txt.")
    parser.add_argument("--x",    help="Use this to set a custom file name")


    parser.add_argument("--country", help="Only create IP Blocks within x Country")
    parser.add_argument("--asn", help="Pass asn value(s) Example: 215892, 214735, 214145, 213727, 212056")
    parser.add_argument("--bloom-size", help="BloomFilter capacity for global scans (default: 100000000). Warning: Higher values use more memory.")

    parser.add_argument("--geo", choices=["local", "ipinfo"], help="Enable IP geolocation lookup.")
    parser.add_argument("--ipinfo", help="Optional ipinfo.io API key. Defaults to none.")

    parser.add_argument("--iot",    action="store_true", help="Scan for IoT devices (MQTT, CoAP, mDNS).")
    parser.add_argument("--nas",    action="store_true", help="Scan for NAS devices (SMB, Synology, web panels).")
    parser.add_argument("--camera", action="store_true", help="Scan for IP cameras (RTSP, ONVIF, web interfaces).")
    parser.add_argument("--router", action="store_true", help="Scan for routers and network infrastructure (admin panels, SSH, Telnet, TR-069).")
    parser.add_argument("--remote", action="store_true", help="Scan for remote access services (RDP, VNC, SSH, FTP).")
    parser.add_argument("--database", action="store_true", help="Scan for open databases (3306, 5432, 27017, 6379, 9200).")
    
    parser.add_argument("--show-all", action="store_true", help="Show all active IPS")
    parser.add_argument("--paths",  help="Manually set path for directory bruteforcing (nas, router, camera).")


    args = parser.parse_args()


    if len(sys.argv) == 1:
        console.print(panel)
        parser.print_help(); exit()
        

    # REQUIRED VARS
    port = args.p        or False
    max_threads = args.t or 250


    # ADDITIONS
    country        = args.country     or False
    asn            = args.asn         or False
    bloom_size     = int(args.bloom_size) if args.bloom_size else 100000000
    lookup         = args.geo         or False
    api_key_ipinfo = args.ipinfo      or False
    save           = args.save        or False
    save_name      = args.x           or False

    # WARNING
    if not country:
        console.print("\n[bold red][!] WARNING:[/bold red] [bold yellow]Scanning without --country will use a 100M BloomFilter limit.")
        console.print("[bold yellow]    After 100M IPs, duplicates may be scanned. Use --country for memory-efficient scanning.")
        console.print("[bold yellow]    Or increase with --bloom-size (e.g., --bloom-size 500000000) but this uses more RAM.\n")

    # PRESET OPTIONS
    iot      = args.iot        or False
    nas      = args.nas        or False
    router   = args.router     or False
    remote   = args.remote     or False
    camera   = args.camera     or False
    database = args.database   or False


    # FOR PRESETS    
    paths          = args.paths       or False
    all            = args.show_all    or False
    

    # SET CONSTANTS
    Mass_IP_Scanner.country = country
    Mass_IP_Scanner.asn        = asn
    Mass_IP_Scanner.all        = all
    Mass_IP_Scanner.save       = save
    Mass_IP_Scanner.save_name  = save_name
    Mass_IP_Scanner.bloom_size = bloom_size


    # ASSIGN PRESETS
    if iot:        port = Database.IOT_PORTS;    
    elif nas:      port = Database.paths_nas      ; Database.paths = Database.paths_nas
    elif router:   port = Database.ROUTER_PORTS   ; Database.paths = Database.paths_router
    elif remote:   port = Database.REMOTE_PORTS
    elif camera:   port = Database.CAMERA_PORTS   ; Database.paths = Database.paths_camera
    elif database: port = Database.DATABASE_PORTS 
    
    
    if paths:
        if   paths in ["nas"]:    Database.paths = Database.paths_nas
        elif paths in ["router"]: Database.paths = Database.paths_router    
        elif paths in ["camera"]: Database.paths = Database.paths_camera


    Database.ports  = port
    Database.lookup = lookup
    Database.api_key_ipinfo = api_key_ipinfo


    # IRANIAN CRITICAL INFRASTRUCTURE ASN SHORTCUTS
    # GOVERNMENT
    if asn=="1":
        Mass_IP_Scanner.asn = "5542,15907,31303,42867,56461,56486,56547,60562,60887,61362,62157,205833,206217,206692,214142"

    # MILITARY
    elif asn=="2":
        Mass_IP_Scanner.asn = "16018,44375,57474,61962"

    # TELECOM
    elif asn=="3":
        Mass_IP_Scanner.asn = "39074,39650,42019,43358,44244,44889,47330,48159,48203,49666,49936,50722,50810,50992,51119,51235,51828,51897,52049,56466,57218,57292,57405,58081,58085,58205,58224,59587,59628,59884,60138,60340,61008,61391,62140,64399,197207,199082,200370,201689,202684,202735,204203,204213,206854,207655,209814,210288,210487,210571,210621,212939,215892,215974"

    # ENERGY
    elif asn=="4":
        Mass_IP_Scanner.asn = "42907,51168,51554,51732,52196,57577,59654,62039,199633,200376,202788,206929,208072,214737"

    # FINANCE
    elif asn=="5":
        Mass_IP_Scanner.asn = "3263,9147,15402,21170,24707,31175,31182,31476,34871,34918,35615,35690,39501,41061,42143,42990,43005,47603,47817,48608,49100,49433,49972,50000,50855,51074,51130,51431,51460,51618,51785,52070,52155,56632,56660,57241,57574,57755,57831,58216,58333,59442,59481,59703,59708,59754,60256,60315,60394,60407,60423,60516,60786,61239,61250,62198,62238,198569,200796,200816,201015,201540,202468,202697,203162,203392,203684,204687,204781,204812,205118,205585,205894,206635,208246,208493,208651,208828,209459,209941,210470,210818,211081,211162,211419,211705,212076,212161,213682,213775,213872,213916,215350,215700"

    # TRANSPORT
    elif asn=="6":
        Mass_IP_Scanner.asn = "48762,59961,201442,203026,205490,208231,209079"

    # EDUCATION
    elif asn=="7":
        Mass_IP_Scanner.asn = "5627,6736,12660,12880,15611,16286,16292,29068,29577,34837,35043,35285,39200,39454,41620,43689,43965,44685,47285,47558,47981,48121,48551,48555,48898,49022,49228,49676,49792,50057,50259,56616,56765,56861,57067,57563,57745,58104,58331,59506,59553,59623,59794,59912,59914,59962,60148,60778,61129,61209,61248,62375,64422,198357,200406,200436,202571,203024,203102,203247,203798,204001,204813,204904,205217,205550,206596,206647,208124,208268,208742,209638,209849,210064,210548,210642,210877,210999,211491,211627,211670,212227,212679,214003,214399,214680,215271,215496"

    # MEDIA
    elif asn=="8":
        Mass_IP_Scanner.asn = "42586,44609,47188,62229,204999,205857"



    c1 = "red"; c2 = "bold green"; c3 = "bold blue"; c4 = "bold yellow"

    stats = (
        f"[{c1}][+] Port(s):[{c4}] {port}"
        f"\n[{c1}] [+] Max Workers:[{c4}] {max_threads}"
        f"\n[{c1}] [+] File Saving:[{c4}] {save}"
        f"\n[{c1}] [+] GEO Lookup:[{c4}] {lookup}"
        f"\n[{c1}] [+] API Key:[{c4}] {api_key_ipinfo}"
    )

    panel  = Panel(renderable= stats,        
        title="Constants",
        border_style="purple",
        style="bold red",
        expand=False 
    )
    
    console.print(
        f"[{c1}]=========   CONSTANTS   =========\n",
        stats,
        f"\n[{c1}]=================================",
    )

    

    Mass_IP_Scanner._main(port=port, threads=max_threads)
