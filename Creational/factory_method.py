
from abc import ABC,abstractmethod


## 1. Simple Email Notification System

class EmailSender:

    def send(self,mesg):

        print(f"Sending a Mail with Message : {mesg}")

#usage
class NotificationService:

    def send_notification(self,mesg):

        email = EmailSender()
        email.send(mesg)


not1 = NotificationService()

not1.send_notification("Hii Mary,")

## 2. Notification System (Email,SMS,Push,Slack,WhatsApp) V2 class

class NotificationService:

    def send_notification(self,type,mesg):

        if type == "email":
            email = EmailNotification()
            email.send(mesg)

        elif type == "sms":
            sms = SMSNotification()
            sms.send(mesg)

        elif type == "whatsapp":
            whatsapp = whatsapp()
            whatsapp.send(mesg)

"""
This becomes a nightmare to maintain:

1. Every time you add a new notification channel, you must modify the same core logic.
2. Testing becomes cumbersome because the logic is intertwined with object creation.
3. It violates key design principles, especially the Open/Closed Principle—the idea that classes should be open for extension but closed for modification.

"""

## Clean It Up with a Simple Factory

class SimpleNotificationFactory:
    @staticmethod

    def create_instance(type):

        if type == "email":
            return EmailNotification()

        elif type == "sms":
            return SMSNotification()

        elif type == "push":
            return PushNotification()
    
    def send(self,type,mesg):
        notifi = SimpleNotificationFactory.create_instance(type)
        notifi.send(mesg)
           

"""
Your system is better, but it's still not open to extension without modification.
You're still hardcoding the decision logic and centralizing creation in one place.

"""


#========================== Factory Method ==================

"""
The Factory Method Pattern takes the idea of object creation and hands it off to subclasses.
Instead of one central factory deciding what to create, 
you delegate the responsibility to specialized classes that know exactly what they need to produce.
"""

## Class Diagram Classes
"""
1.Product (e.g., Notification): An interface or abstract class for the objects the factory method creates.
2.ConcreteProduct (e.g., EmailNotification, SMSNotification): Concrete classes that implement the Product interface.
3.Creator (e.g., NotificationCreator): An abstract class (or an interface) that declares the factory method, which returns an object of type Product. It might also define a default implementation of the factory method. The Creator can also have other methods that use the product created by the factory method.
4.ConcreteCreator (e.g., EmailNotificationCreator, SMSNotificationCreator): Subclasses that override the factory method to return an instance of a specific ConcreteProduct.

"""

#======= Implementing Factory Method ==============

#Product
class Notification(ABC):

    @abstractmethod
    def send(self,message):
        pass

# Concrete Products
class EmailNotification(Notification):

    def send(self,message):

        print(f"Sending Email with subject {message}")

class SMSNotification(Notification):

    def send(self,message):

        print(f"Sending SMS Notification with message {message}")

class PushNotification(Notification):

    def send(self,mesg):

        print(f"Sending push notification: {mesg}")

#Abstract Creator (the abstract creator defines the flow, not the details)
class NotificationCreator(ABC):

    @abstractmethod
    def create_notification(self):
        pass

    def send(self,mesg):
        notify = self.create_notification()
        notify.send(mesg)

#Concrete Creators

class EmailNotificationCreator(NotificationCreator):

    def create_notification(self):
        return EmailNotification()
    
class SMSNotificationCreator(NotificationCreator):
    def create_notification(self):
        return SMSNotification()

class PushNotificationCreator(NotificationCreator):
    def create_notification(self):
        return PushNotification()
    

email_creator = EmailNotificationCreator()
email_creator.send("Welcome to Gmail")

sms_creator = SMSNotificationCreator()
sms_creator.send("Sent a SMS")

push_creator = PushNotificationCreator()
push_creator.send("sent a push notify")


