#Contains the neural network.

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import model_from_json
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.callbacks import EarlyStopping
#For ANOVA
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import f_classif, f_regression
from sklearn.feature_selection import SelectKBest, SelectPercentile



#The format of the fields in the CSV.
FIELD_FORMAT=('Pregnancies','BMI','Insulin','Glucose','Age','BloodPressure','DiabetesPedigreeFunction')
#FIELD_FORMAT=('Pregnancies','Age','DiabetesPedigreeFunction','BMI','Insulin','Glucose','SkinThickness','BloodPressure')

#The global min-max scaler.
scaler= MinMaxScaler()

def dictToArrayOfArray(dictionary):
	array=[]
	for field in FIELD_FORMAT:
		array.append(dictionary[field])
	return [array]

#Prepares the dataset.
#Replaces the means.
#Preprocessing.(EDA)
def prepareDataset():

	df= pd.read_csv('diabetes.csv')

	df1=df[df['Outcome']==0]
	df2=df[df['Outcome']==1]

	df1=df1[df1['Insulin']!=0]
	df1=df1[df1['SkinThickness']!=0]
	df1=df1[df1['BloodPressure']!=0]

	df2=df2[df2['Insulin']!=0]
	df2=df2[df2['SkinThickness']!=0]
	df2=df2[df2['BloodPressure']!=0]

	mean1=df1['BloodPressure'].mean()
	mean2=df1['SkinThickness'].mean()
	mean3=df1['Insulin'].mean()
	mean4=df2['BloodPressure'].mean()
	mean5=df2['SkinThickness'].mean()
	mean6=df2['Insulin'].mean()

	df= pd.read_csv('diabetes.csv')
	df1=df[df['Outcome']==0]
	df2=df[df['Outcome']==1]

	df1['BloodPressure']=df1['BloodPressure'].replace(0,mean1)
	df1['SkinThickness']=df1['SkinThickness'].replace(0,mean2)
	df1['Insulin']=df1['Insulin'].replace(0,mean3)
	df2['BloodPressure']=df2['BloodPressure'].replace(0,mean4)
	df2['SkinThickness']=df2['SkinThickness'].replace(0,mean5)
	df2['Insulin']=df2['Insulin'].replace(0,mean6)

	frames=[df1,df2]

	df=pd.concat(frames)
	df.sample(frac=1)

	return df

def anova(X_train,X_test,y_train):
	#remove constant and quasi constant features
	constant_filter = VarianceThreshold(threshold=0.01)
	constant_filter.fit(X_train)
	X_train_filter = constant_filter.transform(X_train)
	X_test_filter = constant_filter.transform(X_test)

	#remove duplicate features
	X_train_T = X_train_filter.T
	X_test_T = X_test_filter.T

	X_train_T = pd.DataFrame(X_train_T)
	X_test_T = pd.DataFrame(X_test_T)

	duplicated_features = X_train_T.duplicated()

	features_to_keep = [not index for index in duplicated_features]

	X_train_unique = X_train_T[features_to_keep].T
	X_test_unique = X_test_T[features_to_keep].T

	sel = f_classif(X_train_unique,y_train)

	p_values = pd.Series(sel[1])
	p_values.index = X_train_unique.columns
	p_values.sort_values(ascending = True, inplace = True)

	p_values = p_values[p_values<0.05]

	X_train_p = X_train_unique[p_values.index]
	X_test_p = X_test_unique[p_values.index]

	return (X_train_p,X_test_p)

def getNN():

	'''
	model= Sequential()
	model.add(Dense(500,activation='relu'))
	model.add(Dropout(0.35))
	model.add(Dense(100,activation='relu'))
	model.add(Dropout(0.35))
	model.add(Dense(1,activation='sigmoid'))
	model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
	'''
	json_file=open('model.json','r')
	loaded_model_json=json_file.read()
	json_file.close()
	model=model_from_json(loaded_model_json)
	# load weights into new model
	model.load_weights("model.h5")
	return model



#Prepare the nn model and return it.
def prepareModel(df):

	X=df[['Pregnancies','BMI','Insulin','Glucose','SkinThickness','Age','BloodPressure','DiabetesPedigreeFunction']].values
	y=df['Outcome'].values

	X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)

	X_train=scaler.fit_transform(X_train)
	X_test=scaler.transform(X_test) 

	#ANOVAfy everything
	X_train,X_test=anova(X_train,X_test,y_train)

	model=getNN()

	model.fit(x=X_train,y=y_train,epochs=400,verbose=1)

	return model

#Perform the prediction using the nn model and the test data as a dataframe.
def getPrediction(model,df,testdata):
	#Scale the dataframe.

	X=df[['Pregnancies','BMI','Insulin','Glucose','Age','BloodPressure','DiabetesPedigreeFunction']].values
	y=df['Outcome'].values

	X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)

	X_train=scaler.fit_transform(X_train)


	testdata=scaler.transform(testdata)
	prediction=float(model.predict(testdata)[0][0])
	return interpretPrediction(prediction)


#Return something to the user depending on what we want.
#Only true/false
#Or the probability of him/her having diabetes.
def interpretPrediction(prediction):
	print(prediction,prediction>=0.5)
	return prediction
#	return prediction>=0.5


#The main function for this file.
def neuralNetwork(data):

	print(data,'\n'*5)

	data=dictToArrayOfArray(data)

	dataset=prepareDataset()
#	model=prepareModel(dataset)

	model=getNN()

	prediction=getPrediction(model,dataset,data)

	return interpretPrediction(prediction)


