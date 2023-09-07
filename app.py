#Create the main flask app here.

#Import required functions and classes from the flask library.
from flask import Flask

#template_folder='./html'
#This tells the application trhat all .html files are located in the './html' directory.
app=Flask(__name__,template_folder='./html')

