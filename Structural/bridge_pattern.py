#  Reference - https://algomaster.io/learn/lld/bridge
# Refactoring Guru - https://refactoring.guru/design-patterns/bridge/python/example
"""
The Problem: Drawing Shapes
Imagine you're building a cross-platform graphics library. It supports rendering shapes like circles and rectangles using different rendering approaches:

 Vector rendering – for scalable, resolution-independent output
 Raster rendering – for pixel-based output
Now, you need to support:

Drawing different shapes (e.g., Circle, Rectangle)
Using different renderers (e.g., VectorRenderer, RasterRenderer)

"""

# Naive Approach

"""
This doesn't satisfies reqirement because here 
Renderer Doesn't give any information about which shape it's rendering !!
"""


from abc import ABC,abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):

    def draw(self):
        
        print("Drawing a Circle")
class Rectangle(Shape):

    def draw(self):
        print("Drawing a Rectangle")
    
# Renderer

class Type(ABC):

    @abstractmethod
    def draw(self,shape):
        pass

class Vector(Type):

    def draw(self,shape:Shape):
        
        print("Drawing With Vectors")
        shape.draw()

class Raster(Type):

    def draw(self,shape:Shape):
        
        print("Drawing With Raster")
        shape.draw()


c1 = Circle()
r1 = Rectangle()
v1 = Vector()
rr1 = Raster()

v1.draw(c1)
v1.draw(r1)

rr1.draw(r1)


#  ================= Bridge Pattern ============
"""
Entities:
1. Abstraction (Composes an Implementor, communicates to implementors only via this) 
2. Refined Abstraction upto N
3. Implementor
4. Concrete Implementation upto N
"""

class ShapeV2(ABC):

    def __init__(self,render):
        self.renderer = render

    @abstractmethod
    def draw(self):
        pass

class Circle(ShapeV2):

    def __init__(self,radius,render):
        
        self.radius = radius
        super().__init__(render)

    def draw(self):
        
        return self.renderer.render_circle(self.radius)

class Rectangle(ShapeV2):

    def __init__(self,wid,leng,render):

        super().__init__(render)
        self.width = wid
        self.length = leng

    def draw(self):
        return self.renderer.render_rectangle(self.width,self.length)
    

class Render(ABC):

    @abstractmethod
    def render_circle(self,radius):
        pass
    @abstractmethod
    def render_rectangle(self,wid,leng):
        pass


class VectorRenderer(Render):

    def render_circle(self, radius):
        
        print(f"Rendering a Circle of Radius {radius} with Vector Renderer")

    def render_rectangle(self, wid, leng):
        print(f"Rendering a Rectangle of Width*Length is {wid}*{leng} with Vector Renderer")

class RasterRenderer(Render):

    def render_circle(self, radius):
        
        print(f"Rendering a Circle of Radius {radius} with Raster Renderer")
        
    def render_rectangle(self, wid, leng):
        print(f"Rendering a Rectangle of Width*Length is {wid}*{leng} with Raster Renderer")



vr = VectorRenderer()
ras = RasterRenderer()

cir1 = Circle(10,vr)
cir2 = Circle(12,ras)

cir1.draw()
cir2.draw()

rec1 = Rectangle(20,50,vr)
rec2 = Rectangle(30,40,ras)

rec1.draw()
rec2.draw()


#  Sample Payment System

# Implementor

class PaymentGateWay(ABC):

    @abstractmethod
    def pay(self,amount):
        pass

# Concrete Implementation

class RazorpayGateWay(PaymentGateWay):

    def pay(self,amount):
        print(f"Paying Amount {amount}/- from Razorpay")

class StripeGateWay(PaymentGateWay):

    def pay(self,amount):
        print(f"Paying Amount {amount}/- from Stripe")

# Abstractor(Payment Type)

class PaymentType(ABC):

    def __init__(self,payment_gateway):
        
        self.pay_gate = payment_gateway
    
    def make_payment(self,amount):

        self.pay_gate.pay(amount)

class CardPayment(PaymentType):

    def __init__(self, payment_gateway):

        super().__init__(payment_gateway)

    def make_payment(self, amount):
        
        super().make_payment(amount)

class UPIPayment(PaymentType):

    def __init__(self, payment_gateway):

        super().__init__(payment_gateway)
    
    def make_payment(self, amount):
        
        super().make_payment(amount)


#  Client

gateway = RazorpayGateWay()

payment = CardPayment(gateway)
payment.make_payment(100)


payment = UPIPayment(StripeGateWay())
payment.make_payment(1000)