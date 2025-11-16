
from datetime import datetime

class LegacyPayment:

    def __init__(self):
        
        self.tran_id = 0

        self.is_payment_suc = False

    def execute_trans(self,amount,cur):

        print(f"Legacy Payment GateWay for {amount} and {cur}")

        self.tran_id = datetime.now()
        self.is_payment_suc = True

        print("Payment Is Completed")
    
    def is_payment_status(self):

        return self.is_payment_suc
    
    def return_trans_id(self):

        return self.tran_id
    

