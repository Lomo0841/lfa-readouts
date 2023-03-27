
class Context():

    def _init__(self):
        #Maybe add _ before field names
        self._roiExtractorStrategy = None 
        self._contourDetectorStrategy = None
        self._contourFiltratorStrategy= None
        self._contourSelectorStrategy  = None
        self._resultTranslatorStrategy  = None
        self._whiteBalancingStrategy = None

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
    
    @property
    def whiteBalancingStrategy(self):
        return self._whiteBalancingStrategy
    
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

    @whiteBalancingStrategy.setter
    def whiteBalancingStrategy(self, value):
        self._whiteBalancingStrategy = value

    def executeRoiExtractorStrategy(self):
        return self._roiExtractorStrategy.extract_rois()
    
    def executeContourDetectorStrategy(self):
        return self._contourDetectorStrategy.detect_contours()
    
    def executeContourFiltratorStrategy(self):
        return self._contourFiltratorStrategy.filter_contours()

    def executeContourSelectorStrategy(self):
        return self._contourSelectorStrategy.select_contour()

    def executeResultTranslatorStrategy(self):
        return self._resultTranslatorStrategy.translate_result()
    
    def executeWhiteBalancingStrategy(self):
        return self._whiteBalancingStrategy.white_balance()
    