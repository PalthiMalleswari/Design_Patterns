#Reference - https://algomaster.io/learn/lld/facade,
#https://refactoring.guru/design-patterns/facade
#https://refactoring.guru/design-patterns/facade/python/example



"""
The Facade Design Pattern is a structural design pattern that provides a unified, simplified interface to a complex subsystem
making it easier for clients to interact with multiple components without getting overwhelmed by their intricacies.

particularly useful in situations where:
. Your system contains many interdependent classes or low-level APIs.
. The client doesn’t need to know how those parts work internally.
. You want to reduce the learning curve or coupling between clients and complex systems.
"""

"""
Entities:
1. Item(Price,Quantity,type,discount) Methods:updateQuntity()
2. Cart(List<Items>) Methods: addItem,removeItem(item),UpdateQuant(Item,quantity),validate(cart)
3. Discount(Cart) Methods: apply_coupon(cart,coupon),apply_product_dis(cart),apply_cart_levl_disc(cart)
4. Address(Building/Flat,Street,City,Postal Code,address_type,is_default) Methods: add_address(address),get_default_address()
5. Pricing(Cart,Discount) Methods: calculate_amount,total_charges
6. Payment(Payment_Type,Payment_processor) Methods: pay(amount)
7. Order(OrderID,payment,inventory,Items,Address,estimated delivery)
8. Notify_Oder
"""
from typing import List,Dict
import uuid

class Item:

    def __init__(self,type,price,quant,discount,gst):
        
        self.type = type
        self.price = price
        self.quant = quant
        self.discount = discount
        self.gst = gst
    
    def update_quantity(self,new_quant):

        self.quant = new_quant
    
    def total_amount(self):

        return self.price*self.quant

class Cart:

    def __init__(self):
        
        self.cart :List[Item] = []
    
    def addItem(self,item:Item):

        self.cart.append(item)
    
    def removeItem(self,item:Item):

        self.cart.remove(item)

    def update_quantity(self,item:Item,quant):

        if item in self.cart:

            item.update_quantity(quant)
    
    def is_empty(self):

        if len(self.cart) == 0:
            return True
        
        return False

    def cal_total_amount(self):

        amount = 0

        for item in self.cart:

            total+= (item.quant*item.price)

            charges += (item.gst/100)*total

            amount += (total-charges)

        print(f"Total Amount: {amount}")

        return amount

class Pricing:

    def final_amount(self,cart,discounts):
        
        base = self.get_base_amount(cart)

        print(f"Total MRP: {base}")

        gst = self.get_cart_gst(cart)

        print(f"Total GST: {gst}")

        discounts = DiscountEngine(discounts)

        final_amount = discounts.apply_discounts(cart,base)

        print(f"Total After Discounts: {final_amount}")

        print(f"Final Amount To be Paid (discounted_total-gst): {final_amount+gst}")

        return final_amount+gst

    def get_base_amount(self,cart):

        return sum(item.total_amount() for item in cart.cart)
    
    def get_cart_gst(self,cart):

        return sum((item.gst/100)*item.total_amount() for item in cart.cart)



from abc import abstractmethod,ABC

class Discount(ABC):

    @abstractmethod
    def apply_discount(self,cart:Cart,amount):
        pass

class Coupon(Discount):

    def __init__(self,coupon_price):

        self.coupon_price = coupon_price
    
    def apply_discount(self,cart:Cart,amount):
        
        return max(amount-self.coupon_price,0)

class ProductDiscount(Discount):

    def apply_discount(self,cart:Cart,amount):
        
        discounted_total = 0
        
        for item in cart.cart:
            item_total = item.total_amount()
            item_discount = (item.discount / 100) * item_total
            discounted_total += item_total - item_discount
        return discounted_total
    
class CartLevelDiscount(Discount):

    def apply_discount(self, cart:Cart,amount):

        if amount > 2000:
            return amount * 0.95   # 5% off
        return amount
    
class DiscountEngine:

    def __init__(self, discounts: list[Discount]):

        self.discounts = discounts

    def apply_discounts(self, cart, base_amount: float) -> float:

        amount = base_amount
        
        for disc in self.discounts:

            amount = disc.apply_discount(cart, amount)

        return amount

        
class Payment:

    @abstractmethod
    def pay(self,amount):
        pass

class Stripe(Payment):

    def __init__(self,payment_type):
        
        self.payment_type = payment_type

    def pay(self,amount):

        print(f"Stripe [PAYMENT] ₹{amount} paid using {self.payment_type.upper()}")
        return True

class Razorpay(Payment):

    def __init__(self,payment_type):
        
        self.payment_type = payment_type

    def pay(self,amount):

        print(f"Razorpay [PAYMENT] ₹{amount} paid using {self.payment_type.upper()}")
        return True


class Order:

    def __init__(self,cart:Cart,amount,address):

        self.cart = cart.cart
        self.amount = amount
        self.address = address
        self.order_id = str(uuid.uuid4())
    
    def summary(self):

        print("\n------------- ORDER SUMMARY ---------------")
        print(f"Order ID: {self.order_id}")
        print("Items:")
        for item in self.cart:
            print(f"  - {item.type}: {item.quant} x {item.price}")
        print(f"Delivery Address: {self.address}")
        print(f"Total Paid: ₹{self.amount}")
        print("------------------------------------------\n")

class Notification:

    def send(order:Order):
        print(f"[NOTIFICATION] Order {order.order_id} confirmed & message sent to user.")




#================ Facade Class ===================

class CheckoutFacade:

    def checkout(self,items:List[Item],discounts:List[Discount],payment_procesor:Payment,address:str):

        print("\n===== CHECKOUT STARTED =====")

        cart = Cart()

        for item in items:

            cart.addItem(item)

        if cart.is_empty():
            print("Cart is Empty")
            return None
        
        pricing = Pricing()

        final_amount = pricing.final_amount(cart,discounts)

        payment_procesor.pay(final_amount)

        order = Order(cart,final_amount,address)

        order.summary()

        Notification.send(order)

        print("===== CHECKOUT COMPLETE =====")

        return order

if __name__ == "__main__":

    item1 = Item("Milk",100,1,1,1)
    item2 = Item("Cookie",200,2,1,1)

    coupon1 = Coupon(2)
    coupon2 = Coupon(1)

    prod_dis = ProductDiscount()
    cart_dis = CartLevelDiscount()

    payment_procesor = Stripe("wallet")

    facade = CheckoutFacade()

    facade.checkout(
        items=[item1,item2],
        discounts=[prod_dis,cart_dis,coupon1,coupon2],
        payment_procesor=payment_procesor,
        address="Hyderabad,Telangana"
        )




        
    
        

