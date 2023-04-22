class Context():

    def __init__(self):
        self._roi_extractor_strategy = None 
        self._contour_detector_strategy = None
        self._contour_filtrator_strategy = None
        self._contour_selector_strategy = None
        self._white_balancing_strategy = None

    @property
    def roi_extractor_strategy(self):
        return self._roi_extractor_strategy
    
    @property
    def contour_detector_strategy(self):
        return self._contour_detector_strategy
    
    @property
    def contour_filtrator_strategy(self):
        return self._contour_filtrator_strategy
    
    @property
    def contour_selector_strategy(self):
        return self._contour_selector_strategy
    
    @property
    def white_balancing_strategy(self):
        return self._white_balancing_strategy
    
    @roi_extractor_strategy.setter
    def roi_extractor_strategy(self, value):
        self._roi_extractor_strategy = value
        
    @contour_detector_strategy.setter
    def contour_detector_strategy(self, value):
        self._contour_detector_strategy = value
    
    @contour_filtrator_strategy.setter
    def contour_filtrator_strategy(self, value):
        self._contour_filtrator_strategy = value
        
    @contour_selector_strategy.setter
    def contour_selector_strategy(self, value):
        self._contour_selector_strategy = value

    @white_balancing_strategy.setter
    def white_balancing_strategy(self, value):
        self._white_balancing_strategy = value

    def execute_roi_extractor_strategy(self):
        return self._roi_extractor_strategy.extract_roi()
    
    def execute_contour_detector_strategy(self):
        return self._contour_detector_strategy.detect_contours()
    
    def execute_contour_filtrator_strategy(self):
        return self._contour_filtrator_strategy.filter_contours()

    def execute_contour_selector_strategy(self):
        return self._contour_selector_strategy.select_contour()

    def execute_white_balancing_strategy(self):
        return self._white_balancing_strategy.white_balance()
