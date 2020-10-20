#!python3

from argparse import ArgumentParser
from shlex import split
from subprocess import Popen, PIPE, STDOUT
from re import findall
from os import getuid


RED      = "\033[31m"
CYAN     = "\033[96m"
GREEN    = "\033[92m"
ENDCOLOR = "\033[0m"


def main():



    parser = ArgumentParser(description="Enumerates a target.") # Creates a parser to parse command line arguments

    parser.add_argument(dest="ip", help="IP address of the target") # Adds mandatory argument for the IP address

    parser.add_argument("--noBanner",  "-nB", help="Do not print the banner.", action="store_true") # Optional flag to disable the printing of the banner
    parser.add_argument("--fileName",  "-fN", help="Path for the output file", default=None) # Optional flag to change the name of the output file
    parser.add_argument("--rustscan",  "-rs", help="Specify args to be passed to rustscan here in quotes (run rustscan --help for more info)", default="--ulimit 5000") # Optional flag to send flags to rustscan
    parser.add_argument("--nmap",      "-nm", help="Specify args to be passed to nmap here in quotes, ports are gotten from the rustscan.  Default is \"-A --reason -Pn -sV -sC --script vuln -T5\" (run nmap --help for more info)", default="-A --reason -Pn -sV -sC --script vuln -T5") # Optional flag to send flags to nmap


    args = parser.parse_args() # Parse the args

    ip           = args.ip # The IP address supplied
    noBanner     = args.noBanner # Whether or not to show the banner
    outputFile   = args.fileName # The path to write the output file

    if outputFile:
        args.nmap += " -oN " + outputFile

    rustscanArgs = split(args.rustscan) # The args to be passed to rustscan
    nmapArgs     = split(args.nmap) # The args to be passed to nmap.


    if not noBanner: # COOL BANNER AHHHH!!!!
        print(f"""{RED}
▓█████▄ ▓█████ ██▒   █▓ ██▓ ▄████▄  ▓█████    ▓█████  ███▄    █  █    ██  ███▄ ▄███▓▓█████  ██▀███   ▄▄▄     ▄▄▄█████▓ ▒█████   ██▀███  
▒██▀ ██▌▓█   ▀▓██░   █▒▓██▒▒██▀ ▀█  ▓█   ▀    ▓█   ▀  ██ ▀█   █  ██  ▓██▒▓██▒▀█▀ ██▒▓█   ▀ ▓██ ▒ ██▒▒████▄   ▓  ██▒ ▓▒▒██▒  ██▒▓██ ▒ ██▒
░██   █▌▒███   ▓██  █▒░▒██▒▒▓█    ▄ ▒███      ▒███   ▓██  ▀█ ██▒▓██  ▒██░▓██    ▓██░▒███   ▓██ ░▄█ ▒▒██  ▀█▄ ▒ ▓██░ ▒░▒██░  ██▒▓██ ░▄█ ▒
░▓█▄   ▌▒▓█  ▄  ▒██ █░░░██░▒▓▓▄ ▄██▒▒▓█  ▄    ▒▓█  ▄ ▓██▒  ▐▌██▒▓▓█  ░██░▒██    ▒██ ▒▓█  ▄ ▒██▀▀█▄  ░██▄▄▄▄██░ ▓██▓ ░ ▒██   ██░▒██▀▀█▄  
░▒████▓ ░▒████▒  ▒▀█░  ░██░▒ ▓███▀ ░░▒████▒   ░▒████▒▒██░   ▓██░▒▒█████▓ ▒██▒   ░██▒░▒████▒░██▓ ▒██▒ ▓█   ▓██▒ ▒██▒ ░ ░ ████▓▒░░██▓ ▒██▒
▒▒▓  ▒ ░░ ▒░ ░  ░ ▐░  ░▓  ░ ░▒ ▒  ░░░ ▒░ ░   ░░ ▒░ ░░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░ ▒ ░░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
░ ▒  ▒  ░ ░  ░  ░ ░░   ▒ ░  ░  ▒    ░ ░  ░    ░ ░  ░░ ░░   ░ ▒░░░▒░ ░ ░ ░  ░      ░ ░ ░  ░  ░▒ ░ ▒░  ▒   ▒▒ ░   ░      ░ ▒ ▒░   ░▒ ░ ▒░
░ ░  ░    ░       ░░   ▒ ░░           ░         ░      ░   ░ ░  ░░░ ░ ░ ░      ░      ░     ░░   ░   ░   ▒    ░      ░ ░ ░ ▒    ░░   ░ 
░       ░  ░     ░   ░  ░ ░         ░  ░      ░  ░         ░    ░            ░      ░  ░   ░           ░  ░            ░ ░     ░     
░                 ░       ░                                                               {CYAN}This script uses rustscan and nmap!\t:P
        {ENDCOLOR}"""   )



    if getuid() != 0:
        print(RED + "WARNING YOU ARE NOT RUNNING THIS SCRIPT AS ROOT!  SOME FEATURES IN NMAP, SUCH AS OS DETECTION, REQUIRE ROOT PRIVELEDGES TO WORK.  RERUN WITH SUDO TO ENSURE THAT EVERYTHING WORKS!!!!\nIf you are not using any options that require root priveledges you can ignore this message.    :P" + ENDCOLOR)





    rustscan = Popen(["rustscan", "-g", *rustscanArgs, ip], stdout=PIPE, stderr=STDOUT) # Run rustscan in greppable mode using passed args, greppable mode just outputs the ports

    out, _ = rustscan.communicate() # Get the output and the errors
    out = GREEN + out.decode("utf-8") + ENDCOLOR # Make output green

    out = out.split("->")[-1] # Rustscan gives back data in form "IP -> [PORTS]".  Splits by the arrow and takes the part with the ports
    ports = findall("\d+", out)[:-1] # Uses regex to pull out all the ports.  Do not take the last one, as it will always say 0 because it gets it from the ENDCOLOR flag.


    print(f"Ports: {', '.join(ports)}")





    nmapArgs.append("-p")
    nmapArgs.append(','.join(ports)) # Adds the ports to the args

    print(f"Nmap command is nmap {' '.join(nmapArgs)} {ip}")
    print("Scanning ports....")






    nmap = Popen(["sudo", "nmap", *nmapArgs, ip], stdout=PIPE, stderr=STDOUT) # Run nmap


    out, _ = nmap.communicate() # Get the output and the errors
    out = GREEN + out.decode("utf-8") + ENDCOLOR # Make output green
    
    print(out)




if __name__ == "__main__":
    main()
