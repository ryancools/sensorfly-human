from flask import Flask, request, jsonify
import random
import threading
import time
from flask import json
import signal
import sys

from main_testbed import main

app = Flask(__name__);

data = [{"rotation": 0, "distance": 0},{"rotation": 0, "distance": 0}];

# States:
# Unregistered, Registered, GroundTruth, Directions, Rotating, Rotated, Moving, Moved

clients = [{"state": "Unregistered", "groundTruth": {"x": 0, "y" : 0}, "directions": {"move": 0, "rotate": 0, "valid": False}}]
globalGroundTruth = False;
systemRunning = [True];

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        shutdown_server()
        sys.exit(0)

def updateData():
    while True:
        data[0]["rotation"] = random.random();
        data[0]["distance"] = random.random();
        data[1]["rotation"] = random.random();
        data[1]["distance"] = random.random();
        time.sleep(.1);

def runAlgo():
    while True:
        allReady = True;
        for client in clients:
            if client["state"] != "GroundTruth" or client["directions"]["valid"]:
                allReady = False;

        if allReady:
            globalGroundTruth = True;
            # Run algo here
            client["directions"]["move"] = random.random();
            client["directions"]["rotate"] = random.random();
            client["directions"]["valid"] = True;
        time.sleep(.25);

@app.route("/clientUpdate", methods=['POST'])
def hello():
    print(request.json);
    return "Hello World!";

@app.route("/getSensorData/<int:clientId>", methods=['GET'])
def getSensorData(clientId):
    return jsonify(data[clientId]);

@app.route("/register/<int:clientId>", methods=['GET'])
def register(clientId):
    clients[clientId]["state"] = "Registered";
    return "Success";

@app.route("/groundTruth/<int:clientId>", methods=['POST'])
def groundTruth(clientId):
    #print(request.json);
    if clients[clientId]["state"] == "Registered" or clients[clientId]["state"] == "Moved":
        d = dict((key.encode('ascii'), value.encode('ascii')) for (key, value) in request.json.iteritems())
        #print(d);
        clients[clientId]["groundTruth"]["x"] = d["x"];
        clients[clientId]["groundTruth"]["y"] = d["y"];
        clients[clientId]["state"] = "GroundTruth";
        #print(clients[clientId]);
        return "Success";
    else:
        return "Error"

@app.route("/requestDirections/<int:clientId>", methods=['GET'])
def requestDirections(clientId):
    if clients[clientId]["state"] == "GroundTruth" and clients[clientId]["directions"]["valid"]:
        clients[clientId]["state"] = "Directions";
        clients[clientId]["directions"]["valid"] = False;
        globalGroundTruth = False;
        return jsonify(clients[clientId]["directions"]);
    else:
        return "Error"

@app.route("/startRotating/<int:clientId>", methods=['GET'])
def startRotating(clientId):
    if clients[clientId]["state"] == "Directions":
        clients[clientId]["state"] = "Rotating";
        return "Success";
    else:
        return "Error"

@app.route("/stopRotating/<int:clientId>", methods=['GET'])
def stopRotating(clientId):
    if clients[clientId]["state"] == "Rotating":
        clients[clientId]["state"] = "Rotated";
        return "Success";
    else:
        return "Error"

@app.route("/startMoving/<int:clientId>", methods=['GET'])
def startMoving(clientId):
    if clients[clientId]["state"] == "Rotated":
        clients[clientId]["state"] = "Moving";
        return "Success";
    else:
        return "Error"

@app.route("/stopMoving/<int:clientId>", methods=['GET'])
def stopMoving(clientId):
    if clients[clientId]["state"] == "Moving":
        clients[clientId]["state"] = "Moved";
        return "Success";
    else:
        return "Error"

@app.route("/stopSystem", methods=['GET'])
def stopSystem():
    systemRunning[0] = False;
    return "Success";

signal.signal(signal.SIGINT, signal_handler);

t1 = threading.Thread(target=main,args=(clients,data,systemRunning))
#t2 = threading.Thread(target=runAlgo)

t1.daemon = True;
#t2.daemon = True;

t1.start();
#t2.start();


app.debug = False;
app.run(host="10.0.23.151", port=5001);
