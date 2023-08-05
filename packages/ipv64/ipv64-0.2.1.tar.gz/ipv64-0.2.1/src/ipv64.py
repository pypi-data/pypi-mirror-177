import dns.resolver
import requests
from datetime import datetime as dt
import argparse

def nslookup(domain):
    resolver = dns.resolver.Resolver()
    dns.resolver.Cache(1)
    dns.resolver.Timeout(10)
    resolver.nameservers = ["195.201.223.103", "157.90.241.20", "2a01:4f8:c2c:559c::1", "2a01:4f8:c012:9c97::1"]

    try:
        ipv4_ns = resolver.resolve(domain, 'A')[0]
    except:
        print(str(dt.now()) + ": IPv4 DNS resolution failed")
        ipv4_ns = None
    try:
        ipv6_ns = resolver.resolve(domain, 'AAAA')[0]
    except:
        print(str(dt.now()) + ": IPv6 DNS resolution failed")
        ipv6_ns = None

    return ipv4_ns, ipv6_ns

def get_ip():
    # get the current ip from the internet
    try:
        ipv4 = requests.get('https://ipv4.ipapi.de').text
    except:
        ipv4 = None
    try:
        ipv6 = requests.get('https://ipv6.ipapi.de').text
    except:
        ipv6 = None

    return ipv4, ipv6

def update_ip(domain, update_key, ipv4, ipv6):
    # Make Post request to update the ip
    if ipv4 != None and ipv6 != None:
        url = "https://ipv64.net/update.php?key=" + update_key + "&domain=" + domain + "&ip=" + ipv4 + "&ip6=" + ipv6
    elif ipv4 != None and ipv6 == None:
        url = "https://ipv64.net/update.php?key=" + update_key + "&domain=" + domain + "&ip=" + ipv4
    elif ipv6 != None and ipv4 == None:
        url = "https://ipv64.net/update.php?key=" + update_key + "&domain=" + domain + "&ip6=" + ipv6

    try:
        r = requests.get(url)
        return r.status_code, r.text
    except:
        print("Update failed")
        return False, False
    
def run_update(domain, update_key, webhook):
    # Get the current ip
    ipv4, ipv6 = get_ip()
    # Get the ip from the dns
    ipv4_ns, ipv6_ns = nslookup(domain)

    if ipv4_ns == None and ipv6_ns == None:
        exit()

    #print(str(dt.now()) + ": Current IPv4:\t" + str(ipv4) + ", Current IPv6:\t" + str(ipv6))
    #print(str(dt.now()) + ": DNS IPv4:\t" + str(ipv4_ns) + ", DNS IPv6:\t\t" + str(ipv6_ns))

    if str(ipv4) != str(ipv4_ns) and ipv4 != None or str(ipv6) != str(ipv6_ns) and ipv6 != None:
        status_code, status_text = update_ip(domain, update_key, ipv4, ipv6)
        
        if status_code == 200:
            print(str(dt.now()) + ": New IP for " + domain + ": " + str(ipv4) + " (" + str(ipv4_ns) + "), " + str(ipv6) + " (" + str(ipv6_ns) + ")")
            
            if webhook != None or "":
                discord_msg("New IP for " + domain + ": " + str(ipv4) + " (" + str(ipv4_ns) + "), " + str(ipv6) + " (" + str(ipv6_ns) + ")", webhook)
        else:
            print(str(dt.now()) + ": Update failed: " + str(status_code) + " " + str(status_text))
            if webhook != None or "":
                discord_msg("Update failed: " + str(status_code) + " " + str(status_text), webhook)
    else:
        print(str(dt.now()) + ": IPs up to date")


def discord_msg(msg=None, webhook=None):
    if webhook != None or "":
        # Send a message to a discord channel
        try:
            requests.post(webhook, json={"content": msg, "username": "IPV64 Updater"})
        except:
            print("Discord message failed")


# ask for argprase inputs
# if no inputs are given, show help
parser = argparse.ArgumentParser(description='Update the IP for a domain on ipv64.net')
parser.add_argument('-d', '--domain', help='The domain to update', required=True)
parser.add_argument('-uh', '--hash', help='Your DynDNS Updatehash', required=True)
parser.add_argument('-w', '--webhook', help='The webhook url for discord notifications', required=False, default=None)
args = parser.parse_args()

run_update(args.domain, args.hash, args.webhook)
