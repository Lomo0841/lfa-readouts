
class Context():

    def _init__(self):
        #Maybe add _ before field names
        self._roiExtractorStrategy = None 
        self._contourDetectorStrategy = None
        self._contourFiltratorStrategy= None
        self._contourSelectorStrategy  = None
        self._resultTranslatorStrategy  = None

    @property
    def roiExtractorStrategy(self):
        return self._roiExtractorStrategy
    
    @property
    def contourDetectorStrategy(self):
        return self._contourDetectorStrategy
    
    @property
    def contourFiltratorStrategy(self):
        return self._contourFiltratorStrategy
    
    @property
    def contourSelectorStrategy(self):
        return self._contourSelectorStrategy
    
    @property
    def resultTranslatorStrategy(self):
        return self._resultTranslatorStrategy
    
    @roiExtractorStrategy.setter
    def roiExtractorStrategy(self, value):
        self._roiExtractorStrategy = value
        
    @contourDetectorStrategy.setter
    def contourDetectorStrategy(self, value):
        self._contourDetectorStrategy = value
    
    @contourFiltratorStrategy.setter
    def contourFiltratorStrategy(self, value):
        self._contourFiltratorStrategy = value
        
    @contourSelectorStrategy.setter
    def contourSelectorStrategy(self, value):
        self._contourSelectorStrategy = value

    @resultTranslatorStrategy.setter
    def resultTranslatorStrategy(self, value):
        self._resultTranslatorStrategy = value

    def executeRoiExtractorStrategy(self):
        return self._roiExtractorStrategy.extractRois()
    
    def executeContourDetectorStrategy(self):
        return self._contourDetectorStrategy.detectContours()
    
    def executeContourFiltratorStrategy(self):
        return self._contourFiltratorStrategy.filterContours()

    def executeContourSelectorStrategy(self):
        return self._contourSelectorStrategy.selectContour()

    def executeResultTranslatorStrategy(self):
        return self._resultTranslatorStrategy.translateResult()