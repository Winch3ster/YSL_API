class CustomerModel():
    def __init__(self, 
                pCustomerId="-",
                pOldCustomerId="", 
                pEmail="-", 
                pIc="-",
                pCustomerName="-",
                pGender="-",
                pRace="-",
                pAddress="-",
                pHandphoneNum="-",
                pInstagram="-",
                pHowDidYouFindUs= "-",
                pWeChat="-",
                pHeight="-",
                pWeight="-",
                pBloodType="-",
                ):
        self.customerId = pCustomerId
        self.oldCustomerId = pOldCustomerId
        self.email = pEmail
        self.ic = pIc
        self.customerName = pCustomerName
        self.gender = pGender
        self.race = pRace
        self.address = pAddress
        self.handphone = pHandphoneNum
        self.instagram = pInstagram
        self.howDidYouFindUs = pHowDidYouFindUs
        self.weChat = pWeChat 
        self.height = pHeight
        self.weight = pWeight
        self.bloodType = pBloodType


    def to_dict(self):
        return {
            'customerId': self.customerId,
            'oldCustomerId': self.oldCustomerId,
            'email': self.email,
            'ic': self.ic,
            'customerName': self.customerName,
            'gender': self.gender,
            'race': self.race,
            'address': self.address,
            'handphone': self.handphone,
            'instagram': self.instagram,
            'howDidYouFindUs': self.howDidYouFindUs,
            'weChat': self.weChat,
            'height': self.height,
            'weight': self.weight,
            'bloodType': self.bloodType
        }
        





