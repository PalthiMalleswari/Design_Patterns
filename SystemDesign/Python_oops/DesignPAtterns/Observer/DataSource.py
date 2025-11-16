
from __future__ import annotations
from typing import List
from abc import ABC,abstractmethod


class IObserver:

    @abstractmethod
    def notify(self):
        pass

class Sheet(IObserver):

    def __init__(self,dataS:DataSource):

        self.data = dataS
        
    def notify(self):

        return sum(self.data.getValue())
    

class Chart(IObserver):

    def __init__(self, data:DataSource):

        self.data = data

    def notify(self):
        
        return f" Chart Rendered For Values " + " ".join(map(str, self.data.getValue()))


class Subject:

    def __init__(self):

        self.observers : List[IObserver] = []

    def addObs(self,obs:IObserver):

        self.observers.append(obs)

    def removeObs(self):

        self.observers.pop()

    def updateObservers(self):

        for obs in self.observers:
            print(obs.notify())


class DataSource(Subject):

    def __init__(self,val):

        self.values = val

        super().__init__()

    def getValue(self):
        return self.values
    
    def setValue(self,value):

        self.values = value

        super().updateObservers()





ds = DataSource([1,2,3])
s = Sheet(ds)
c = Chart(ds)
ds.addObs(s)
ds.addObs(c)

ds.setValue([0,8])
ds.setValue([1,4])

ds2 = DataSource([1,4])
ds2.setValue([1,7])