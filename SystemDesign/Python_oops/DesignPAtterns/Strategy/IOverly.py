from abc import ABC,abstractmethod

class IOvery(ABC):

    @abstractmethod
    def overly():
        pass

class BlurWhite(IOvery):

    def overly(self):
        print("BlueWhite Overly Applied")
    

class Blur(IOvery):

    def overly(self):
        print("Blur Overly Applied")
    

class Dark(IOvery):

    def overly(self):
        print("Dark Overly Applied")
    

