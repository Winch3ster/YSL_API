import csv
import constants.errorCode as errorCode
import constants.dbColumn as dbCol
from models.userModel import UserModel

DB_PATH='../YSL_backend/database/data/account.csv'

def getAllAccounts():
    with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        res = []
        id_index, name_index, username_index, role_index = header.index(dbCol.id), header.index(dbCol.name), header.index(dbCol.username), header.index(dbCol.role)
        for lines in csvFile:     
            if lines != []:
                data = UserModel(
                    pId=lines[id_index],
                    pName=lines[name_index],
                    pUsername=lines[username_index],
                    pRole=lines[role_index]
                )
                res.append(data)
        return res

        



def AddUser(userModel): 
    try: 
        with open(DB_PATH, mode='a', newline='') as file:
            # Ensure there's a newline before writing if needed
            file.write("\n")  
            writer_object = csv.writer(file)
            data = [value for key, value in vars(userModel).items()]
            writer_object.writerow(data)
            return True
    except: 
        print("Error registering customer")
        return False
    

def deleteUserById(user_id):
    try:
        # Read all users from the file
        with open(DB_PATH, mode='r', newline='') as file:
            reader = csv.reader(file)
            users = list(reader)

        # Filter out the user with the given ID
        filtered_users = [user for user in users if len(user) > 0 and user[0].strip("(),'") != user_id]

        # Rewrite the file without the deleted user
        with open(DB_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(filtered_users)

        return True

    except Exception as e:
        print(f"Error deleting user: {e}")
        return False