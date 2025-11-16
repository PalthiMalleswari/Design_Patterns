
import ICompressor,IOverly

from ICompressor import CompressorMP4,CompressorWEB

from IOverly import BlurWhite,Dark

class VideoStorage:
    
    def __init__(self, comp: ICompressor,over:IOverly):
        
        self._compresor = comp
        self._overlay = over

    def setCompressor(self,comp:ICompressor):

        self._compresor = comp

    def setOverly(self,over:IOverly):

        self._overlay = over

    def storage(self):

        self._compresor.compress()
        self._overlay.overly()



vid = VideoStorage(CompressorMP4(),BlurWhite())

vid.setCompressor(CompressorWEB())

vid.storage()
        
vid.setOverly(Dark())

vid.storage()