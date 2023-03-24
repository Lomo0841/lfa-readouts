import datetime
import cv2 as cv
import os

class Printer():

    def __init__(self):
        self.folder_path = None
        self.create_folder()

    def create_folder(self):
        now = datetime.datetime.now()
        
        folder_name = now.strftime('%Y-%m-%d_%H-%M-%S')
        
        folder_path = os.path.join(os.getcwd(), "lfa_readouts_package", "lfa_project", "Results", folder_name)
        
        os.makedirs(folder_path, exist_ok=True)
        
        self.folder_path = folder_path

    def write_image(self, image, name, contours = []):
        
        if len(contours):
            cv.drawContours(image, contours, -1, (0, 255, 0), 3)

        picture_name = name + ".png"

        img_path = os.path.join(self.folder_path, picture_name)

        cv.imwrite(img_path, image)
        
        
    def write_file(self, message):
        
        now = datetime.datetime.now()

        txt_name = now.strftime("%Y%m%d%H%M%S%f") + ".txt"

        txt_path = os.path.join(self.folder_path, txt_name)

        with open(txt_path, "w") as f:
            f.write(message)
    