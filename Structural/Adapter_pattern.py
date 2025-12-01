# Refernce - https://algomaster.io/learn/lld/adapter

"""
The Adapter Design Pattern is a structural design pattern that allows incompatible interfaces to work together by converting the interface of one class into another that the client expects.
’s particularly useful in situations where:
    . You’re integrating with a legacy system or a third-party library that doesn’t match your current interface.
    . You want to reuse existing functionality without modifying its source code.
    . You need to bridge the gap between new and old code, or between systems built with different interface designs.

"""

# The Problem: Incompatible Payment Interfaces

"""
Imagine you’re building the checkout component of an e-commerce application.
Your Checkout Service is designed to work with a Payment Interface for handling payments.
"""
import time 

# The Expected Interface

class paymentProcessor:

    def process_payment(self,amount,currency):

        raise NotImplementedError
    
    def is_payment_successful(self):

        raise NotImplementedError

    def get_transaction_id(self):

        raise NotImplementedError
    
# In-House Implementation


class InHousePaymentProcessor(paymentProcessor):

    def __init__(self):

        self.transaction_id = None
        self.is_payment_successful_flag  = False

    def process_payment(self, amount, currency):

        print(f"Inhouse Processing for amount {amount} {currency}")
        self.transaction_id = f"TXN_{(time.time()*1000)}"
        self.is_payment_successful_flag = True
        print("Inhouse Processing is Done")

    def is_payment_successful(self):
        return self.is_payment_successful_flag
    
    def get_transaction_id(self):
        return self.transaction_id
    
class CheckoutService:

    def __init__(self,payement_processor):

        self.payment_processor = payement_processor
    
    def checkout(self,amount,currency):

        print(f"CheckoutService: Attempting to process order for ${amount} {currency}")
        
        self.payment_processor.process_payment(amount,currency)
        
        if self.payment_processor.is_payment_successful():
        
            print(f"CheckoutService: Order Successful ! with Transaction ID: {self.payment_processor.get_transaction_id()}")
        
        else:

            print("CheckoutService: Order failed. Payment was not successful.")

   
class LegacyGateway:

    def __init__(self):
        
        self.transaction_reference = None
        self.is_payment_successful_flag = False
    
    def execute_transaction(self,total_amount,currency):

        print(f"Legacy GateWay: Executing Transaction for {currency} {total_amount}")
        self.transaction_reference = time.time_ns()
        self.is_payment_successful_flag = True
        print(f"LEgacyGateWay: Transaction executed Successfully. Txn Id:{self.transaction_reference}")
    
    def check_status(self,transaction_reference):
        return self.is_payment_successful_flag
    
    def get_reference_number(self):
        return self.transaction_reference

# Adapter Pattern

"""
The Adapter acts as a bridge between an incompatible interface and what the client actually expects.
Two Types of Adapters
    1. Object Adaptor(Uses Composition) 
    2. Class Adaptor(Uses Inheritance) (Create a child class to legacy gateway class(parent) with client expected methods and internal each calls respective parent methods)

"""

# Implementing Adaptor Pattern

class LegacyGateWayAdaptor(paymentProcessor):

    def __init__(self):

        self.adaptee = LegacyGateway()
        self.current_ref = None
        
    def process_payment(self,amount,currency):

        self.adaptee.execute_transaction(amount,currency)
        self.current_ref = self.adaptee.get_reference_number()
    
    def is_payment_successful(self):
        return self.adaptee.check_status(self.current_ref)
    
    def get_transaction_id(self):
        return self.current_ref
    


if __name__ == "__main__":

    checkout1 = CheckoutService(InHousePaymentProcessor())

    checkout1.checkout(500,"INR")

    checkout2 = CheckoutService(LegacyGateWayAdaptor())

    checkout2.checkout(900,"INR")



# PITFALLS OF ADAPTER PATTERN

"""
1. Hides Bad Architecture or Legacy Code
2. Performance Overhead Adapters add: Extra method calls,Data transformations,JSON/XML conversion cost
3. If Interface Changes → Adapter Breaks (When the 3rd-party library changes:Your adapter must be updated)
"""

# Use Adapter when

"""
You integrate a 3rd-party library you cannot modify.
You migrate legacy → modern systems.
You standardize multiple implementations behind one interface.
You want to replace a dependency without refactoring entire codebase.
"""


#=======================================================================================
#            REAL-WORLD PAYMENT GATEWAY INTEGRATION USING ADAPTER PATTERN
#=======================================================================================


# 3rd Party Libraries

# ----------------- Stripe SDK ------------------
class StripeSDK:

    def charge(self,amount):
        print("[Stripe] Charging", amount)
        return "stripe_tx_123"
    
    def refund_charge(self, tx_id):
        print("[Stripe] Refunding", tx_id)
        return True
    
    def check_status(self, tx_id):
        return "stripe_status_success"
    
# ----------------- Razorpay SDK ----------------

class RazorpaySDK:
    def pay(self, amount):
        print("[Razorpay] Paying", amount)
        return "rzp_tx_456"

    def reverse(self, tx_id):
        print("[Razorpay] Reversing", tx_id)
        return True

    def info(self, tx_id):
        return "rzp_status_pending"
    
# ----------------- PayPal SDK ------------------

class PayPalSDK:
    def create_payment(self, amount):
        print("[PayPal] Creating payment of", amount)
        return "paypal_tx_789"

    def refund_payment(self, tx_id):
        print("[PayPal] Refunding", tx_id)
        return True

    def payment_details(self, tx_id):
        return "paypal_completed"
    
# Unified Payment Interface

class PaymentProcessor:

    def process(self,amount:float):
        return NotImplementedError
    
    def refund(self, tx_id:str):
        return NotImplementedError
    
    def status(self,tx_id:str):
        return NotImplementedError

# Adapters

# ----------------- Stripe Adapter ------------------

class StripeAdapter(PaymentProcessor):

    def __init__(self):
        self.stripe = StripeSDK()

    def process(self, amount):
        return self.stripe.charge(amount)

    def refund(self, tx_id):
        return self.stripe.refund_charge(tx_id)

    def status(self, tx_id):
        return self.stripe.check_status(tx_id)

# ----------------- Razorpay Adapter ------------------

class RazorpayAdapter(PaymentProcessor):

    def __init__(self):
        self.rzp = RazorpaySDK()

    def process(self, amount):
        return self.rzp.pay(amount)

    def refund(self, tx_id):
        return self.rzp.reverse(tx_id)

    def status(self, tx_id):
        return self.rzp.info(tx_id)

# ----------------- PayPal Adapter ------------------

class PayPalAdapter(PaymentProcessor):

    def __init__(self):
        self.paypal = PayPalSDK()

    def process(self, amount):
        return self.paypal.create_payment(amount)

    def refund(self, tx_id):
        return self.paypal.refund_payment(tx_id)

    def status(self, tx_id):
        return self.paypal.payment_details(tx_id)
    

# Client Code

def pay_user(payment_gateway:PaymentProcessor,amount):

    tx_id = payment_gateway.process(amount)
    print("Transaction:", tx_id)
    print("Status:", payment_gateway.status(tx_id))
    return tx_id


provider = StripeAdapter()
pay_user(provider,500)

razor_provider = RazorpayAdapter()
pay_user(razor_provider,700)

paypal_provider = PayPalAdapter()
pay_user(paypal_provider,900)