# Reference - https://algomaster.io/learn/lld/chain-of-responsibility

# Problem - Handling HTTP Requests

"Building  a backend server that processes incoming HTTP Requets for Web"
"Request should go to Authentication and Authorization,Rate Limiting,Data Validation"

class Request:
    def __init__(self,user,user_role,request_cnt,payload):

        self.user = user
        self.user_role = user_role
        self.request_cnt = request_cnt
        self.payload = payload

class RequestHandler:

    def __init__(self,request):
        self.request = request
    
    def handle(self):

        if not self.authentication():
            print(f"User {self.request.user} is not Authenticated")
            return
        if not self.authorization():
            print(f"User {self.request.user} is not Authorized")
            return
        if not self.rate_limiting():
            print(f"User {self.request.user}'s Rate Limiting Exceeded")
            return
        if not self.validation():
            print(f"Validation Failed {self.request.user}")
            return
        
        print("Passed All Validations !")
    
    def authentication(self):
        return self.request.user is not None

    def authorization(self):
        return self.request.user_role == 'ADMIN'
    
    def rate_limiting(self):
        return self.request.request_cnt < 4
    
    def validation(self):
        return self.request.payload
            

req = Request(None, "ADMIN", 2, '{ "data": 123 }')
req2 = Request("john_doe", "User", 4, '{ "data": 123 }')
req3 = Request("john_doe", "ADMIN", 3, '{ "data": 123 }')
req4 = Request("john_doe", "ADMIN", 4, '{ "data": 123 }')
req5 = Request("john_doe", "ADMIN", 2, '')

processor = RequestHandler(req)
processor2 = RequestHandler(req2)
processor3 = RequestHandler(req3)
processor4 = RequestHandler(req4)
processor5 = RequestHandler(req5)

# processor.handle()
# processor2.handle()
# processor3.handle()
# processor4.handle()
# processor5.handle()

# ============== Problems With This Design ==============
"""
1. Violation of Open/Closed Principle: Every time new method comes,it needs to be added in handle method too
    Which may violate the exiting behaviour
2. No Reusability : If Other Services also need to support Authorization etc, We need to duplicate the same logic
3. Inflexible Configuration : If User wanted to recorder or skip few steps like you need to skip authorization for public apis
    we need to add mpre conditions
4. Tightly Coupled: Each Logic is tightly coupled in a single class, violates the Single Responsibility
"""
#  ============== Chain of Responsibility ==============

from abc import ABC,abstractmethod

class RequestHandler(ABC):

    @abstractmethod
    def handle(self,request):
        pass

class BaseRequestHandler(RequestHandler):

    def __init__(self):
        self.next_handler =  None
    
    def set_next_handler(self,handler):
        self.next_handler = handler

    @abstractmethod
    def handle(self,request):
        pass

    def next_process(self,request):
        self.next_handler.handle(request)


class Authentication(BaseRequestHandler):
    
    def handle(self,request):
        if request.user is None:
            print(f"User {request.user} is not Authenticated")
            return

        self.next_process(request)

class Authorization(BaseRequestHandler):

    def handle(self, request):

        if request.user_role.lower() != "ADMIN".lower():
            print(f"User {request.user} is not Authorized")
            return

        self.next_process(request)

class RateLimitig(BaseRequestHandler):

    def handle(self,request):

        if request.request_cnt >= 4:
            print(f"User {request.request_cnt}'s Rate Limiting 3 Exceeded")
            return 
        
        self.next_process(request)

class Validation(BaseRequestHandler):

    def handle(self, request):
        
        if not request.payload:

            print(f"Validation Failed {request.user}")
            return 
        
        print("Passed All Validations !")


class RequestHandlerV2():

    def handle(self,request):

        auth = Authentication()
        autrz = Authorization()
        rtlm = RateLimitig()
        valid = Validation()

        auth.set_next_handler(autrz)
        autrz.set_next_handler(rtlm)
        rtlm.set_next_handler(valid)

        auth.handle(request)

req_handle = RequestHandlerV2()
req_handle.handle(req)
req_handle.handle(req2)
req_handle.handle(req3)
req_handle.handle(req4)
req_handle.handle(req5)

# =============== ATM Cash Dispenser =============
class CashRequest:
    def __init__(self, amount: int):
        self.amount = amount

class CashRequestHandler(ABC):
    
    @abstractmethod
    def set_next(self,handler):
        pass 

    @abstractmethod
    def dispense(self,request):
        pass

class BaseCashHandler(CashRequestHandler):

    def __init__(self,denorm):
        self.denomination = denorm
        self.next = None
    
    def set_next(self,handler):
        self.next = handler

    def dispense(self, request):
        if request.amount >= self.denomination:

            notes_cnt = request.amount // self.denomination
            request.amount = request.amount % self.denomination

            print(f"Dispensing {notes_cnt} x ${self.denomination}")
        
        if self.next:

            self.next.dispense(request)

class HundredDollarHandler(BaseCashHandler):
    def __init__(self):
        super().__init__(100)


class FiftyDollarHandler(BaseCashHandler):
    def __init__(self):
        super().__init__(50)


class TwentyDollarHandler(BaseCashHandler):
    def __init__(self):
        super().__init__(20)


class TenDollarHandler(BaseCashHandler):
    def __init__(self):
        super().__init__(10)

# Usage
hundreds = HundredDollarHandler()
fifties = FiftyDollarHandler()
twenties = TwentyDollarHandler()
tens = TenDollarHandler()

hundreds.set_next(fifties)
fifties.set_next(twenties)
twenties.set_next(tens)

print("--- Withdrawing $380 ---")
request1 = CashRequest(380)
hundreds.dispense(request1)
print(f"Remaining: ${request1.amount}")

print("\n--- Withdrawing $275 ---")
request2 = CashRequest(275)
hundreds.dispense(request2)
print(f"Remaining: ${request2.amount}")