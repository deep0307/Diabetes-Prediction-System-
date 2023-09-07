#Import flask things.
from flask import render_template
from flask import request
from flask import jsonify
#Import the flask app.
from app import app
#Import default values.
from defaults import *
#Import neural network model.
import nn2 as nn

#The main route to the application.
#Renders the first page of the application.
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/prediction/')
def prediction():
	return render_template('prediction.html')

@app.route('/more/')
def more():
	return render_template('more.html')

@app.route('/insulin/')
def insulin():
	return render_template('insulin.html')

@app.route('/insulin2/')
def insulin2():
	return render_template('insulin2.html')



#The function to run when the application routes to this path.
@app.route('/predict')
def predict():
	#Extract the data.
	data=extractData(request.args)
	#Dummy prediction
	prediction=nn.neuralNetwork(data);
	#The data is returned in key=value form which is referenced at the html page.
	#So the keys for reference(here 'prediction') must be same.
	return jsonify(prediction=prediction)

def extractData(args):
	data={}
	#All data is sent via a GET request.

	#Nonsensical value set as default wherever we expect validation in the browser itself.
	#For all other cases, use the values in the defaults.py file.

	data['Age']=args.get('age',-1,type=int)
	data['Pregnancies']=args.get('pregnancies',PREGNANCIES,type=int)
	data['Glucose']=args.get('glucose',GLUCOSE_LEVEL,type=float)
	data['BloodPressure']=args.get('bp',BLOOD_PRESSURE,type=float)
#	data['SkinThickness']=args.get('skin',SKIN_THICKNESS,type=float)
	data['Insulin']=args.get('insulin',INSULIN_LEVEL,type=float)
	data['BMI']=args.get('bmi',BMI,type=float)
	data['DiabetesPedigreeFunction']=args.get('dpf',DIABETES_PEDIGREE_FUNCTION,type=float)

	return data


#Run the application in debug mode.
app.run(debug=True)

