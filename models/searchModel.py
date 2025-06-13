class searchModel():
    def __init__(self, pUserId="", pCustomerName=""):
        self.userId = pUserId
        self.customerName = pCustomerName

    def to_dict(self):
        return {
            'userId': self.userId,
            'customerName': self.customerName
        }