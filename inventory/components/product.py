from abc import ABC, abstractmethod
#template, (interface Pattern) create base structure for all products 
class Product(ABC):
     #decorator - forces the subclasses to implement following methods
    @abstractmethod
    def getStock(self):
        pass   #do nothing, just a placeholder

    @abstractmethod
    def reduceStock(self, qty):
        pass

    @abstractmethod
    def getPrice(self):
        pass

        