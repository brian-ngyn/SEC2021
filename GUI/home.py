from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import csv


import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("./sec2021-4362e-firebase-adminsdk-w43kk-00e523d365.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'sec2021-4362e.appspot.com'
})

bucket = storage.bucket()

root = Tk()
root.title("Prediction Expert")
width = 600
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x= (screen_width/2) - (width/2)
y= (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0,0)

def addCSV():

    filename = fd.askopenfilename(
        title="Add .csv File",
        initialdir='/')

    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)


myLabel1 = Label(root, text="Prediction Expert").grid(row=0, column=2)
myLabel2 = Label(root, text="                                                          ").grid(row=2, column=1)
myLabel3 = Label(root, text="                                    ").grid(row=3, column=3)
myFileButton = Button(root, text="Add .csv File", padx=20, pady=15, command=addCSV, fg="green", bg="black").grid(row=4, column=2)



if __name__ == '__main__':
    root.mainloop() 