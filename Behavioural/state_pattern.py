# Reference - https://algomaster.io/learn/lld/state

"""
Problem - Build a Simple Vending Machine System
which should accept money,dispense products,goback to idle,it can be in any one of the state
IdleState: Waiting for user input (nothing selected, no money inserted).
ItemSelectedState: An item has been selected, waiting for payment.
HasMoneyState: Money has been inserted, waiting to dispense the selected item.
DispensingState: The machine is actively dispensing the item.
"""

# =========== Naive Implementation

from enum import Enum

class State(Enum):

    idle = 1
    item_selected = 2
    has_money = 3
    dispensing = 4

class VendingMachine:

    def __init__(self):
        
        self.current_state = State.idle
        self.item_selected = ""
        self.amount = 0
    
    def select_item(self,item_code):

        if self.current_state == State.idle:
            print(f"{item_code} - Item Selected")
            self.current_state = State.item_selected
            self.item_selected = item_code

        elif self.current_state == State.item_selected:
            print(f"Already {self.item_selected} Item Selected !")
        
        elif self.current_state == State.has_money:
            print(f"Payment Already Received for item - {self.item_selected}")

        elif self.current_state == State.dispensing:
            print(f"Currently Dispensing,Please Wait !")
    
    def insert_coin(self,amount):

        if self.current_state == State.item_selected:

            print(f"Inserted Amount - {amount} for Item - {self.item_selected} ")
            self.amount = amount
            self.current_state = State.has_money

        elif self.current_state == State.idle:
            print(f"Please Select Any Item")

        elif self.current_state == State.has_money:
            print("Money Has Already Inserted")

        elif self.current_state == State.dispensing:
            print(f"Please Wait,Currently Dispensing {self.item_selected}")

    def dispense_item(self):

        if self.current_state == State.idle:
            print("Please select any Item")

        elif self.current_state == State.item_selected:
            print(f"Please Insert Money for {self.item_selected}") 

        elif self.current_state == State.has_money:
            print(f"Dispensing Item - {self.item_selected}")
            self.current_state = State.dispensing
            self.reset_machine()

        elif self.current_state == State.dispensing:
            print("Already Dispensing, Please Wait...")

    def reset_machine(self):
        self.current_state = State.idle
        self.item_selected = ""
        self.amount = 0
    

vm = VendingMachine()

vm.insert_coin(30)

vm.select_item('A12')
vm.dispense_item()

vm.insert_coin(20)
vm.select_item('A13')

vm.dispense_item()
vm.insert_coin("40")
vm.select_item('A13')


# Problems With this Design

"""
1. Cluttered Code : All State related logic fec into Single Class, with repetative 
if-else block,leads hard to read and reason the code, duplicate checks

2. Hard to Extend : If New State Like (OutOfStock,Maintainance) needs to implement this state behaviour
in each and every method previously implemented, leads to broke existinf funct (Violates Open/Closed)

3. Violates Single Responsibility: managing State transitions,business ruls,executions specific logic
leads to tight coupling, hard to test
"""

# ============== State Pattern =============

"""
State Pattern, Allows an Object to alter it's behaviour when its internal state changes,
the object appears to change it's class because  its behaviour now delegated to different state object

Characterstics:
1. Encapsulation of State Specific Behaviour: Each state gets its own class,all logic what happens
when user inserted an amount when the machine is in IDLE state now lives in IDLE class, not burried in if-else

2. State-Driven Transitions: State objects handles decide when and how to transition to another state
the contex does not manage transitions through conditionals, it just delegates to current state, to handle the rest
"""

# Components
# 1. Contex Class
# 2. State Interface - Common Interface for all States with methods common methods with Contex as param
# 3. Concrete States - IdleState, ItemSelectedState

from abc import ABC,abstractmethod

class MachineState(ABC):

    @abstractmethod
    def selecte_item(self,contex,item_code):
        pass
    
    @abstractmethod
    def insert_coin(self,context,amount):
        pass
    
    @abstractmethod
    def dispense_item(self,context):
        pass

class IdleState(MachineState):

    def selecte_item(self, contex, item_code):

        print(f"{item_code} - Item Selected")
        contex.set_selected_item(item_code)
        contex.set_state(ItemSelectedState())
    
    def insert_coin(self, context, amount):
        print(f"Please Select Any Item")

    def dispense_item(self, context):
        print("Please select any Item")
        
class ItemSelectedState(MachineState):
    
    def selecte_item(self, contex, item_code):
        
        contex.set_selected_item(item_code)
        print(f"{item_code} - Item Selected")

    def insert_coin(self, context, amount):
        
        print(f"Inserted Amount - {amount} for Item - {context.get_selected_item()} ")
        context.set_inserted_amount(amount)
        context.set_state(HasMoneyState())
    
    def dispense_item(self, context):
        print("Please Insert Amount")
    
class HasMoneyState(MachineState):

    def selecte_item(self, contex, item_code):
        
        print("Can't Change an Item,after inserting money")

    def insert_coin(self, context, amount):
        
        print("Money Already Inserted")
    
    def dispense_item(self, context):

        context.set_state(DispensingState())
        print(f"Dispensing Item - {context.get_selected_item()} ")
        print("Item Dispended Successfully")
        context.reset()
    
class DispensingState(MachineState):

    def selecte_item(self, contex, item_code):
        print("Please wait, dispensing is going on")
    
    def insert_coin(self, context, amount):
        print("Please Wait, dispensing in progess.")
    
    def dispense_item(self, context):
        print("Already dispensing. Please wait.")
        

class VendingMachine:

    def __init__(self):
        
        self._current_state = IdleState()
        self._selected_item = ""
        self._inserted_amount = 0.0
    
    def set_state(self,new_state):
        self._current_state = new_state

    def set_selected_item(self,item_code):
        self._selected_item = item_code

    def set_inserted_amount(self,amount):
        self._inserted_amount = amount
    
    def get_selected_item(self):
        return self._selected_item

    def get_inserted_amount(self):
        return self._inserted_amount

    def select_item(self,item_code):
        self._current_state.selecte_item(self,item_code)

    def insert_coin(self,amount):
        self._current_state.insert_coin(self,amount)

    def dispense_item(self):
        self._current_state.dispense_item(self)

    def reset(self):
        self.set_state(IdleState())
        self._selected_item = ""
        self._inserted_amount = 0.0


def main():
    vm = VendingMachine()

    print("\n--- First Transaction ---")
    vm.insert_coin(1.0)   # Rejected: no item selected
    vm.select_item("A1")  # Transitions to ItemSelectedState
    vm.insert_coin(1.5)   # Transitions to HasMoneyState
    vm.dispense_item()    # Dispenses, resets to IdleState

    print("\n--- Second Transaction ---")
    vm.select_item("B2")
    vm.select_item("B3")
    vm.insert_coin(2.0)
    vm.dispense_item()

    print("\n---- Third Transaction -----")
    vm.select_item("C4")
    vm.select_item("B6")
    vm.insert_coin(9.8)
    vm.dispense_item()

if __name__ == "__main__":
    main()
    
        

# ========== Document Work Flow Example =========

class DocumentState(ABC):

    @abstractmethod
    def edit(self,context,content):
        pass
    
    @abstractmethod
    def submit_for_review(self,context):
        pass

    @abstractmethod
    def reject(self,context):
        pass
    
    @abstractmethod
    def approve(self,context):
        pass
    
    @abstractmethod
    def unpublish(self,context):
        pass

class DraftState(DocumentState):

    def edit(self, context, content):
        print(f"Editing Content - {content}")
        context.set_content(content)
    
    def submit_for_review(self, context):
        print("Submitted For Review")
        context.set_state(UnderReviewState())
    
    def reject(self, context):
        print("Can't Reject in draft state,Submit for Review First")
    
    def approve(self, context):
        print("Can't approve a draft,Submit for Review First.")
    
    def unpublish(self, context):
        print("Can't unpublish a draft, Submit for Review First.")

class UnderReviewState(DocumentState):

    def edit(self,contex,content):
        print("Can't Edit a Doc, while under Review")
    
    def submit_for_review(self,context):
        print("This Doc, Already under Review")
    
    def reject(self,context):
        context.set_state(DraftState())
        print("Doc, Rejected, Returning to Draft")
    
    def approve(self,context):
        print("Successfully Doc Approved and Published")
        context.set_state(PublishedState())

    def unpublish(self,context):
        print("Document not Published Yet")

class PublishedState(DocumentState):

    def edit(self, context, content):
        print("Can't edit a published document, un-publish first")
    
    def submit_for_review(self, context):
        print("Document Already Reviewed and Published")
    
    def reject(self, context):
        print("Can't reject a published Doc")
    
    def approve(self, context):
        print("Document Already Published !")
    
    def unpublish(self, context):
        print("Un published the Document,Returning to Draft")
        context.set_state(DraftState())

class Document:

    def __init__(self):
        
        self._current_state = DraftState()
        self._content = ""
    
    def set_state(self,new_state):
        self._current_state = new_state
    
    def set_content(self,content):
        self._content = content
    
    def edit(self,content):
        self._current_state.edit(self,content)
    
    def submit_for_review(self):
        self._current_state.submit_for_review(self)
    
    def approve(self):
        self._current_state.approve(self)
    
    def reject(self):
        self._current_state.reject(self)
    
    def unpublish(self):
        self._current_state.unpublish(self)


print("---------- Document WorkFlow --------")
doc = Document()

doc.edit("First draft of the article.")
doc.approve()              # Rejected: cannot approve a draft
doc.submit_for_review()
doc.edit("Trying to edit")  # Rejected: under review
doc.reject()                # Back to draft
doc.edit("Revised draft.")
doc.submit_for_review()
doc.approve()               # Published
doc.edit("Trying to edit")  # Rejected: published
doc.unpublish()             # Back to draft

# ============= Traffic Light Controller Example =============

from abc import ABC, abstractmethod

class TrafficLightState(ABC):
    @abstractmethod
    def change(self, context):
        pass

class RedState(TrafficLightState):
    def change(self, context):
        
        print("RED light - Stop")
        context.set_state(GreenState())

class GreenState(TrafficLightState):
    def change(self, context):
        print("GREEN light - Go")
        context.set_state(YellowState())

class YellowState(TrafficLightState):
    def change(self, context):
        print("YELLOW light - Slow down")
        context.set_state(RedState())

class TrafficLight:
    def __init__(self):
        self._state = RedState()

    def set_state(self, state):
        self._state = state

    def change(self):
        self._state.change(self)

if __name__ == "__main__":
    
    light = TrafficLight()
    light.change()  
    light.change()
    light.change()  
    light.change()  
    light.change()  