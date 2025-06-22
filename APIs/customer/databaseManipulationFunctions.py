import csv
import constants.errorCode as errorCode
import constants.dbColumn as dbCol
from models.customerObjectModel import CustomerModel
from models.customerSearchModel import CustomerSearchModel
from utils.converterFunctions import convertTimeStampToId, getFormattedDateTime
from utils.generatorFunctions import generateUUID
import os
from typing import Union

DB_PATH = '../YSL_backend/database/data/db.csv'
def searchForSingleUser( userId):
    print("Absolute path:", os.path.abspath(DB_PATH))
    print("File exists:", os.path.exists(DB_PATH))


    print("from searching constant function")
    print(userId)    
    with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        
        if dbCol.customerId in header:
            customer_id = header.index(dbCol.customerId)
            ic_index = header.index(dbCol.ic)
            name_index = header.index(dbCol.name)
            email_index = header.index(dbCol.email)
            handphone_index = header.index(dbCol.handPhoneNumber)
            gender_index = header.index(dbCol.gender)
            address_index = header.index(dbCol.address)
            insta_index = header.index(dbCol.instagram)
            knowUsMethod_index = header.index(dbCol.knowUsMethod)
            race_index = header.index(dbCol.race)  
            old_cus_id_index = header.index(dbCol.oldCustomerId)
            wechat_index = header.index(dbCol.weChat)
            height_index = header.index(dbCol.height)
            weight_index = header.index(dbCol.weight)
            blood_type_index = header.index(dbCol.bloodType)

            for lines in csvFile:
                if lines != []:
                    if lines[customer_id] == userId:
                        print(lines[old_cus_id_index])

                        customer = CustomerModel(
                            pCustomerId=lines[customer_id],
                            pOldCustomerId= lines[old_cus_id_index],
                            pIc=lines[ic_index],
                            pCustomerName=lines[name_index],
                            pEmail= lines[email_index],
                            pHandphoneNum= lines[handphone_index],
                            pGender=lines[gender_index],
                            pAddress=lines[address_index],
                            pInstagram=lines[insta_index],
                            pHowDidYouFindUs= lines[knowUsMethod_index],
                            pRace=lines[race_index],
                            pWeChat=lines[wechat_index],
                            pHeight=lines[height_index],
                            pWeight=lines[weight_index],
                            pBloodType=lines[blood_type_index]
                        )
                        return customer          
        else:
            return errorCode.NO_USER_FOUND
        
def getAllCustomers():
    with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        res = []
        if dbCol.ic in header and dbCol.name in header:
            customer_id, ic_index, name_index, email_index = header.index(dbCol.customerId), header.index(dbCol.ic), header.index(dbCol.name), header.index(dbCol.email)
            for lines in csvFile:     
                if lines != []:
                    data = CustomerSearchModel(
                        pUserId=convertTimeStampToId(lines[customer_id]),
                        pCustomerIC=lines[ic_index],
                        pCustomerName=lines[name_index],
                        pEmail=lines[email_index]
                    )
                    res.append(data)
            return res
        else:
            return errorCode.NO_USER_FOUND

def registerCustomer(customerModel): 
    try: 
        with open(DB_PATH, mode='a', newline='') as file:
            # Ensure there's a newline before writing if needed
            file.write("\n")  

            writer_object = csv.writer(file)
            data = [value for key, value in vars(customerModel).items()]
            writer_object.writerow(data)
            return True
    except: 
        print("Error registering customer")
        return False

def updateCustomerByID(updatedCustomer) -> Union[bool, str]:
    print("Updating user with ID:", updatedCustomer.customerId)

    # Read existing data
    if not os.path.exists(DB_PATH):
        return "Database file not found."

    updated = False

    with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csv_reader = list(csv.reader(file))
        header = csv_reader[0]

        if dbCol.customerId not in header:
            return "Header does not contain customerId."

        # Get column indexes
        customer_id = header.index(dbCol.customerId)
        ic_index = header.index(dbCol.ic)
        name_index = header.index(dbCol.name)
        email_index = header.index(dbCol.email)
        handphone_index = header.index(dbCol.handPhoneNumber)
        gender_index = header.index(dbCol.gender)
        address_index = header.index(dbCol.address)
        insta_index = header.index(dbCol.instagram)
        knowUsMethod_index = header.index(dbCol.knowUsMethod)
        race_index = header.index(dbCol.race)
        old_cus_id_index = header.index(dbCol.oldCustomerId)
        wechat_index = header.index(dbCol.weChat)
        height_index = header.index(dbCol.height)
        weight_index = header.index(dbCol.weight)
        blood_type_index = header.index(dbCol.bloodType)

        # Update matching row
        for i in range(1, len(csv_reader)):
            row = csv_reader[i]

            if convertTimeStampToId(row[customer_id]) == updatedCustomer.customerId:
                row[customer_id] = str(row[customer_id]) 
                row[old_cus_id_index] = updatedCustomer.oldCustomerId
                row[ic_index] = updatedCustomer.ic
                row[name_index] = updatedCustomer.customerName
                row[email_index] = updatedCustomer.email
                row[handphone_index] = updatedCustomer.handphone
                row[gender_index] = updatedCustomer.gender
                row[address_index] = updatedCustomer.address
                row[insta_index] = updatedCustomer.instagram
                row[knowUsMethod_index] = updatedCustomer.howDidYouFindUs
                row[race_index] = updatedCustomer.race
                row[wechat_index] = updatedCustomer.weChat
                row[height_index] = updatedCustomer.height
                row[weight_index] = updatedCustomer.weight
                row[blood_type_index] = updatedCustomer.bloodType
                updated = True
                break

    if not updated:
        return "User not found."

    # Write updated data back to CSV
    with open(DB_PATH, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_reader)

    return True

def searchForUserBasedOn_ID_IC_Name_Email(userId):
    with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        res = []
        if dbCol.ic in header and dbCol.name in header:
            customer_id, ic_index, name_index, email_index = header.index(dbCol.customerId), header.index(dbCol.ic), header.index(dbCol.name), header.index(dbCol.email)
            for lines in csvFile:
                if (
                    userId.lower() in lines[ic_index].lower() or
                    userId.lower() in lines[customer_id].lower() or
                    userId.lower() in lines[name_index].lower() or
                    userId.lower() in lines[email_index].lower()
                ):
                    res.append([lines[customer_id], lines[ic_index], lines[name_index], lines[email_index]])
            return res
        else:
            return errorCode.NO_USER_FOUND
                    
def addOldCustomerID(customerID, oldCustomerId):
    print(f'{customerID} --> {oldCustomerId}')
    updated = False

    # Read all rows
    with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    if not rows:
        print("Empty CSV")
        return

    header = rows[0]
    if dbCol.customerId in header and dbCol.oldCustomerId in header:
        customer_id_index = header.index(dbCol.customerId)
        old_customer_id_index = header.index(dbCol.oldCustomerId)

        for i in range(1, len(rows)):  # Skip header
            if rows[i][customer_id_index] == customerID:
                rows[i][old_customer_id_index] = oldCustomerId
                updated = True
                break

        if updated:
            # Write the updated rows back to the file
            with open(DB_PATH, mode='w', encoding='utf-8', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(rows)
            print("Added old customer ID successfully.")
        else:
            print("Customer ID not found.")
            return errorCode.NO_USER_FOUND
    else:
        print("Required columns not found.")
        return errorCode.NO_USER_FOUND
        