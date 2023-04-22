import datetime
import cv2 as cv
import os

class Printer():

    def __init__(self, config):
        self.folder_path = None
        self.do_print = config.get_config_boolean("Print", "print")
        self.create_folder_and_file()

    def create_folder_and_file(self):
        if self.do_print:

            now = datetime.datetime.now()
            
            folder_name = now.strftime('%Y-%m-%d_%H-%M-%S')
            folder_path = os.path.join(os.getcwd(), "lfa_readouts_package", "lfa_project", "Results", folder_name)

            txt_name = now.strftime("%Y%m%d%H%M%S%f") + ".txt"
            txt_path = os.path.join(folder_path, txt_name)
            
            os.makedirs(folder_path, exist_ok=True)
            
            self.folder_path = folder_path
            self.txt_path = txt_path

    def write_image(self, image, name, contours = []):
        if self.do_print:
            if len(contours):
                cv.drawContours(image, contours, -1, (0, 255, 0), 3)

            picture_name = name + ".png"

            img_path = os.path.join(self.folder_path, picture_name)

            cv.imwrite(img_path, image)
        
    def write_file(self, message):
        if self.do_print:
            with open(self.txt_path, "a") as f:
                f.write(message + "\n \n")
    