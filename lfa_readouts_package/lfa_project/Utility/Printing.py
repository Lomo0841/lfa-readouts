import datetime
import cv2 as cv
import os

#EVERY CLASS IS GIVEN THE SAME PRINTING INSTANCE WHEN INSTANTIATED IN THE MAIN METHOD
class printing():

    def __init__(self):
        self.folder_name = None

    def create_folder(self):
        now = datetime.datetime.now()
        
        folder_name = now.strftime('%Y-%m-%d_%H-%M-%S')
        
        folder_path = os.path.join(os.getcwd(), folder_name)
        
        os.makedirs(folder_path, exist_ok=True)
        
        self.folder_name = folder_path

    def write_to_folder(self, image):
        if self.folder_name is None:
            raise ValueError("Folder not created. Call create_folder() method first.")
        
        now = datetime.datetime.now()

        picture_name = now.strftime("%Y%m%d%H%M%S%f") + ".png"

        img_path = os.path.join(self.folder_name, picture_name)

        cv.imwrite(img_path, image)
        