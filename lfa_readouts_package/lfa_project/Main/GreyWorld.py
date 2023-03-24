import cv2 as cv

img = cv.imread("lfa_readouts_package/lfa_project/Images/TwoLeds/green.png")

lab_img = cv.cvtColor(img, cv.COLOR_BGR2LAB)

l_mean, a_mean, b_mean, _ = cv.mean(lab_img)

l_scale = 128 / l_mean
a_scale = 128 / a_mean
b_scale = 128 / b_mean

lab_img[:, :, 0] = cv.multiply(lab_img[:, :, 0], l_scale)
lab_img[:, :, 1] = cv.multiply(lab_img[:, :, 1], a_scale)
lab_img[:, :, 2] = cv.multiply(lab_img[:, :, 2], b_scale)

balanced_img = cv.cvtColor(lab_img, cv.COLOR_LAB2BGR)

greyScale = cv.cvtColor(balanced_img, cv.COLOR_BGR2GRAY)

ret, thresholdedImage = cv.threshold(greyScale, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

# Display the original and balanced images side by side
cv.imshow('thresh', thresholdedImage)
cv.imshow('Original', img)
cv.imshow('Balanced', balanced_img)
cv.waitKey(0)
cv.destroyAllWindows()
