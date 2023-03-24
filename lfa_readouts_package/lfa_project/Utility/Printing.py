import datetime
import cv2 as cv
import os

class Printing():

    def __init__(self):
        self.folderPath = None
        self.create_folder()

    def create_folder(self):
        now = datetime.datetime.now()
        
        folder_name = now.strftime('%Y-%m-%d_%H-%M-%S')
        
        folderPath = os.path.join(os.getcwd(), "lfa_readouts_package", "lfa_project", "Results", folder_name)
        
        os.makedirs(folderPath, exist_ok=True)
        
        self.folderPath = folderPath

    def write_image(self, image, name, contours = []):
        
        if len(contours):
            cv.drawContours(image, contours, -1, (0, 255, 0), 3)

        pictureName = name + ".png"

        img_path = os.path.join(self.folderPath, pictureName)

        cv.imwrite(img_path, image)
        
        
    def write_file(self, message):
        
        now = datetime.datetime.now()

        txt_name = now.strftime("%Y%m%d%H%M%S%f") + ".txt"

        txt_path = os.path.join(self.folderPath, txt_name)

        with open(txt_path, "w") as f:
            f.write(message)
    