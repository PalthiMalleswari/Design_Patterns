#==========================================================
# Composite Pattern 
#===========================================================


from abc import ABC,abstractmethod
from typing import List

class Item(ABC):

    def get_price():
        pass


class Box(Item):

    def __init__(self):
        
        self.items : List[Item] = []
    
    def add_item(self,item:Item ):

        self.items.append(item)

    def get_price(self):
        
        price = 0

        for item in self.items :

            price += item.get_price()

        return price


class Mouse(Item) :

    def get_price(self):

        return 10
    
class Keyboard(Item) :

    def get_price(self):
        
        return 20
    
class Speaker(Item) :

    def get_price(self):
        
        return 30
    


package = Box()

key_b = Keyboard()

mou = Mouse()

spe = Speaker()

b1 = Box()

b2 = Box()

b3 = Box()

b1.add_item(spe)

b2.add_item(mou)

b3.add_item(key_b)

b4 = Box()

b4.add_item(b3)
b4.add_item(b2)

package.add_item(b4)
package.add_item(b1)

print(package.get_price())

print(b4.get_price())

print(b1.get_price())
