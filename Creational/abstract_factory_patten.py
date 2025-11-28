
# Reference - https://algomaster.io/learn/lld/abstract-factory

"""
1. The Problem: Platform-Specific UI
Imagine you're building a cross-platform desktop application that must support both Windows and Linux.

To provide a good user experience, your application should render native-looking UI components for each operating system like:
Buttons,Checkboxes,Text fields,Menus etc

"""


## Naive Implementation

## Windows UI Components

class WindowsButton:

    def paint(self):

        print("Painting on windows style button")
    
    def on_click(self):

        print("Windows button clicked.")

class WindowsCheckbox:

    def paint(self):

        print("Painting a window checkbox..")
    
    def on_click(self):

        print("Windows checkbox is clicked..")

## Linux UI Components

class LinuxButton:

    def paint(self):

        print("Painting in Linux Style button")

    def on_click(self):

        print("Clcking on a Linux Button")

class LinuxCheckbox:

    def paint(self):

        print("Painting a Linux Checbox")
    
    def on_click(self):
        
        print("Linux Checkbox clicked")


import platform

class App:

    @staticmethod
    def main():

        os = platform.system()

        if "windows"in os:
            button = WindowsButton()
            checkbox = WindowsCheckbox()
            button.paint()
            checkbox.paint()
        elif "Linux" in os:

            button = LinuxButton()
            checkbox = LinuxCheckbox()
            button.paint()
            checkbox.paint()

# Call Main

App.main()

"""
Why this approach Breaks Down

1. Tight Coupling to Concrete Classes
    Your main application logic is tightly bound to platform-specific classes (WindowsButton, MacOSCheckbox, etc.).
    This means everywhere you create UI components, you must check the OS manually.
2. No Abstraction or Polymorphism
    You can’t treat buttons or checkboxes generically.
    There’s no common interface like Button or Checkbox to work with.

3.Scalability Issues:
    Add new concrete classes for each platform,Modify every place in your code where platform-specific logic appears

"""


##======================== Abstract Factory =============================

"""
1.The Abstract Factory Design Pattern is a creational pattern that provides an interface 
for creating families of related or dependent objects without specifying their concrete classes.
2.The Abstract Factory Pattern encapsulates object creation into factory interfaces.
3.Each concrete factory implements the interface and produces a complete set of related objects. 
This ensures that your code remains extensible, consistent, and loosely coupled to specific product implementations.

"""

from abc import ABC,abstractmethod

#Abstract Product Interface
class Button(ABC):
    @abstractmethod
    def paint(self):
        pass
    @abstractmethod
    def on_click(self):
        pass

#Concreate Product Classes
class LinuxButton(Button):

    def paint(self):

        print("Painting with Linux Button")
    
    def on_click(self):
        
        print("Clicking on Linux Button")

class WindowsButton(Button):

    def paint(self):
        
        print("Painting With Windows Button")
    
    def on_click(self):

         print("Clicking on Windows Button")
        
# Abstract Product Interface
class Checkbox(ABC):

    @abstractmethod
    def paint(self):
        pass
    @abstractmethod
    def on_click(self):
        pass

#Concreate Product Classes

class LinuxCheckbox(Checkbox):

    def paint(self):

        print("Painting with Linux Checkbox ")
    
    def on_click(self):
        
        print("Clicking on Linux Checkbox")

class WindowsCheckbox(Checkbox):

    def paint(self):
        
        print("Painting with Windows Checkbox ")
    
    def on_click(self):
        
        print("Clicking on Windows Checkbox")
    
# Abstract Factory

class GUIFactory(ABC):

    @abstractmethod
    def create_button(self):
        pass
    
    @abstractmethod
    def create_checkbox(self):
        pass

## Concrete Factories

class WindowsFactory(GUIFactory):

    def create_button(self):
        
        return WindowsButton()
    
    def create_checkbox(self):
    
        return WindowsCheckbox()

class LinuxFactory(GUIFactory):

    def create_button(self):
        return LinuxButton()
    def create_checkbox(self):
        return LinuxCheckbox()

class Application:

    def __init__(self,factory):

        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()
    
    def render_ui(self):
        
        self.button.paint()
        self.checkbox.paint()

class AppLauncher:

    @staticmethod
    def main():

        os = platform.system()

        if "Windows" in os:
            factory = WindowsFactory()
        else:
            factory = LinuxFactory()
        
        app = Application(factory)
        app.render_ui()

if __name__ == "__main__":

    AppLauncher.main()

        
## Real-World Usage        
##============================= Abstract Factory: Cloud Infrastructure Provisioning ===============


## Abstract Product

class VirtualMachine(ABC):
    @abstractmethod
    def provision(self):
        pass

class StorageBucket(ABC):

    @abstractmethod
    def provision(self):
        pass

class FireWallRules(ABC):

    @abstractmethod
    def provision(self):
        pass

# Concrete Products (AWS Family)

class EC2Instance(VirtualMachine):

    def provision(self):
        print("Provisioning AWS EC2")

class S3Bucket(StorageBucket):

    def provision(self):
        print("Provisioning AWS S3")

class SecurityGroups(FireWallRules):

    def provision(self):
        print("Provisioning AWS Security Groups")

# Concrete Products (Azure Family)

class VMInstance(VirtualMachine):

    def provision(self):
        print("Provisioning of Azure VMInstance")

class BlobStorage(StorageBucket):

    def provision(self):
        print("Provisioning of Azure Blob Storage ")
    
class NetworkSecurityGroup(FireWallRules):

    def provision(self):
        print("Provisioning Azure Network Securiy")

# Abstract Factory
class CloudFactory(ABC):

    @abstractmethod
    def create_vir_machn(self):
        pass
    @abstractmethod
    def create_storage(self):
        pass
    @abstractmethod
    def create_firwall(self):
        pass

#Concrete Factories

class AWSFactory(CloudFactory):

    def create_vir_machn(self):
        return EC2Instance()
    def create_storage(self):
        return S3Bucket()
    def create_firwall(self):
        return SecurityGroups()
    
class AzureFactory(CloudFactory):

    def create_vir_machn(self):
        return VMInstance()

    def create_storage(self):
        return BlobStorage()
    
    def create_firwall(self):
        return NetworkSecurityGroup()

## Application

class Application:

    def main(factory):

        vm = factory.create_vir_machn()
        storage = factory.create_storage()
        security = factory.create_firwall()

        vm.provision()
        storage.provision()
        security.provision()

azure = Application.main(AzureFactory())
aws   = Application.main(AWSFactory())
    


