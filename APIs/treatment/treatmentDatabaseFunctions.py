import csv
from csv import writer
import constants.dbColumn as dbCol
import constants.errorCode as errorCode
from models.treatmentModel import TreatmentModel
from utils.converterFunctions import getFormattedDateTime
from utils.generatorFunctions import generateUUID
import os

DB_PATH = '../YSL_backend/database/data/treatmentDb.csv'
TREATMENT_REVISION_PATH = '../YSL_backend/database/data/treatmentRevisionHistory.csv'

def getAllTreatmentByCustomerId(customerId):
   
   #!!!!!!!!!!!! customerId --> converted format
   with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        customer_id_index = header.index(dbCol.customerIdTreatment)
        treatment_description = header.index(dbCol.treatmentDescription)
        treatment_date = header.index(dbCol.treatmentDate)    
        pain_lvl = header.index(dbCol.treatmentPainLevel)
        tense_lvl = header.index(dbCol.treatmentTenseLevel)
        sore_lvl = header.index(dbCol.treatmentSoreLevel)
        numb_lvl = header.index(dbCol.treatmentNumbLevel)
        result = []

        for line in csvFile:
            if line != []:
                if line[customer_id_index] == customerId:
                    treatment = TreatmentModel(
                        pCustomerId=customerId,
                        pTreatmentDescription= line[treatment_description],
                        pTreatmentDate=line[treatment_date],
                        pNumbLevel=line[numb_lvl],
                        pPainLevel=line[pain_lvl],
                        pSoreLevel=line[sore_lvl],
                        pTenseLevel=line[tense_lvl]
                    )
                    result.append(treatment)
        
        return result




def createTreatment(treatmentModel):
    try:
        with open(DB_PATH, mode='a', encoding='utf-8', newline='\n') as file:
            # Ensure there's a newline before writing if needed
            file.write("\n")  

            writer_object = writer(file)
            data = [value for key, value in vars(treatmentModel).items()]
            writer_object.writerow(data)
        return {"Status": errorCode.SUCCESS, "message": errorCode.SUCCESS}
    except Exception as e:
        return {"Status": errorCode.ERROR, "message": str(e)}


def getAllTreatmentByConditionID(conditionId):
   
   #!!!!!!!!!!!! customerId --> converted format
   with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        customer_id_index = header.index(dbCol.conditionId)
        treatment_id_index = header.index(dbCol.treatmentId)
        treatment_description = header.index(dbCol.treatmentDescription)
        treatment_date = header.index(dbCol.treatmentDate)    
        pain_lvl = header.index(dbCol.treatmentPainLevel)
        tense_lvl = header.index(dbCol.treatmentTenseLevel)
        sore_lvl = header.index(dbCol.treatmentSoreLevel)
        numb_lvl = header.index(dbCol.treatmentNumbLevel)
        result = []

        for line in csvFile:
            if line != []:
                if line[customer_id_index] == conditionId:
                    treatment = TreatmentModel(
                        pConditionId=conditionId,
                        pTreatmentId=line[treatment_id_index],
                        pTreatmentDescription= line[treatment_description],
                        pTreatmentDate=line[treatment_date],
                        pNumbLevel=line[numb_lvl],
                        pPainLevel=line[pain_lvl],
                        pSoreLevel=line[sore_lvl],
                        pTenseLevel=line[tense_lvl]
                    )
                    result.append(treatment)
        
        return result

def getTreatmentByID(treatmentID):
    #!!!!!!!!!!!! customerId --> converted format
   with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        condition_id_index = header.index(dbCol.conditionId)
        treatment_id_index = header.index(dbCol.treatmentId)
        treatment_description = header.index(dbCol.treatmentDescription)
        treatment_date = header.index(dbCol.treatmentDate)    
        pain_lvl = header.index(dbCol.treatmentPainLevel)
        tense_lvl = header.index(dbCol.treatmentTenseLevel)
        sore_lvl = header.index(dbCol.treatmentSoreLevel)
        numb_lvl = header.index(dbCol.treatmentNumbLevel)
        result = None

        for line in csvFile:
            if line != []:
                if line[treatment_id_index] == treatmentID:
                    treatment = TreatmentModel(
                        pConditionId=line[condition_id_index],
                        pTreatmentId=treatmentID,
                        pTreatmentDescription= line[treatment_description],
                        pTreatmentDate=line[treatment_date],
                        pNumbLevel=line[numb_lvl],
                        pPainLevel=line[pain_lvl],
                        pSoreLevel=line[sore_lvl],
                        pTenseLevel=line[tense_lvl]
                    )
                    return treatment
        
        return result
   
def updateTreatmentByID(newTreatmentModel):

    treatmentId = newTreatmentModel.treatmentID
    temp_file_path = DB_PATH + ".tmp"
    updated = False
    print("received treatmentId: ", treatmentId)
    with open(DB_PATH, mode='r', encoding='utf-8', newline='') as infile, \
         open(temp_file_path, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            # Skip completely empty rows
            if not row or all(cell.strip() == '' for cell in row):
                continue

            if row[1].strip() == treatmentId:
                row[0] = generateUUID()
                if row[len(row)-1] == 0:
                    row[len(row)-1] = getFormattedDateTime(dateOnly=True)

                addToTreatmentRevisionTable(row)
                new_row = [value for _, value in vars(newTreatmentModel).items()]
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

def deleteTreatmentByID(treatmentId):
    temp_file_path = DB_PATH + ".tmp"
    updated = False
    print("received treatmentId: ", treatmentId)
    with open(DB_PATH, mode='r', encoding='utf-8', newline='') as infile, \
         open(temp_file_path, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            # Skip completely empty rows
            if not row or all(cell.strip() == '' for cell in row):
                continue

            if row[1].strip() == treatmentId:
                updated = True
                continue  # Skip this row, effectively deleting it
            else:
                writer.writerow(row)

    if updated:
        print("UPDATED DB")
        os.replace(temp_file_path, DB_PATH)
    else:
        print("DB NOT UPDATED")
        os.remove(temp_file_path)

    return updated

def addToTreatmentRevisionTable(data):
    with open(TREATMENT_REVISION_PATH, mode='a', encoding='utf-8', newline='\n') as file:
        # Ensure there's a newline before writing if needed
        file.write("\n")  
        writer_object = writer(file)
        writer_object.writerow(data)

def getAllTreatmentRevisionByID(treatmentID):
    print("treatmentID: ", treatmentID)
    with open(TREATMENT_REVISION_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)    

        treatment_id_index = header.index(dbCol.treatmentId)
        treatment_description = header.index(dbCol.treatmentDescription)
        treatment_date = header.index(dbCol.treatmentDate)    
        pain_lvl = header.index(dbCol.treatmentPainLevel)
        tense_lvl = header.index(dbCol.treatmentTenseLevel)
        sore_lvl = header.index(dbCol.treatmentSoreLevel)
        numb_lvl = header.index(dbCol.treatmentNumbLevel)
        ammendDate = header.index(dbCol.amendmentDate)
        result = []

        for line in csvFile:
            if line != []:
                print("line[treatment_id_index]: ", line[treatment_id_index])
                if line[treatment_id_index] == treatmentID:
                    print("Adding to result: ", line)
                    treatment = TreatmentModel(
                        pConditionId=line[0],
                        pTreatmentId=line[treatment_id_index],
                        pTreatmentDescription= line[treatment_description],
                        pTreatmentDate=line[treatment_date],
                        pNumbLevel=line[numb_lvl],
                        pPainLevel=line[pain_lvl],
                        pSoreLevel=line[sore_lvl],
                        pTenseLevel=line[tense_lvl],
                        pAmendmentDate= line[ammendDate]
                    )
                    result.append(treatment)
        
        return result
