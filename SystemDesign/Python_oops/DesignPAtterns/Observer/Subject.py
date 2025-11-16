
from typing import List

from IObserver import IObserver

class Subject:

    def __init__(self):

        self.observers : List[IObserver]

    def addObs(self,obs:IObserver):

        self.observers.append(obs)

    def removeObs(self):

        self.observers.pop()

    def updateObservers(self):

        for obs in self.observers:
            obs.notify()
