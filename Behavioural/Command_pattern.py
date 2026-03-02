# Resource - https://algomaster.io/learn/lld/command

"""
Problem: Smart Home Controller
you need to set up a home hub,The hub needs to control various devices:
lights, thermostats, and more.You need a controller that can send commands to these devices.
"""

# =============== Naive Approach

class Lights:

    def turn_on(self):

        print("turning Lights On")
    
    def turn_off(self):

        print("Turning Lights Off")
    
class Thermostat:

    def __init__(self):
        
        self.temp = 30

    def set_temparature(self,tem):
        print(f"Setting Temperature to {tem}")
        self.temp = tem

class SmartHomHub:

    def __init__(self):
        
        self.lights = Lights()
        self.thermostat = Thermostat()
        # self.undo_stack = []

    def turn_on(self):
        self.lights.turn_on()
        # self.undo_stack.append()
    
    def turn_off(self):
        self.lights.turn_off()
    
    def set_temperature(self,new_temp):
        self.thermostat.set_temparature(new_temp)


# home = SmartHomHub()

# home.turn_on()
# home.turn_off()
# home.set_temperature(21)


# Problems

# 1. Tightly Copuled : Every change made to Executors(Lights,Thermostat) need an update in 
#                       SmartHomeHub class Too !
# 2. Poor Scalability : Every new executor needs a refernce in the Controller, which leads to
#                       unexpected brokage of existing code
# 3. No Redo/Undo Support : each operation requires to store each state of the contoller for every action,
#                           needs a giant if or switch block to figure out which action to reverse
# 4. No Reusable Actions : if same turn on light action needs to be triggered from a physical button,
#                           a voice assistant, every trigger point needs its own coupling to light class
# 5. No scheduling or Queuing : user won't able to set rules like turn on the lights at 7pm, because actions 
#                               are hardcoded as method calls


"""
Command Pattern : turns a request into a standalone object containing all the information needed to perform that request.
This lets you parameterize methods with different requests, delay or queue a request's execution, and support undoable operations.

Two Characteristics :
1. Encapsulation of requests as objects:  Each action (turn on light, set temperature, play music) becomes its own object
    implementing a common interface. The object holds a reference to the receiver and knows exactly how to execute (and optionally undo) the action

2. Decoupling of invoker and receiver. The invoker (a button, scheduler, or voice assistant) does not know which receiver it is
    talking to or what the action does. It simply holds a Command reference and calls execute(). 
"""


class RemoteContol:

    def __init__(self):

        self.history = []
    
    def executeCommand(self,command):
        command.execute()
        self.history.append(command)

    def undo_last(self):

        if self.history:
            last_cmd = self.history.pop()
            last_cmd.undo()
        else:
            print("No Commands to Undo")

class Light:

    def on(self):
        print("Turning Lights On")
    
    def off(Self):
        print("Turnin Lights Off")

class Thermostat:

    def __init__(self):
        
        self.curentTemp = 25
    
    def set_temperature(self,new_temp):

        self.curentTemp = new_temp

    def get_current_temperature(self):
        return self.curentTemp

from abc import ABC,abstractmethod

class Command(ABC):

    @abstractmethod
    def execute(self):
        pass
    @abstractmethod
    def undo(self):
        pass

class LightOnCommand(Command):

    def __init__(self,light):
        
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()

class LightOffCommand(Command):
        
    def __init__(self,light):
        
        self.light = light

    def execute(self):
        self.light.off()

    def undo(self):
        self.light.on()

class SetTemperatureCommand(Command):

    def __init__(self,thermostat,new_temp):
        
        self.thermostat = thermostat
        self.new_temp = new_temp
        self.prev_temp = None

    def execute(self):
        print(f"Setting New Temperature: {self.new_temp}")

        self.prev_temp = self.thermostat.get_current_temperature()
        self.thermostat.set_temperature(self.new_temp)

    def undo(self):
        print(f"Resetting Temperature to Prev {self.prev_temp}")
        self.thermostat.set_temperature(self.prev_temp)





light = Light()
thermostat = Thermostat()

lon = LightOnCommand(light)
lof = LightOffCommand(light)

set_temp = SetTemperatureCommand(thermostat,10)
set_temp2 = SetTemperatureCommand(thermostat,20)

remote = RemoteContol()

remote.executeCommand(lon)
remote.executeCommand(set_temp)
remote.executeCommand(set_temp2)
remote.executeCommand(lof)

remote.undo_last()
remote.undo_last()
remote.undo_last()
remote.undo_last()
remote.undo_last()
