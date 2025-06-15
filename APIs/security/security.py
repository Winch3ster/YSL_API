import hashlib
import os 
import json
import csv
import constants.dbColumn as dbCol
CONFIG_PATH = '../YSL_backend/constants/config.json'
DB_PATH = '../YSL_backend/database/data/account.csv'
def sha256_hash(text):
    # Encode the text to bytes, then hash it
    hashed = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return hashed



def authenticateUser(username, password):
    with open(DB_PATH, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[dbCol.username] == sha256_hash(username) and row[dbCol.password] == sha256_hash(password):
                return row  # Return the matching row as a dictionary
        return None
    return None 




def find_user(csv_file_path, username, password):
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return row  # Return the matching row as a dictionary
    return None 




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