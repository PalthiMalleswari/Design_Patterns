
from abc import ABC,abstractmethod

from typing import List

class FileSystem(ABC):

    @abstractmethod
    def print_structure():
        pass

    @abstractmethod
    def get_file_size():
        pass

    @abstractmethod
    def delete_file():
        pass

class File(FileSystem):

    def __init__(self,name,size):
        
        self.file_name = name
        self.size = size

    def print_structure(self,ind):
        
        print(ind + f"- {self.file_name} ({self.size}) Kb")

    def get_file_size(self):
        
        return self.size
    
    def delete_file(self):
        
        print(f" Deleting {self.file_name}")


class Folder(FileSystem):

    def __init__(self,name):
        
        self.folder_name =  name
        
        self.files : List[FileSystem] = []

    def add_files(self,file:File):

        self.files.append(file)

    def print_structure(self,ind):
        
        print(ind + f"+ {self.folder_name} /")

        for file in self.files :

            file.print_structure(ind + "  ")

    def get_file_size(self):
        
        t = 0
        for file in self.files:

            t += file.get_file_size()

        print(f"Total {self.folder_name } Folder Size is {t} Kb")

        return t
        
    def delete_file(self):
        
        print(f"Deleting Folder {self.folder_name}")

        for file in self.file:

            file.delete_file()


home = Folder("Home")

doc = Folder("Documents")

pic = Folder("Pictures")

jpg = File("image.pg",10)

mv = File("movie.mp4", 50)

txt = File("test.txt", 20)

doc.add_files(mv)
doc.add_files(txt)

pic.add_files(jpg)

home.add_files(doc)
home.add_files(pic)

home.print_structure("  ")
home.get_file_size()

# print("     " + f"+ check /")