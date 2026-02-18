# Refernce - https://algomaster.io/learn/lld/strategy


"""
Strategy Design Pattern, lets you define a family of algorithms,encapsulate each one in it's own class,
make them interchangable at runtime

At its core, the Strategy pattern is about separating "what varies" from "what stays the same

This pattern becomes valuable when:

You have multiple ways to perform the same operation, and the choice might change at runtime
You want to avoid bloated conditional statements that select between different behaviors
You need to isolate algorithm-specific data and logic from the code that uses it
Different clients might need different algorithms for the same task

"""

"""
The Problem: Shipping Cost Calculation

Imagine you are building an e-commerce platform. 
but shipping costs can be calculated in many different ways depending on business rules:

Flat Rate: A fixed fee regardless of weight or distance
Weight-Based: Cost increases with package weight
Distance-Based: Different rates for different delivery zones
Express Delivery: Premium pricing for faster service
Third-Party API: Dynamic rates from carriers like FedEx or UPS

"""

class Order:

    def __init__(self,items):

        self.items = items
    
    def get_total_weight(self):

        return sum(self.items)

    def get_destibation_zone(self):

        return 'A'

    def get_order_val(self):

        return sum(self.items)
        


class ShippingCostCalculator:

    def calculate_shipping_cost(self,order:Order,strategy_type):

        cost = 0.0

        if strategy_type.lower()=='flat_rate':

            cost = order.get_order_val()
        
        elif strategy_type.lower()=='weight_based':

            cost = order.get_total_weight()*2.5

        elif strategy_type.lower()=='distance_based':

            zone = order.get_destibation_zone()

            if zone=='A':
                cost = 13
            else:
                cost = 40

        elif strategy_type=='third_party_api':

            cost = 7.3+order.get_order_val()

        else:

            raise ValueError(f"Unknown Shiping Strategy: {strategy_type}")

        print(f"Calculated Shipping Cost: ${cost} with {strategy_type}")
        return cost


def checkout():

    ord_price = ShippingCostCalculator()

    ord1 = Order([1,2,3])

    ord_price.calculate_shipping_cost(ord1,'flat_rate')
    ord_price.calculate_shipping_cost(ord1,'weight_based')
    ord_price.calculate_shipping_cost(ord1,'distance_based')
    ord_price.calculate_shipping_cost(ord1,'third_party_api')

checkout()

"""
Pitfalls:
1. New Strategy,Need to modify the class
2. Bloated If-Else If no.of strategies grows
3. Difficult to test the individual strategies 
"""

# ============= Strategy Pattern ===========

"""
# Components In Stategy Pattern:
1. Concrete Strategies with a common method
2. Strategy(Interface,implemented by all concrete strategies)
3. Context Class,had a reference to Strategy Interface (Composition)
4. Client - Selects a strategy and call context for data
"""

from abc import ABC,abstractmethod

class ShippingCostStrategy(ABC):

    @abstractmethod
    def calculate_cost(self):
        pass

class WeightBasedShipping(ShippingCostStrategy):

    def __init__(self,rate):
        
        self.rate_per_kg = rate
        
    def calculate_cost(self,order):

        return order.get_total_weight()*self.rate_per_kg
    
class FlateBasedShipping(ShippingCostStrategy):

    def calculate_cost(self,order:Order):

        return order.get_order_val()
        
class ShippingCostService:

    def __init__(self,strategy:ShippingCostStrategy):
        
        self.strategy = strategy
    
    def set_strategy(self,new_stra):

        self.strategy = new_stra
    
    def calculate_shipping_cost(self,order):

        if self.strategy is None:
            raise ValueError("Shipping strategy not set.")

        cost = self.strategy.calculate_cost(order)
        print(f"ShippingCostService: Final Calculated Shipping Cost: ${cost} "
              f"(using {self.strategy.__class__.__name__})")
        return cost
 

def ecommerce_app_v2():

    ord1 = Order([1,2,3])

    flat_rate = FlateBasedShipping()
    weight_based = WeightBasedShipping(2.5)

    shipping_service = ShippingCostService(flat_rate)

    print("--- Order 1: Using Flat Rate (initial) ---")
    shipping_service.calculate_shipping_cost(ord1)

    print("\n--- Order 1: Changing to Weight-Based ---")
    shipping_service.set_strategy(weight_based)
    shipping_service.calculate_shipping_cost(ord1)

ecommerce_app_v2()

# ============= Payment System ============

"""
Companies like amazon,Swiggy etc provide different payment types like
UPI, Card, Wallet, Net Banking

Real Production Payment WorkFlow

API Request
    ↓
Controller Layer
    ↓
PaymentService (Orchestrator)
    ↓
Fraud Check
    ↓
Strategy Selection
    ↓
Payment Gateway Call
    ↓
Audit Log + Metrics
    ↓
Response

Strategy is NOT the full system.It is just the "algorithm plug" inside a bigger architecture.

"""


from dataclasses import dataclass
import time
import random


@dataclass
class PaymentRequest:
    user_id:str
    amount: float
    currency:str
    payement_method:str


@dataclass
class PaymentResponse:

    status:str
    trans_id:str
    amount:float
    mesg:str


class PaymentStrategy(ABC):
    @abstractmethod
    def validate(self,request:PaymentRequest):
        pass

    @abstractmethod
    def execute(self,request:PaymentRequest):
        pass

class CardPaymentStrategy(PaymentStrategy):

    def validate(self, request):
        
        print("Validating Card Details...")
        if request.amount <= 0:

            raise ValueError("Invalid Amount")
    def execute(self, request:PaymentRequest) -> PaymentResponse:

        print("Connecting to VISA Gateway")

        time.sleep(1)

        if random.choice([True,False]):
            return PaymentResponse(
                status="Success",
                trans_id="Card123",
                amount=request.amount,
                mesg="Card Payment Successful"
            )
        else:

            return PaymentResponse(
                status="Failed",
                amount=request.amount,
                trans_id="Card123",
                mesg="Card Declained"
            )
        
class UPIPaymentStrategy(CardPaymentStrategy):

    def validate(self, request:PaymentRequest):

        print("Validating UPI ID:")
    
    def execute(self, request):
        
        print("Redirecting to UPI Provider..")
        time.sleep(1)

        return PaymentResponse(
            status="Success",
            trans_id="UPI45678",
            amount=request.amount,
            mesg="UPI Payment is Successful"

        )
    

class PaymentStrategyFactory:

    _strategies = {
        "Card":CardPaymentStrategy(),
        "UPI": UPIPaymentStrategy()
    }

    @classmethod
    def get_stategy(cls,method):

        strategy = cls._strategies.get(method)

        if not strategy:

            raise ValueError(f"Unsupported Payment Method: {method}")
        return strategy

class PaymentService:

    def __init__(self,factory:PaymentStrategyFactory):

        self.factory = factory
    
    def process_payment(self,request:PaymentRequest) -> PaymentResponse:

        print("Starting payment processing")

        strategy = self.factory.get_stategy(request.payement_method)

        strategy.validate(request)

        response = strategy.execute(request)

        self.log_transaction(request,response)
        return response

    def log_transaction(self,request,response):

         print(f"[AUDIT] User {request.user_id} | "
              f"Amount {request.amount} | Status {response.status}")



request = PaymentRequest(
    user_id="user_1",
    amount=500,
    currency="INR",
    payement_method="Card"
)

service = PaymentService(PaymentStrategyFactory())
response = service.process_payment(request)

print(response)

# ========================= Text Formatter Task ========================

"""
Build a text formatting system where different strategies format text in different ways. The TextEditor context should allow swapping formatters at runtime,
so the same editor can produce uppercase, lowercase, or title case output depending on the active strategy.
"""

from abc import ABC, abstractmethod


class TextFormatter(ABC):
    @abstractmethod
    def format(self, text: str) -> str:
        pass


class UpperCaseFormatter(TextFormatter):
    def format(self, text: str) -> str:
        return text.upper()


class LowerCaseFormatter(TextFormatter):
    def format(self, text: str) -> str:
        return text.lower()


class TitleCaseFormatter(TextFormatter):
    def format(self, text: str) -> str:
        return text.title()


class TextEditor:
    def __init__(self, formatter: TextFormatter):
        self._formatter = formatter

    def set_formatter(self, formatter: TextFormatter):
        self._formatter = formatter

    def publish_text(self, text: str):
        print(self._formatter.format(text))


if __name__ == "__main__":
    # pass
    editor = TextEditor(UpperCaseFormatter())
    editor.publish_text("hello world from strategy pattern")

    editor.set_formatter(LowerCaseFormatter())
    editor.publish_text("Hello World From Strategy Pattern")

    editor.set_formatter(TitleCaseFormatter())
    editor.publish_text("hello world from strategy pattern")

        
