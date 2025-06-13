from utils.generatorFunctions import generateUUID
class TreatmentModel:
    def __init__(self, 
                 pTreatmentId="",
                pConditionId="", 
                pTreatmentDescription="", 
                pTreatmentDate="",
                pPainLevel = 0,
                pTenseLevel = 0,
                pSoreLevel = 0,
                pNumbLevel = 0,
                pAmendmentDate = None
                 ):
          # Placeholder for treatment ID, if needed
        self.conditionID = pConditionId
        self.treatmentID = pTreatmentId if not "" else generateUUID()
        self.treatmentDescription = pTreatmentDescription
        self.painLevel = pPainLevel
        self.tenseLevel = pTenseLevel
        self.soreLevel = pSoreLevel
        self.numbLevel = pNumbLevel
        self.treatmentDate = pTreatmentDate
        self.version = 0
        self.amendmentDate = pAmendmentDate


    def to_dict(self):
        return {
            'conditionID': self.conditionID,
            'treatmentID': self.treatmentID,
            'treatmentDescription': self.treatmentDescription,
            'painLevel': self.painLevel,
            'tenseLevel': self.tenseLevel,
            'soreLevel': self.soreLevel,
            'numbLevel': self.numbLevel,
            'treatmentDate': self.treatmentDate,
            'version': self.version,
            'amendmentDate': self.amendmentDate
        }

