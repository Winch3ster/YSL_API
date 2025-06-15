from flask import Flask,jsonify,request
from APIs.customer.databaseManipulationFunctions import searchForSingleUser, getAllCustomers, updateCustomerByID, registerCustomer
from APIs.condition.conditionDbFunctions import getAllConditionsByCustomerId, updateConditionByID, getConditionById
from APIs.treatment.treatmentDatabaseFunctions import getAllTreatmentByConditionID,createTreatment, getTreatmentByID, getAllTreatmentRevisionByID,updateTreatmentByID, deleteTreatmentByID
from APIs.security.security import authenticateUser,updatePassword
from flask_cors import CORS
from models.conditionModel import ConditionModel
from models.treatmentModel import TreatmentModel
from models.customerObjectModel import CustomerModel
from APIs.condition.conditionDbFunctions import insertConditionToDb
from utils.generatorFunctions import generateUUID
from utils.converterFunctions import getFormattedDateTime
from constants.errorCode import SUCCESS, ERROR, NO_USER_FOUND, INVALID_TIME, INVALID_CREDENTIALS
from APIs.files.customerFilesServices import customerHasConsentForm,uploadCustomerFile,viewCustomerFilePDF
import os
import constants.termConstants as tc
import constants.dbColumn as dbTerm 


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/')
def home():
    allCustomers = getAllCustomers()
    result = []
    for customer in allCustomers:
        result.append(customer.to_dict())
    return jsonify(result)

@app.route('/registerCustomer/', methods=['POST', 'OPTIONS'])
def register_customer():
    if request.method == 'OPTIONS':
        return '', 200  # Preflight response
    data = request.json
    customer = CustomerModel(
        pCustomerId=generateUUID(),
        pOldCustomerId= data['oldCustomerId'], 
        pEmail=data['email'],
        pIc = data['ic'],
        pCustomerName= data['customerName'],
        pGender=data['gender'],
        pRace=data['race'],
        pAddress=data['address'],
        pHandphoneNum=data['handphone'],
        pInstagram=data['instagram'],
        pHowDidYouFindUs=data['discoveryMethod']
    )
    status = registerCustomer(customer)
    if status:
        return jsonify({"Status":SUCCESS, "message": "OK" }), 200
    else:
        return jsonify({"Status": ERROR, "message": "Error registering customer"}), 401
    




@app.route('/customer/<string:id>', methods=['GET'])
def get_customer_by_id(id):
    print("Received request for customer ID:", id)
    customer = searchForSingleUser(str(id))
    print("Customer found:", customer)
    print("Customer id:", customer.customerId)
    return jsonify(customer.to_dict()) if customer else jsonify({"error": "Customer not found"})



@app.route('/editCustomerDetails/<string:id>', methods=['POST', 'OPTIONS'])
def update_customer_by_id(id):
    if request.method == 'OPTIONS':
        return '', 200  # Preflight response
    data = request.json
    customer = CustomerModel(
        pCustomerId=id,
        pOldCustomerId= data['oldCustomerId'], 
        pEmail=data['email'],
        pIc = data['ic'],
        pCustomerName= data['customerName'],
        pGender=data['gender'],
        pRace=data['race'],
        pAddress=data['address'],
        pHandphoneNum=data['handphone'],
        pInstagram=data['instagram'],
        pHowDidYouFindUs=data['discoveryMethod']
    )
    status = updateCustomerByID(customer)
    if status:
        return jsonify({"Status":SUCCESS, "message": "OK" }), 200
    else:
        return jsonify({"Status": ERROR, "message": "Error updating treatment"}), 401



@app.route('/customerConditions/<string:id>', methods=['GET'])
def get_customer_conditions(id):
    conditions = getAllConditionsByCustomerId(str(id))
    result = [condition.to_dict() for condition in conditions]
    return jsonify({"data": result}),200

@app.route('/treatments/<string:id>', methods=['GET'])
def get_all_treatments_by_condition_ID(id):
    treatments = getAllTreatmentByConditionID(str(id))
    result = [treatment.to_dict() for treatment in treatments]
    return jsonify(result) if result else jsonify([])

@app.route('/addTreatment', methods=['POST', 'OPTIONS'])
def add_treatment():
    if request.method == 'OPTIONS':
        return '', 200  # Preflight response
    data = request.json
    print("Received data:", data)
    treatment = TreatmentModel(
        pTreatmentId=generateUUID(),
        pConditionId=data['conditionId'], 
        pTreatmentDescription=data['treatmentDescription'],
        pNumbLevel= data['numbLevel'],
        pPainLevel= data['painLevel'],
        pSoreLevel= data['soreLevel'],
        pTenseLevel= data['tenseLevel'],
        pTreatmentDate=data['treatmentDate'],
    )
    
    result = createTreatment(treatment)
    return jsonify(result), 201

@app.route('/treatmentDetails/<string:id>', methods=['GET'])
def get_treatment_details(id):
    treatmentDetails = getTreatmentByID(id)
    treatmentRevision = getAllTreatmentRevisionByID(id)
    result = {
        "treatmentDetails": treatmentDetails.to_dict() if treatmentDetails else None,
        "treatmentRevision": [t.to_dict() for t in treatmentRevision]
    }
    return jsonify(result)


@app.route('/editTreatment/<string:id>', methods=['POST', 'OPTIONS'])
def edit_treatment(id):
    if request.method == 'OPTIONS':
        return '', 200  # Preflight response
    data = request.json
    treatment = TreatmentModel(
        pTreatmentId=id,
        pConditionId=data['conditionId'], 
        pTreatmentDescription=data['treatmentDescription'],
        pNumbLevel= data['numbLevel'],
        pPainLevel= data['painLevel'],
        pSoreLevel= data['soreLevel'],
        pTenseLevel= data['tenseLevel'],
        pTreatmentDate=data['treatmentDate'],
        pAmendmentDate=getFormattedDateTime(),
    ) 
    status = updateTreatmentByID(treatment)
    if status:
        return jsonify({"Status":SUCCESS, "message": "OK" }), 200
    else:
        return jsonify({"Status": ERROR, "message": "Error updating treatment"}), 401


@app.route('/addCondition', methods=['POST', 'OPTIONS'])
def add_condition():
    if request.method == 'OPTIONS':
        return '', 200  # Preflight response
    data = request.json
    print("Received data:", data)
    condition = ConditionModel(
        customerId=data['customerId'],
        condition_id=generateUUID(),
        conditionDescription=data['conditionDescription'],
        undergoingTreatment=data['undergoingTreatment'],
        conditionDate=getFormattedDateTime()
    )
    insertConditionToDb(condition)
    return jsonify({"message": "Condition added successfully"}), 201

@app.route('/editCondition/<string:id>', methods=['POST', 'OPTIONS'])
def edit_condition_details(id):
    if request.method == 'OPTIONS':
        return '', 200  # Preflight response 
    data = request.json
    try:
        existingData = getConditionById(id)
        if existingData is not None:
            newConditionModel = ConditionModel(
                condition_id=id,
                customerId= existingData.customerId,
                conditionDescription=data['conditionDescription'],
                undergoingTreatment=data['undergoingTreatment'],
                conditionDate=existingData.conditionDate
            )
            result = updateConditionByID(newConditionModel)
            if result: 
                return jsonify({"message": "Successfully updated condition"}), 200
        return jsonify({"message": "Failed to find condition"}), 404

    except:
        return jsonify({"message": "Failed to update condition"}), 404




@app.route('/authenticate', methods=['POST', 'OPTIONS'])
def authenticate():
    if request.method == 'OPTIONS':
            return '', 200  # Preflight response
    data = request.json
    data = authenticateUser(data['username'], data['password'])
    if data is None:
        return jsonify({"name":"-", "username": "-", "Role":tc.guest }), 200
    else:
        return jsonify({"name":data[dbTerm.name], "username": data[dbTerm.username], "role": data[dbTerm.role]}), 200


@app.route('/updatePassword', methods=['POST', 'OPTIONS'])
def update_password():
    if request.method == 'OPTIONS':
            return '', 200  # Preflight response
    data = request.json
    status = updatePassword(data['oldPassword'], data['newPassword'])
    if status:
        return jsonify({"Status":SUCCESS, "message": "OK" }), 200
    else:
        return jsonify({"Status": ERROR, "message": "Incorrect old Password!"}), 401

@app.route('/deleteTreatment/<string:id>', methods=['DELETE'])
def delete_treatment_by_id(id):
    result = deleteTreatmentByID(id)
    if result: 
        return jsonify({"message": f"Treatment with ID {id} deleted successfully"}), 200

    else:
        return jsonify({"message": "Treatment not found"}), 404



@app.route('/customerConsentForm/<string:id>', methods=['GET'])
def customer_has_consent_form(id):
    print("Received request for customer ID:", id)
    status = customerHasConsentForm(str(id))
    return jsonify({"hasConsentForm" : True}) if status else jsonify({"hasConsentForm" : False})

@app.route('/uploadCustomerConsentForm', methods=['POST'])
def handle_file_upload():
    try:
        file = request.files['file']
        customer_id = request.form['customerId']
        file_name = request.form['fileName']

        result = uploadCustomerFile(customer_id, file, file_name)
        return  jsonify({"status" : SUCCESS}), 200
    except:
         return jsonify({"status" : ERROR}), 400
    
@app.route('/viewCustomerConsentForm/<string:id>', methods=['GET'])
def view_consent_form(id):
    viewCustomerFilePDF(id)



if __name__ == '__main__':
    app.run(debug=True)