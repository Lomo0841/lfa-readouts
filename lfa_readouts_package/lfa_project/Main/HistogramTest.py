from lfa_project.Implementations.DeepSearch import DeepSearch
from lfa_project.Utility.Printing import Printing
from lfa_project.Implementations.FilterOnConditions import FilterOnConditions
from lfa_project.Utility.ConfigReader import ConfigReader
from lfa_project.Implementations.AprilTagsExtractor import AprilTagsExtractor
from lfa_project.Implementations.HierarchicalSelector import HierarchicalSelector
import cv2 as cv
import itertools

imageName = "rotatedblurry.png"
image = cv.imread("lfa_project/Images/" + imageName)

printer = Printing()
config = ConfigReader()

extractor = AprilTagsExtractor(printer, image)
roi = extractor.extractRois()
roi1 = roi.copy()

deep = DeepSearch(printer, roi)
allContours = deep.detectContours()
flatContours = list(itertools.chain(*allContours))

filter = FilterOnConditions(printer, config, roi, flatContours)
filtered = filter.filterContours()

selector = HierarchicalSelector(printer, roi, filtered)
contour = selector.selectContour()

cv.drawContours(roi1, contour, -1, (0, 255, 0), 3)

cv.imshow(".", roi1)

cv.waitKey(0)

cv.destroyAllWindows
