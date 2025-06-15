from utils.generatorFunctions import generateUUID
class UserModel:
    def __init__(   self, 
                    pId="",
                    pName="",
                    pUsername ="",
                    pPassword ="",
                    pRole = ""
                 ):
          # Placeholder for treatment ID, if needed
        self.id = pId
        self.name = pName
        self.username = pUsername
        self.password = pPassword
        self.role = pRole


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'role': self.role,
        }

