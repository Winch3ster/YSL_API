import csv
import models.conditionModel as CM
from datetime import datetime
import constants.dbColumn as dbCol
import os
DB_PATH = '../YSL_backend/database/data/conditionDb.csv'

def getAllConditionsByCustomerId(customerId):
    with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        customer_id_index = header.index(dbCol.customerIdConditionDb)
        condition_id = header.index(dbCol.conditionId)
        condition_description = header.index(dbCol.conditionDescription)
        undergoing_treatment = header.index(dbCol.undergoingTreatment)
        condition_date = header.index(dbCol.conditionDate)
      

        result = []

        for line in csvFile:
            if line != []:

                print(f'{line[customer_id_index]} == {customerId} --> {line[customer_id_index] == customerId}')
                if line[customer_id_index] == customerId:
                    condition = CM.ConditionModel(
                        customerId=customerId,
                        condition_id=line[condition_id],
                        conditionDescription=line[condition_description],
                        undergoingTreatment=True if line[undergoing_treatment] == "True" else False ,
                        conditionDate= line[condition_date] 
                    )
                    result.append(condition)
        sorted_result = sorted(result, key=lambda x: parse_date_safe(x.conditionDate), reverse=True)  # Sort by conditionDate in descending order
        return sorted_result


def parse_date_safe(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    except (ValueError, TypeError):
        return datetime.min  # or datetime.max if sorting descending



def insertConditionToDb( conditionModel):
    with open(DB_PATH, mode='a', encoding='utf-8', newline='\n') as file:
        # Ensure there's a newline before writing if needed
        file.write("\n")  

        writer_object = csv.writer(file)
        data = [value for key, value in vars(conditionModel).items()]
        writer_object.writerow(data)


def updateConditionByID(newConditionModel):
    #  self.customerId = customerId
    #    self.conditionId = condition_id
    ##    self.conditionDescription = conditionDescription    
    #    self.undergoingTreatment = undergoingTreatment
    #    self.conditionDate = conditionDate
        
    temp_file_path = DB_PATH + ".tmp"
    updated = False

    conditionId = newConditionModel.conditionId
    with open(DB_PATH, mode='r', encoding='utf-8', newline='') as infile, \
         open(temp_file_path, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            # Skip completely empty rows
            if not row or all(cell.strip() == '' for cell in row):
                continue

            if row[1].strip() == newConditionModel.conditionId:
                new_row = [value for _, value in vars(newConditionModel).items()]
                writer.writerow(new_row)
                updated = True
            else:
                writer.writerow(row)

    if updated:
        print("UPDATED DB")
        os.replace(temp_file_path, DB_PATH)
    else:
        print("DB NOT UPDATED")
        os.remove(temp_file_path)

    return updated


def getConditionById(conditionId):
    with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        customer_id_index = header.index(dbCol.customerIdConditionDb)
        condition_id = header.index(dbCol.conditionId)
        condition_description = header.index(dbCol.conditionDescription)
        undergoing_treatment = header.index(dbCol.undergoingTreatment)
        condition_date = header.index(dbCol.conditionDate)

        for line in csvFile:
            if line != []:
                if line[condition_id] == conditionId:
                    condition = CM.ConditionModel(
                        customerId=line[customer_id_index],
                        condition_id=line[condition_id],
                        conditionDescription=line[condition_description],
                        undergoingTreatment=line[undergoing_treatment],
                        conditionDate=line[condition_date]
                    )
                    return condition
        return None