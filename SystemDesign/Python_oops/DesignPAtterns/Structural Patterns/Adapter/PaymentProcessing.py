
from datetime import datetime

from abc import ABC,abstractmethod

from LegacyPayment import LegacyPayment


class PaymentProcessing(ABC):

    @abstractmethod
    def process_payment(amount,currency):
        pass

    @abstractmethod
    def is_Payment_succ():
        pass

    @abstractmethod
    def get_trans_id():
        pass


class InHandPaymentGateWay(PaymentProcessing):

    def __init__(self):
        
        self.transaction_id = 0

        self.is_Payment_done = False

    def process_payment(self,amount,currency):

        print(f"Inhand Paymemt Started {amount} in currency {currency} ")

        self.is_Payment_done = True

        self.transaction_id = datetime.now()

        print("In Hand Payment Process is Done")

    def is_Payment_succ(self):
        
        return self.is_Payment_done
    
    def get_trans_id(self):
        
        return self.transaction_id
    

class Adapter(PaymentProcessing):

    def __init__(self,adaptee:LegacyPayment):

        self.adaptee = adaptee

    def process_payment(self,amount,cur):

        self.adaptee.execute_trans(amount,cur)

    def is_Payment_succ(self):

        return self.adaptee.is_payment_status()

    def get_trans_id(self):
        
        return self.adaptee.return_trans_id()


class CheckOut():

    def __init__(self,payment:PaymentProcessing):
        
        self.payment_type = payment
    
    def check_out(self,amt,cur):

        self.payment_type.process_payment(amt,cur)

in_hand = InHandPaymentGateWay()

chek_1 = CheckOut(in_hand)

chek_1.check_out(30,'$')

adapte = LegacyPayment()

adpter = Adapter(adapte)

check_2 = CheckOut(adpter)

check_2.check_out(50,'/-')

# adapte = LegacyPayment()

# adpter = Adapter(adapte)

# options = [in_hand,adpter]

# for option in options:

#     option.process_payment(20,'$')
#     print(option.is_Payment_succ())
#     print(option.get_trans_id())


