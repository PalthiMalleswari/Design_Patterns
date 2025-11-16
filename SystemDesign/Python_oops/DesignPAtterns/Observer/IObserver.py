from abc import ABC,abstractmethod

from DataSource import DataSource

class IObserver:

    @abstractmethod
    def notify(self):
        pass

class Sheet(IObserver):

    def __init__(self,dataS:DataSource):

        self.data = dataS.getValue()
        
    def notify(self):

        return self.data.sum()
    

class Chart(IObserver):

    def __init__(self, data:DataSource):

        self.data = data.getValue()

    def notify(self):
        
        return f" Chart Rendered For Values " + " ".join(self.data)