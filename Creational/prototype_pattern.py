# Reference - https://algomaster.io/learn/lld/prototype

"""
The Prototype Design Pattern is a creational design pattern that lets you create new objects by cloning existing ones, instead of instantiating them from scratch.
It’s particularly useful in situations where:

    . Creating a new object is expensive, time-consuming, or resource-intensive.
    . You want to avoid duplicating complex initialization logic.
    . You need many similar objects with only slight differences.

"""
# The Challenge of Cloning Objects
"""
Imagine you have an object in your system, and you want to create an exact copy of it. How would you do it?

1.Create a new object of the same class.
2.Manually copy each field from the original object to the new one.

Problems:
1. many fields are private and hidden behind encapsulation. That means your cloning logic can’t access them directly.
2. (Class-Level Dependency) Even if you could access all the fields, you'd still need to know the concrete class of the object to instantiate a copy.
3. Interface-Only Contexts, in many cases, your code doesn’t work with concrete classes at all—it works with interfaces
"""

#=========================== Prototype Pattern =================

"""
Instead of having external code copy or recreate the object, the object itself knows how to create its clone.
It exposes a clone() or copy() method that returns a new instance with the same data.

This:

Preserves encapsulation
Eliminates the need to know the concrete class
Makes the system more flexible and extensible

The Prototype pattern specifies the kinds of objects to create using a prototypical instance and creates new objects by copying (cloning) this prototype.

"""

# The Problem: Spawning Enemies in a Game

from abc import ABC,abstractmethod

class EnemyPrototype(ABC):

    @abstractmethod
    def clone(self):
        pass


class Enemy(EnemyPrototype):

    def __init__(self,type,health,speed,armored,weapon):

        self.type = type
        self.health = health
        self.speed = speed
        self.armored = armored
        self.weapon  = weapon

    def clone(self):

        return Enemy(self.type,self.health,self.speed,self.armored,self.weapon)

    def set_health(self,health):
        self.health = health

    def print_stats(self):

        print(f"{self.type} [Health: {self.health}, Speed: {self.speed}, Armored: {self.armored}, Weapon: {self.weapon}]")

"""
A Quick Note on Cloning:
Shallow Copy: This implementation performs a shallow copy. It’s fine if all fields are primitives or immutable (like String). But if Enemy had a field like a List, both the original and cloned enemies would share the same list object, which can cause subtle bugs.
Deep Copy: If your object contains mutable reference types, you should create a deep copy in the copy constructor. For example:
"""

class EnemyRegistry:

    def __init__(self):

        self.prototypes = {}

    def register(self,key,prototype):

        self.prototypes[key] = prototype

    def get(self,key):

        prototype = self.prototypes.get(key)

        if prototype is not None:
            return prototype.clone()
        raise ValueError(f"No prototype registered for: {key}")

#usage


class Game:

    def main():

        registry = EnemyRegistry()

        registry.register("flying",Enemy("FlyingEnemy", 100, 12.0, False, "Laser"))
        registry.register("armored", Enemy("ArmoredEnemy", 300, 6.0, True, "Cannon"))

        e1 = registry.get("flying")
        e2 = registry.get("flying")
        e2.set_health(80)
        e3 = registry.get("armored")
        # Print stats to verify
        e1.print_stats()
        e2.print_stats()
        e3.print_stats()

if __name__ == "__main__":

   Game.main()

