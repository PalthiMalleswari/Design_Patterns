from abc import ABC, abstractmethod

class ICompressor(ABC):

    @abstractmethod
    def compress():
        pass

class CompressorMP4(ICompressor):

    def compress(self):
        print("MP4 Compressed")

class CompressorWEB(ICompressor):

    def compress(self):
        print("WEB Compressed")