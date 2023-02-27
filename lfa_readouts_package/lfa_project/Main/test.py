import cv2
import numpy as np
import pupil_apriltags as apriltag

# Load the image
img = cv2.imread("lfa_project/Images/test.png")

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Initialize the AprilTag detector with the "tag36h11" family
detector = apriltag.Detector(families='tag36h11')

# Detect all the tags in the image
detections = detector.detect(gray)

# Make sure we detected all 4 tags
if len(detections) == 4:
    # Get the corners of each tag and their IDs
    tag_corners = {}
    for detection in detections:
        tag_corners[detection.tag_id] = detection.corners.reshape((4, 2))
    
    # Get the 3D coordinates of each tag
    tag_size = 0.03 # Assuming all tags are of the same size (in meters)
    tag0_3d = np.array([[0, 0, 0], [tag_size, 0, 0], [tag_size, tag_size, 0], [0, tag_size, 0]], dtype=np.float32)
    tag1_3d = np.array([[0, 0, 0], [tag_size, 0, 0], [tag_size, tag_size, 0], [0, tag_size, 0]], dtype=np.float32)
    tag2_3d = np.array([[0, 0, 0], [tag_size, 0, 0], [tag_size, tag_size, 0], [0, tag_size, 0]], dtype=np.float32)
    tag3_3d = np.array([[0, 0, 0], [tag_size, 0, 0], [tag_size, tag_size, 0], [0, tag_size, 0]], dtype=np.float32)
    tag_3d = [tag0_3d, tag1_3d, tag2_3d, tag3_3d]
    
    # Calculate the homography matrix for each tag
    homography_matrices = []
    for i in range(4):
        tag_id = i
        tag_2d = tag_corners[tag_id]
        homography_matrix, _ = cv2.findHomography(tag_2d, tag_3d[tag_id])
        homography_matrices.append(homography_matrix)
    
    # Combine the homography matrices into one
    H = np.linalg.inv(homography_matrices[0]) @ homography_matrices[1] @ np.linalg.inv(homography_matrices[2]) @ homography_matrices[3]
    
    # Warp the image using the homography matrix
    height, width = img.shape[:2]
    dewarped_img = cv2.warpPerspective(img, H, (width, height))
    
    # Show the dewarped image
    cv2.imshow('Dewarped Image', dewarped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
else:
    print("Did not detect all 4 tags.")