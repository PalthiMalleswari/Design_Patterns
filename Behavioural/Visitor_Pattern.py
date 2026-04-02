# Reference - https://algomaster.io/learn/lld/visitor , https://refactoring.guru/design-patterns/visitor

"""
Problem - Imagine you are building a vector graphics editor that supports multiple shape types:
Circle,Rectangle, Each shape is part of a common hierarchy and must support a variety of operations, such as:
Rendering on screen, Calculating area, Exporting to SVG, Serializing to JSON
"""

class Circle:
    def __init__(self,r):
        self.r = r
    def draw(self):
        print("Drawing A Circle")
    def calculate_area(self):
        a = 3.15*self.r*self.r
        print(f"Area Of Circle is {a}")
    def export_to_svg(self):
        print("Exporting Circle to SVG")
    
class Rectangle:

    def __init__(self,l,w):
        self.l = l
        self.w = w
    def draw(self):
        print("Drawing Rectangle")
    
    def calculate_area(self):
        a = self.l*self.w
        print(f"Area of Rectangle is {a}")
    def export_to_svg(self):
        print("Exporting Rectangle to SVG")

#============= Problem ==========
# Violation of Single Responsibility - Shape Class Was Deeling with more than one functionality which makes class bloated
# Hard To Extend - Every New Functionality Needs to be implemented which breaks the Open/Closed Princple, which breaks existing working code
# We Don't Alwas controll the classes - What if Shape Class Resides in Third Party Modules, We can't modify

# ========= What We Need ==========
# We Need to Seperate Algorithm from the objects it applys on
# Able to Add New Functionality Without Changing Existing Functionality

"""
Visitor Pattern: Visitor is a behavioral design pattern that lets you separate algorithms from the objects on which they operate.
Characterstics :

1. Seperation of Algorithms and Structure: data class stays clean, all the operation logic lives in
visitor classes.
2. Double Dispatch: Correct Method to call visitors functionality depends on type of the visitor and type of element
So, element calls back the visitors with "this",which resolves the element concreate type checkings, it avoids usages of instanceof checks
"""

# Element Interface(Shape)

from abc import ABC,abstractmethod
class Shape(ABC):

    @abstractmethod
    def accept(visitor):
        pass

class Circle(Shape):
    def __init__(self,r):
        self.r = r
    
    def get_radius(self):
        return self.r
    
    def accept(self, visitor):
        visitor.visit_circle(self)
    
class Rectangle(Shape):
    def __init__(self,h,w):
        self.h = h
        self.w = w

    def get_width(self):
        return self.w
    
    def get_height(self):
        return self.h
    
    def accept(self,visitor):
        visitor.visit_rectangle(self)

class ShapeVisitor(ABC):

    @abstractmethod
    def visit_circle(self,circle):
        pass

    @abstractmethod
    def visit_rectangle(self,rectangle):
        pass

class AreaCalculatorVisitor(ShapeVisitor):

    def visit_circle(self, circle):
        area = 10 * circle.get_radius() * circle.get_radius()
        print(f"Area Of Circle is :{area}")
        
    def visit_rectangle(self, rectangle):
        area = rectangle.get_width() * rectangle.get_height()
        print(f"Area Of Rectangle is: {area}")

class SvgExporterVisitor(ShapeVisitor):

    def visit_circle(self, circle):
        print(f'<circle r="{circle.get_radius()}" />')
    
    def visit_rectangle(self, rectangle):
        print(f'<rect width="{rectangle.get_width()}" height="{rectangle.get_height()}" />')


def main():
    shapes = [
        Circle(5),
        Rectangle(10, 4),
        Circle(2.5)
    ]
    
    print("=== Calculating Areas ===")
    area_calculator = AreaCalculatorVisitor()
    for shape in shapes:
        shape.accept(area_calculator)
    
    print("\n=== Exporting to SVG ===")
    svg_exporter = SvgExporterVisitor()
    for shape in shapes:
        shape.accept(svg_exporter)

if __name__ == "__main__":
    main()