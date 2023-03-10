import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk

class ImageView:
    def __init__(self, master):
        # Create GUI elements using Tkinter widgets
        self.select_button = tk.Button(master, text='Select Image', command=self.select_image)
        self.canvas = tk.Canvas(master, width=400, height=400)
        
        # Pack widgets into main window
        self.select_button.pack()
        self.canvas.pack()
        
    def select_image(self):
        # Open file dialog to select image file
        filename = tk.filedialog.askopenfilename()
        # Load image using PIL
        image = Image.open(filename)
        # Resize image to fit in canvas
        image = image.resize((400, 400))
        # Convert image to Tkinter PhotoImage format
        self.photo_image = ImageTk.PhotoImage(image)
        # Display image in canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

if __name__ == '__main__':
    root = tk.Tk()
    view = ImageView(root)
    root.mainloop()
