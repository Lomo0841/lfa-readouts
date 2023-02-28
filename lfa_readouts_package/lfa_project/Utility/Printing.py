import datetime
import cv2 as cv
import os
import platform

#EVERY CLASS IS GIVEN THE SAME PRINTING INSTANCE WHEN INSTANTIATED IN THE MAIN METHOD
class Printing():

    def __init__(self):
        self.folder_path = None
        self.create_folder()

    def create_folder(self):
        now = datetime.datetime.now()
        
        folder_name = now.strftime('%Y-%m-%d_%H-%M-%S')
        
        if platform.system() == 'Windows':
            folder_path = os.path.join(os.getcwd(), "lfa_readouts_package", "lfa_project", "Results", folder_name)
        else:
            folder_path = os.path.join(os.getcwd(), "lfa_project", "Results", folder_name)
        
        os.makedirs(folder_path, exist_ok=True)
        
        self.folder_path = folder_path

    def write_image(self, image):
        if self.folder_path is None:
            raise ValueError("Folder not created. Call create_folder() method first.")
        
        now = datetime.datetime.now()

        picture_name = now.strftime("%Y%m%d%H%M%S%f") + ".png"

        img_path = os.path.join(self.folder_path, picture_name)

        cv.imwrite(img_path, image)
        
    def write_file(self, message):
        if self.folder_path is None:
            raise ValueError("Folder not created. Call create_folder() method first.")
        
        now = datetime.datetime.now()

        txt_name = now.strftime("%Y%m%d%H%M%S%f") + ".txt"

        txt_path = os.path.join(self.folder_path, txt_name)

        with open(txt_path, "w") as f:
            f.write(message)
    