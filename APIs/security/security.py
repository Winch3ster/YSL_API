import hashlib
import os 
import json

CONFIG_PATH = '../YSL_backend/constants/config.json'

def sha256_hash(text):
    # Encode the text to bytes, then hash it
    hashed = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return hashed



def authenticateUser(username, password):
    sysUsername = ""
    sysPassword = ""    

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
        sysUsername = config["adminUsername"]
        sysPassword = config["adminPassword"]

    if sha256_hash(username) == sysUsername and sha256_hash(password) == sysPassword:
        return True
    else:
        return False

def updatePassword(oldpassword, newpassword):
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    if sha256_hash(oldpassword) == config["adminPassword"]:
        config["adminPassword"] = sha256_hash(newpassword)
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f)
        return True
    else:
        return False