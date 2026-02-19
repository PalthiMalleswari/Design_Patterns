# Reference - https://algomaster.io/learn/lld/observer

"""
Observer Pattern, defines a one to many relationship between objects, so when one object
changes its sate, all its dependencies(observers) are automatically notified and updated

"""

# Problem : Broadcasting Fitness Data

"""
a Fitness Tracker App that connects to a wearable device. 
The device continuously streams real-time fitness data: steps taken, active minutes, and calories burned.
Now, multiple modules within your app need to react to these updates:

LiveActivityDisplay: Shows real-time stats on the dashboard
ProgressLogger:	Persists data to a database for trend analysis
GoalNotifier: Sends alerts when the user hits milestones
"""

class LiveActivityDisplay:
    
    def show_states(self,fitness):

        print(f"\Displaying New Data - Steps: {fitness.steps}, "
        f"ActiveMins: {fitness.active_minutes}, Calories: {fitness.calories}")


class ProgessLoger:
        
    def log_data(self,fitness):

        print(f"\Logging New Data - Steps: {fitness.steps}, "
        f"ActiveMins: {fitness.active_minutes}, Calories: {fitness.calories}")


class NotificationService:
        def notify(self,steps):

            print(f"Notifination:Goal - Steps: {steps}")


class FitnessData:

    def __init__(self):
        
        self.steps = 0
        self.active_minutes = 0
        self.calories = 0
        
        self.live_display = LiveActivityDisplay()
        self.progess_logger = ProgessLoger()
        self.notification_service = NotificationService()
    
    def new_fitness_data_pushed(self,stp,am,cl):

        self.steps = stp
        self.active_minutes = am
        self.calories = cl

        print(f"\nFitnessDataNaive: New data received - Steps: {self.steps}, "
        f"ActiveMins: {self.active_minutes}, Calories: {self.calories}")

        self.live_display.show_states(self)
        self.progess_logger.log_data(self)
        self.notification_service.notify(self.steps)

    def daily_reset(self):

        if self.notification_service is not None:
            # Reset the daily Notification
            pass

        print("FitnessDataNaive: Daily data reset.")
        self.new_fitness_data_pushed(0, 0, 0)


#  Client Code

def fitness_app():

    fitnes = FitnessData()
    fitnes.new_fitness_data_pushed(100,20,345)
    fitnes.new_fitness_data_pushed(300,720,45)
    fitnes.daily_reset()
    fitnes.new_fitness_data_pushed(500,900,569)

    

# if __name__ == "__main__":

#     fitness_app()

# Problems With This Design

"""
1. Tight Coupling - Fitness Data now knows, all it's dependents, if any one class Changes
    you must modify FitnessData
2. Violates the Open/Closed Principle -Every new Depency should be added as a field to fitnessdata
    modify FitnessData's new_fitness_data method
3. Inflexible and Static Design : Modules like NotificationService or ProgessLogger
    can't be added or removes at runtime (user disable the notification settings)
4. Responsibility Bloats - Along with fitness data, it manages UI updates,notification logic

"""

# =========== Observer Pattern ==============
"""
The Observer Design Pattern provides a clean and flexible solution to the problem of broadcasting changes from one central object (the Subject)
to many dependent objects (the Observers) — all while keeping them loosely coupled.

# Component
 
1.Publisher
2.Subscriber
3.ConcreteSubscriber
"""

# Observer Interface

from abc import ABC,abstractmethod

class FitnessDataObserver(ABC):

    @abstractmethod
    def update(self):
        pass

class LiveActivityDisplayV2(FitnessDataObserver):
    
    def show_states(self,fitness):

        print(f"\Displaying New Data - Steps: {fitness.steps}, "
        f"ActiveMins: {fitness.active_minutes}, Calories: {fitness.calories}")

    def update(self,fitness):

        self.show_states(fitness)

class ProgessLogerV2(FitnessDataObserver):
    
    def __init__(self):
        
        self.fitness = None
        
    def log_data(self):

        print(f"\Logging New Data - Steps: {self.fitness.steps}, "
        f"ActiveMins: {self.fitness.active_minutes}, Calories: {self.fitness.calories}")
    
    def update(self,fitness):
        self.fitness = fitness
        self.log_data()

class NotificationServiceV2(FitnessDataObserver):
        
        def __init__(self):
            
            self.steps_goal = 1000
            self.goal_reached = False

        def notify(self,steps):

            print(f"Notifination:Goal - Steps: {steps}")

        def update(self,fitness):

            if fitness.get_steps()>=self.steps_goal and not self.goal_reached:
                print(f"Notifier → 🎉 Goal Reached! You've hit {self.steps_goal} steps!")
                self.goal_reached = True
        
        def reset(self):
            self.goal_reached = False

class FitnessDataSubject(ABC):

    @abstractmethod
    def register_observer(self,observer):
        pass
    @abstractmethod
    def remove_observer(self,observer):
        pass

    @abstractmethod
    def notify_observers(self):
        pass

class FitnessDataV2(FitnessDataSubject):

    def __init__(self):
        
        self.steps = 0
        self.active_minutes = 0
        self.calories = 0
        self.observers = []
    
    def register_observer(self,observer):

        self.observers.append(observer)
    
    def remove_observer(self, observer):
        
        if observer in self.observers:

            self.observers.remove(observer)
    
    def notify_observers(self):

        for obsrv in self.observers:

            obsrv.update(self)
    
    def new_fitness_data_pushed(self,steps,act_min,cal):

        self.steps = steps
        self.active_minutes = act_min
        self.calories = cal
        
        print(f"\nFitnessData: New data received – Steps: {steps}, "
              f"Active Minutes: {act_min}, Calories: {cal}")
        
        self.notify_observers()
    
    def daily_reset(self):
        self.steps = 0
        self.active_minutes = 0
        self.calories = 0

        print("\nFitnessData: Daily reset performed.")
        self.notify_observers()

    # Getters
    def get_steps(self):
        return self.steps
    
    def get_active_minutes(self):
        return self.active_minutes
    
    def get_calories(self):
        return self.calories


def fitness_app_observer_app():

    fitness_data = FitnessDataV2()

    display = LiveActivityDisplayV2()
    logger = ProgessLogerV2()
    notifier = NotificationServiceV2()

    # Register observers
    fitness_data.register_observer(display)
    fitness_data.register_observer(logger)
    fitness_data.register_observer(notifier)

        # Simulate updates
    fitness_data.new_fitness_data_pushed(500, 5, 20)
    fitness_data.new_fitness_data_pushed(9800, 85, 350)

    fitness_data.remove_observer(logger)
    fitness_data.new_fitness_data_pushed(10100, 90, 380)

    notifier.reset()
    fitness_data.daily_reset()

if __name__ == "__main__":

    fitness_app_observer_app()