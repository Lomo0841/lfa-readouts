import cv2 as cv
import numpy as np

def maxrgb_white_balance(img):
    b, g, r = cv.split(img)
    maxVals = np.maximum(np.maximum(r, g), b)

    rNorm = r / maxVals
    gNorm = g / maxVals
    bNorm = b / maxVals

    balancedImg = cv.merge((bNorm, gNorm, rNorm))

    balancedImgCorrected = cv.convertScaleAbs(balancedImg * 255)

    return balancedImgCorrected

if __name__ == '__main__':
    # Load the image
    img = cv.imread("lfa_readouts_package/lfa_project/Images/TwoLeds/Roi.png")

    # Perform white balancing using the MaxRGB algorithm
    balanced_img = maxrgb_white_balance(img)

    # Convert the balanced image to an 8-bit depth image

    # Convert the 8-bit depth image to grayscale
    greyScale = cv.cvtColor(balanced_img, cv.COLOR_BGR2GRAY)
    greyScaleOr = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Apply thresholding
    ret, thresholdedImage = cv.threshold(greyScale, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    ret, thresholdedImageOr = cv.threshold(greyScaleOr, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # Display the original and balanced images
    cv.imshow('threshold', thresholdedImage)
    cv.imshow('thresholdor', thresholdedImageOr)
    cv.imshow('Original Image', img)
    cv.imshow('Balanced Image', balanced_img)
    cv.waitKey(0)
    cv.destroyAllWindows()
