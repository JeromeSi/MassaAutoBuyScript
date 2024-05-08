#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  script-autobuy.py
#
#  Copyright 2024 Jérôme Signouret <jerome.signouret@laposte.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

###########################
# Save this script in massa folder
address = 'AU...'
password = 'yourPasswordHere'
fees = '0.001'
minimumAmout = 1
###########################

import requests
import json
import subprocess
import os

def chercherClef(truc,cle):
    if isinstance(truc,dict):
        for clef in truc:
            if clef == cle:
                return truc[cle]
            else:
                resultat = chercherClef(truc[clef],cle)
                if resultat != "Not find":
                    return resultat
        return "Not find"
    elif isinstance(truc,list):
        for element in reversed(truc):
            resultat = chercherClef(element,cle)
            if resultat != "Not find":
                return resultat
    return "Not find"

def getaddresses(url,headers):
    global address
    # Data of JSON-RPC request
    methode = "get_addresses"
    params = [[address]]
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": methode,
        "params": params
    }
    # Convert  dict in JSON
    json_data = json.dumps(data)
    # POST request
    response = requests.post(url, headers=headers, data=json_data)
    if response.status_code == 200:
        json_response = response.json()
        getAddresses = {}
        for laClef in ['final_balance','final_roll_count','candidate_balance','candidate_roll_count','active_rolls','ok_count', 'nok_count']:
            temp = chercherClef(json_response['result'],laClef)
            if temp == None:
                getAddresses[laClef] = 0
            else:
                getAddresses[laClef] = temp
    return getAddresses

def autobuy(limite):
    global password
    global fees
    global address
    if os.path.exists("massa-client/massa-client"):
        runClient = 'cd massa-client/;./massa-client'
    elif os.path.exists("target/release/massa-client"):
        runClient = 'cd massa-client/;../target/release/massa-client'
        else:
            return "massa-client : file not found"
    lemassaClient = runClient+' -p '+password+' buy_rolls '+address

    url = 'http://localhost:33035'
    headers = {'Content-Type': 'application/json'}
    finalBalance = float(getaddresses(url,headers)['final_balance'])

    if finalBalance > (limite + 100):
        rollAchat = int((finalBalance - limite) / 100)
        parametres = ' '+str(rollAchat)+' '+fees
        subprocess.run([lemassaClient+parametres],shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        return 1
    return 0

def main(args):
    global minimumAmout
    autobuy(minimumAmout)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
