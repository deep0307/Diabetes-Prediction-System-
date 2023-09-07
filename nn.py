#Contains the neural network.

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dropout


#The format of the fields in the CSV.
FIELD_FORMAT=('Pregnancies','Age','DiabetesPedigreeFunction','BMI','Insulin','Glucose','SkinThickness','BloodPressure')

#The global min-max scaler.
scaler= MinMaxScaler()

def dictToArrayOfArray(dictionary):
	array=[]
	for field in FIELD_FORMAT:
		array.append(dictionary[field])
	return [array]


#Prepare the nn model and return it.
def prepareModel():

	df= pd.read_csv('datasets_228_482_diabetes.csv')
	df=df[df['Insulin']!=0]
	df=df[df['SkinThickness']!=0]
	df=df[df['BloodPressure']!=0]


	X=df[list(FIELD_FORMAT)].values
	y=df['Outcome'].values

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

	X_train= scaler.fit_transform(X_train)
	X_test= scaler.transform(X_test) 

	model= Sequential()
	model.add(Dense(500,activation='relu'))
	model.add(Dropout(0.35))
	model.add(Dense(300,activation='relu'))
	model.add(Dropout(0.35))
	model.add(Dense(1,activation='sigmoid'))
	model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

	stop=EarlyStopping(monitor='val_loss',mode='min',verbose=2,patience=8)

	model.fit(x=X_train,y=y_train,epochs=60,verbose=2,validation_data=(X_test,y_test),callbacks=[stop])

	return model


#Perform the prediction using the nn model and the test data as a dataframe.
def getPrediction(model,testdata):
	#Scale the dataframe.
	testdata=scaler.transform(testdata)
	prediction=float(model.predict(testdata)[0][0])
	return interpretPrediction(prediction)


#Return something to the user depending on what we want.
#Only true/false
#Or the probability of him/her having diabetes.
def interpretPrediction(prediction):
	return prediction
#	return prediction>0.5


#The main function for this file.
def neuralNetwork(data):
	data=dictToArrayOfArray(data)

	model=prepareModel()

	prediction=getPrediction(model,data)

	return prediction


