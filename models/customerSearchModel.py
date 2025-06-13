
class CustomerSearchModel():
    def __init__(self, pUserId="", pCustomerIC = "", pCustomerName="", pEmail = ""):
        self.userId = pUserId
        self.customerIC = pCustomerIC
        self.customerName = pCustomerName
        self.customerEmail = pEmail

    def to_dict(self):
        return {
            "userId": self.userId,
            "customerIC": self.customerIC,
            "customerName": self.customerName,
            "customerEmail": self.customerEmail
        }
    