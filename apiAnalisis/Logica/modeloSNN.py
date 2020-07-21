from django.db import models
from django.urls import reverse
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_transformer, ColumnTransformer
from sklearn.pipeline import Pipeline
from tensorflow.python.keras.models import load_model, model_from_json
from keras import backend as K
from apiSNN import models
import os
from tensorflow.python.keras.models import Sequential
import pathlib

class modeloSNN():
    """Clase modelo SNN"""
    
    Selectedmodel = Sequential()
    preprocesador1 = make_column_transformer(
        (StandardScaler(),['Age','Fare']),
        (OneHotEncoder(),['Pclass','Sex','Embarked']))

    def suma(num1=0,num2=0):
        resultado=num1+num2
        return resultado
    def cargarRNN(nombreArchivoModelo,nombreArchivoPesos):
        K.reset_uids()
        # Cargar la Arquitectura desde el archivo JSON
        with open(nombreArchivoModelo+'.json', 'r') as f:
            model = model_from_json(f.read())
        # Cargar Pesos (weights) en el nuevo modelo
        model.load_weights(nombreArchivoPesos+'.h5') 
        print("Red Neuronal Cargada desde Archivo") 
        return model
    def predecirSobrevivencia(self,Pclass=1, Sex='female', Age=60 ,Fare=0, Embarked='C'):
        #Modelo optimizado
        print('MODELO OPTIMIZADO')
        nombreArchivoModelo=r'apiSNN/Logica/arquitectura_optimizada'
        nombreArchivoPesos=r'apiSNN/Logica/pesos_optimizados'
        #return (str(pathlib.Path().absolute())+'\Modelos')
        self.Selectedmodel=self.cargarRNN(nombreArchivoModelo,nombreArchivoPesos) 
        print(self.Selectedmodel)
        print(self.Selectedmodel.summary())
        self.preprocesamiento(self)
        resultado=self.predict(self,Pclass, Sex, Age,Fare, Embarked)
        resultado=resultado[0,0]
        print('Predicción:',resultado)
        #print('Predicción:',self.predict(self,Age=32 ,Fare=9))
        #print('Predicción:',self.predict(self,Pclass=1, Sex='female', Age=60 ,Fare=0, Embarked='C'))
        #print('Predicción:',self.predict(self,Pclass=3, Sex='female', Age=78 ,Fare=4563, Embarked='Q'))
        mensaje=''
        if resultado==1:
            mensaje='Sobrevive'
        else:
            mensaje='No sobrevive'
        return mensaje
    def predict(self,Pclass=1, Sex='female', Age=60 ,Fare=0, Embarked='C'):
        cnames = ['Pclass', 'Sex', 'Age', 'Fare', 'Embarked']
        data = [[Pclass, Sex, Age, Fare, Embarked]]
        my_X = pd.DataFrame(data=data, columns=cnames)
        my_X = self.preprocesador1.transform(my_X)
        Survived = self.Selectedmodel.predict_classes(my_X)
        dbReg=models.Persona(pclass=Pclass, sex=Sex, age=Age ,fare=Fare, embarked=Embarked, survived=Survived)
        dbReg.save()
        return Survived
    def preprocesamiento(self):
        df = pd.read_csv('apiSNN/Datasets/titanic/train.csv')
        df.head()
        df = df.dropna(subset=['Pclass', 'Sex', 'Age', 'Embarked', 'Fare', 'SibSp'])
        df.head()
        Xsubset = df[['Pclass', 'Sex', 'Age', 'Fare', 'Embarked']]
        y = df.Survived.values
        self.preprocesador1.fit_transform(Xsubset)
        
