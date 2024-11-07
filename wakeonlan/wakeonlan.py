import socket
import struct
import argparse
import re

# Constants for default broadcast IP and port
DEFAULT_IP = '255.255.255.255'
DEFAULT_PORT = 9

# Regular expressions for MAC address validation
MAC_REGEXES = [
    r'^(?:[0-9a-fA-F]{1,2}:){5}[0-9a-fA-F]{1,2}$',  # xx:xx:xx:xx:xx:xx
    r'^(?:[0-9a-fA-F]{1,2}-){5}[0-9a-fA-F]{1,2}$',  # xx-xx-xx-xx-xx-xx
    r'^[0-9a-fA-F]{6}-[0-9a-fA-F]{6}$',             # xxxxxx-xxxxxx
    r'^[0-9a-fA-F]{12}$',                          # xxxxxxxxxxxx
]

def is_valid_mac(mac):
    """Check if the MAC address is valid."""
    for regex in MAC_REGEXES:
        if re.match(regex, mac):
            return True
    return False

def build_magic_packet(mac):
    """Build a magic packet from a MAC address."""
    mac = mac.replace(':', '').replace('-', '').lower()
    mac_bytes = bytes.fromhex(mac)
    return b'\xff' * 6 + mac_bytes * 16

def send_wol_packet(mac, ip=DEFAULT_IP, port=DEFAULT_PORT, dryrun=False):
    """Send a Wake-on-LAN packet to a MAC address."""
    if dryrun:
        print(f"Dry run: Would send packet to {mac} at {ip}:{port}")
        return

    try:
        magic_packet = build_magic_packet(mac)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, (ip, port))
        print(f"Packet sent to {mac} at {ip}:{port}")
    except Exception as e:
        print(f"Failed to send packet to {mac}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Send Wake-on-LAN packets to specified MAC addresses.")
    parser.add_argument('--mac', type=str, nargs='+', required=True, help="Specify one or more MAC addresses.")
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help="Specify a custom port (default: 9).")
    parser.add_argument('--dryrun', action='store_true', help="Simulate sending packets without actually sending.")
    parser.add_argument('--verbose', action='store_true', help="Print detailed output.")
    
    args = parser.parse_args()

    total = len(args.mac)
    valid_count = 0
    invalid_count = 0
    sent_count = 0

    for mac in args.mac:
        if is_valid_mac(mac):
            valid_count += 1
            if args.verbose:
                print(f"Valid MAC address: {mac}")
            send_wol_packet(mac, port=args.port, dryrun=args.dryrun)
            sent_count += 1
        else:
            invalid_count += 1
            print(f"Invalid MAC address: {mac}")

    # Summary output
    print("\nSummary:")
    print(f"Total MACs processed: {total}")
    print(f"Valid MACs: {valid_count}")
    print(f"Invalid MACs: {invalid_count}")
    print(f"Packets sent: {sent_count if not args.dryrun else 0}")

if __name__ == "__main__":
    main()
