from flask import Flask, render_template, request, abort, url_for, redirect
from app import app
import requests
import os
from flask import jsonify
import json
counter = 0

@app.route('/')
@app.route('/index')
def index():
    zoneList = updateZoneInfo()
    return render_template('index.html', zoneList = zoneList, counter = counter)

#../sbin/music-cli signer leave -s signer1anton -g Atest -v -d | För att ta bort signer

def updateZoneInfo():
    headers = {'Accept': 'application/json', 'X-API-KEY': 'you-have-stolen-my-frotzblinger'}
    url = 'https://13.53.85.107:8080/api/v1/zone'
    payload = {  "Command": "list"
    }
    response = requests.post(url,verify = '/home/ubuntu/music/etc/certs/RootCA.pem', headers=headers, json=payload)
    zoneList = [[]]
    response_json = response.json()
    for zones in response_json['Zones']:
        zoneName = zones
        if(zoneName != ""):
            state = response_json['Zones'][zoneName]['State']
            process = response_json['Zones'][zoneName]['SGroup']['CurrentProcess']
            stopReason = response_json['Zones'][zoneName]['StopReason']
            tmpList = [state,process,zoneName,stopReason]
            zoneList.append(tmpList)
    #index 0 = State, 1 = NextState, 2 = proccess. 
    return zoneList



@app.route('/nextState', methods = ['GET', 'POST'])
def nextState():
    #../sbin/music-cli zone step-fsm -z anton.catch22.se
    zoneName = request.get_json()
    urlZone = 'https://13.53.85.107:8080/api/v1/zone'
    os.chdir("/home/ubuntu/music/music-cli")
    os.system(f'../sbin/music-cli zone step-fsm -z {zoneName["name"]}')
    os.chdir("/home/ubuntu/scanner-lite/cmd/scanner")
    os.system("./scanner")
    zoneList = updateZoneInfo()
    correctList = []
    tmpCounter = 0
    for zones in zoneList:
        print(zones)
        print("hej123")
        if tmpCounter >= 1:
            if zoneName["name"] == zones[2]:
                correctList = zones
                break
        tmpCounter +=1
    zoneDict = {"process": correctList[0], "state": correctList[1],"name":correctList[2],"error":correctList[3] }
    return zoneDict


@app.route('/currentProcess', methods =['POST', 'GET'])
def currentProcess():
    zoneList = updateZoneInfo()
    print("Nu är jag här")
    tmpList = []
    #for zones in zoneList:
     #   if zoneName == zones[3]:
      #      tmpList = zones
    currentP = {"process": zoneList[1][0], "state": zoneList[1][1]}
    return jsonify(currentP)


@app.route('/reset', methods = ['GET', 'POST'])
def reset():
    global counter
    counter = 0
    #Kör alla .sh, men göra music manuellt, och signers. 
    os.chdir("/home/ubuntu")
    os.system("sh reset_parent.sh")
    os.chdir("/home/ubuntu/music/music-cli")
    os.system("sh antonlab_test_setup.sh")
    zoneList = updateZoneInfo()

    #Kör de två .sh på signers och stäng av music manuellt och sätt igång den. 
    return render_template('index.html', zoneList = zoneList,counter = counter)


@app.route('/removeSigner')
def removeSigner():
    os.chdir("/home/ubuntu/music/music-cli")
    os.system("../sbin/music-cli signer leave -s signer1anton -g Atest -v -d")
    return "success"



