import tkinter as tk
from tkinter import *

import numpy as np
import win32gui
from keras.models import load_model
from PIL import ImageGrab

model = load_model('mnist.h5')


def predict_digit(img):
    img = img.resize((28, 28))
    img = img.convert('L')
    img = np.array(img)
    img = img.reshape(1, 28, 28, 1)
    img = img/255.0
    result = model.predict([img])[0]
    return np.argmax(result), max(result)


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.x = self.y = 0

        # creating elements of an app window
        self.canvas = tk.Canvas(self, width=300, height=300, bg='white', cursor='cross')
        self.label = tk.Label(self, text='Draw a digit', font=('Helvetica', 48))
        self.classify_button = tk.Button(self, text='Recognise a digit', command=self.classify_handwriting)
        self.clear_button = tk.Button(self, text='Clear', command=self.clear_all)

        # creating grid structure

        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete('all')

    def classify_handwriting(self):
        handler = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(handler) # coordinates of the canvas
        a, b, c, d = rect
        rect = (a+4, b+4, c-4, d-4)
        im = ImageGrab.grab(rect)

        digit, acc = predict_digit(im)
        self.label.configure(text=str(digit) + ', ' + str(int(acc*100)) + "%")

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.create_oval(self.x-r, self.y-r, self.x+r, self.y+r, fill='black')


application = Application()
mainloop()
