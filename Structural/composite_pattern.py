# Refernce - https://algomaster.io/learn/lld/composite

"""

The Composite Design Pattern is a structural pattern that lets you treat individual objects 
and compositions of objects uniformly.
It’s particularly useful in situations where:

. You need to represent part-whole hierarchies.
. You want to perform operations on both leaf nodes and composite nodes in a consistent way.
. You want to avoid writing special-case logic to distinguish between "single" and "grouped" objects.

"""


from abc import ABC,abstractmethod

class FileExplorer(ABC):

    @abstractmethod
    def get_size(self):
        pass
    @abstractmethod
    def print_structure(self,indent):
        pass
    @abstractmethod
    def delete(self):
        pass


class File(FileExplorer):

    def __init__(self,file_name,size):
        
        self.file_name = file_name
        self.size  =  size
    
    def get_size(self):

        return self.size
    
    def print_structure(self,indent):

        print(indent+"-"+f"{self.file_name} ({self.size})KB ")
    
    def delete(self):
        print(f"Deleting {self.file_name} ({self.size})KB")

class Folder(FileExplorer):

    def __init__(self,folder_name):
        
        self.folder_name = folder_name
        self.contents = []
    
    def add(self,file):
        
        self.contents.append(file)

    def remove_file(self,file):

        self.contents.remove(file)

    def get_size(self):
        
        total = 0

        for file in self.contents:
            total += file.get_size()
        return total
    
    def delete(self):

        for file in self.contents:
            file.delete()
        
        print(f"Deleting {self.folder_name} Folder")
                
    def print_structure(self,indent):
        
        print(indent+"+"+f"{self.folder_name} ({self.get_size()})KB /")

        for file in self.contents:

            file.print_structure(indent+"  ")
    
f1 = File("hello.txt",10)
f2 = File("photo.jpg",5)
f3 = File("image.png",5)

documents = Folder("Documents")
pictures = Folder("Images")

pictures.add(f2)
pictures.add(f3)
documents.add(f1)

home = Folder("Home")
home.add(pictures)
home.add(documents)

home.print_structure("")

print(f" Home Size - {home.get_size()}KB")
home.delete()


#  Formula / expression evaluation using Composite Pattern

"""

(10 + 5) * (3 - 1) / 2
And later you may want to support:

    . Variables (x + y)

    . Nested formulas

    . New operators without changing client code

            (/)
           /   \
         (*)    2
        /   \
     (+)     (-)
    /   \   /   \
  10     5 3     1

Each node is:

    Either a value (leaf)

    Or an operation (composite)

"""


class Expression(ABC):

    @abstractmethod
    def evaluate(self):
        pass

#  Leaf Node
class Number(Expression):

    def __init__(self,number):

        self.number = number
    
    def evaluate(self):
        
        return self.number

# Composite
class Operation(Expression):

    def __init__(self,left,right):
        
        self.left = left
        self.right = right
    
    def evaluate(self):
        pass

# Variables

class Variable(Expression):

    def __init__(self,name,context):
        
        self.var_name = name
        self.context = context
    
    def evaluate(self):
        
        if self.var_name not in self.context:

            return f"{self.var_name} didn't find in context"
        
        return self.context[self.var_name]

# Concrete Operators
class AddOperator(Operation):

    def __init__(self, left, right):

        super().__init__(left, right)
    
    def evaluate(self):
        
        return self.left.evaluate()+self.right.evaluate()

class SubtractOperator(Operation):

    def __init__(self, left, right):

        super().__init__(left, right)

    def evaluate(self):

        return self.left.evaluate() - self.right.evaluate()

class MultiplicationOperator(Operation):

    def __init__(self, left, right):

        super().__init__(left, right)
    
    def evaluate(self):

        return self.left.evaluate() * self.right.evaluate()

if __name__ == "__main__":

    #  (10-3) + (12-7)
    
    exp = MultiplicationOperator(
        SubtractOperator(Number(10),Number(3)),
        SubtractOperator(Number(12),Number(7))
        )
    res = exp.evaluate()
    print(res)
    
    context = {
        'a':10,
        'b':20,
        'c':30,
        'd':40
    }

    exp2 = MultiplicationOperator(
        SubtractOperator(Variable('b',context),Variable('a',context)),
        SubtractOperator(Variable('d',context),Variable('c',context))
        )
    res2 = exp2.evaluate()
    print(res2)





