from django.db import models
from django.urls import reverse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder
from sklearn.compose import make_column_transformer, ColumnTransformer
import seaborn as sns
from sklearn import preprocessing
from apiAnalisis import models
import os
import pathlib
import math
import operator
import csv

class modeloAnalisis():
    """Clase modelo Analisis"""
    dfOriginal=pd.DataFrame([])
    DataframeTransformado1=pd.DataFrame([])
    def suma(num1=0,num2=0):
        resultado=num1+num2
        return resultado

    def similarity(cn=[],ce=[]):
        sct=0
        sca=0
        scb=0
        for i in range(len(ce)):
            sct+=float(cn[i])*float(ce[i])
            sca+=math.pow(float(ce[i]),2)
            scb+=math.pow(float(cn[i]),2)
        sc=sct/(math.sqrt(sca)*math.sqrt(scb))
        return sc

    def calculoSimilitud(self,Dni=0):
        cliente=self.dfOriginal.loc[self.dfOriginal['DNI'] == Dni]
        indice=cliente.index.values[0]
        df = pd.read_csv('apiAnalisis/Datasets/DatasetBanco/5.DatasetBancoTransformadoMinMax.csv')
        clientes = [list(row) for row in df.values]
        cn=clientes[indice][0].split(";")
        similares={}
        for i in range(len(clientes)):
            fila=[]
            fila=clientes[i][0].split(";")
            if fila[len(fila)-1] != str(0):
                tipo=fila[len(fila)-1]
                x = self.similarity(cn,fila)
                similares.update({str(i):[round(x,5),int(tipo)]})
        return similares

    def crearGrafica(self):
        etiquetas=["Buenos Clientes","Malos Clientes"]
        lec = pd.read_csv("apiAnalisis/Datasets/DatasetBanco/3.DatasetBanco.csv")
        clientes = lec.values.tolist()
        cont=0
        cont2=0
        for i in clientes:
            lista = i[0].split(";")
            if lista[17]==str(1):
                cont=cont+1
            elif lista[17]==str(2):
                cont2=cont2+1
        porcentajes=[str(cont),str(cont2)]
        #plt.pie(porcentajes,labels=etiquetas,startangle=90,explode=(0.1,0.1),radius=1.2,autopct="%1.2f%%")
        #plt.title("Gráfica Clientes")
        #plt.savefig("pie.jpg")
        #path = os.path.realpath("pie.jpg")
        return porcentajes

    def predecirTipoCliente(self,Dni=0):
        print('Dni:',Dni)
        self.preprocesamiento(self)
        tipoCliente, edad=self.predecir(self,Dni)
        #print(tipoCliente)
        if tipoCliente==1:
            mensaje=1
            dbReg=models.Cliente(cedula=Dni, edad=edad, tipoCliente=tipoCliente)
            dbReg.save()
        elif tipoCliente==2:
            mensaje=2
            dbReg=models.Cliente(cedula=Dni, edad=edad, tipoCliente=tipoCliente)
            dbReg.save()
        else:
            mensaje='No existe el cliente con Dni:',Dni
        return mensaje

    def predecir(self,Dni=0):
        cliente=self.dfOriginal.loc[self.dfOriginal['DNI'] == Dni]
        print('LLego cliente: ',cliente)
        tipoCliente=2
        edad=0
        if not cliente.empty:
            print('Existe el cliente')
            indiceCliente=cliente.index.values[0]
            edad=cliente['EDAD'].values
            edad=edad[0]
            cliente=self.DataframeTransformado1.loc[ indiceCliente , : ]
            calculos=self.calculoSimilitud(self,Dni)
            ordenados = dict(sorted(calculos.items(), key=operator.itemgetter(1),reverse=True))
            ind=list(ordenados)[0]
            cont=0
            cont2=0
            for i in range(10):
                res1= list(ordenados)[i]
                ar=ordenados[res1]
                if ar[1]==1:
                    cont=cont+1
                else:
                    cont2=cont2+1
            print("# 1: ",cont, " , #2: ",cont2)
            if cont>cont2 or cont==cont2:
                tipoCliente=1
            elif cont2>cont:
                tipoCliente=2
            self.dfOriginal.at[indiceCliente,'TIPOCLIENTE']=tipoCliente
            self.dfOriginal.to_csv("apiAnalisis/Datasets/DatasetBanco/3.DatasetBanco.csv",sep=";", index=False)
        else:
            tipoCliente=3
        return tipoCliente, edad

    def preprocesamiento(self):
        self.dfOriginal = pd.read_csv('apiAnalisis/Datasets/DatasetBanco/3.DatasetBanco.csv', sep=";")
        dataframe=self.dfOriginal
        #print(dataframe.shape)
        salida = self.dfOriginal.TIPOCLIENTE.values
        dataframe=dataframe.drop(['DNI'], axis=1)
        dataframe=dataframe.drop(['TIPOCLIENTE'], axis=1)
        #print(dataframe.shape)

        categorical_ordinal = ['HISTORIALCREDITO','SALDOCUENTAAHORROS','TIEMPOEMPLEO','ESTADOCIVILYSEXO','ACTIVOS','VIVIENDA','EMPLEO']
        categorical_nominal = ['PROPOSITOCREDITO','GARANTE','TRABAJADOREXTRANJERO']
        numerical = ['PLAZOMESESCREDITO','MONTOCREDITO','TASAPAGO','AVALUOVIVIENDA','EDAD','CANTIDADCREDITOSEXISTENTES']
        preprocesador1 = make_column_transformer(
            (OrdinalEncoder(),categorical_ordinal),
            (OneHotEncoder(sparse=False),categorical_nominal),
            remainder='passthrough'
            )

        X = preprocesador1.fit_transform(dataframe)
        #print(X.shape[1])
        #print(X.shape)

        np.set_printoptions(formatter={'float': lambda X: "{0:0.0f}".format(X)})
        #print(preprocesador1)
        cnamesDataset1 = categorical_ordinal
        cnamesDataset2 = preprocesador1.transformers_[1][1].get_feature_names(categorical_nominal)
        cnamesDataset3 = numerical
        cnamesDataset1.extend(cnamesDataset2)
        cnamesDataset1.extend(cnamesDataset3)
        #print(cnamesDataset1)

        DataframePreprocesado = pd.DataFrame(data=X,columns=cnamesDataset1)
        DataframePreprocesado = pd.concat([DataframePreprocesado, self.dfOriginal[['TIPOCLIENTE']]], axis = 1)
        DataframePreprocesado.to_csv("apiAnalisis/Datasets/DatasetBanco/4.DatasetBancoPreprocesado.csv", sep=";",index = False) #sep es el separador, por defector es ","
        
        cr=DataframePreprocesado.corr()
        cr=round(cr,3)
        #print(cr)

        # Min max scaling
        DataframePreprocesado=DataframePreprocesado.drop(['TIPOCLIENTE'], axis=1)
        data_scaler_minmax = preprocessing.MinMaxScaler(feature_range=(0, 1))
        data_scaled_minmax = data_scaler_minmax.fit_transform(DataframePreprocesado)
        #print("\nDatos normalizados con escala Min Max:\n", data_scaled_minmax)

        self.DataframeTransformado1 = pd.DataFrame(data=data_scaled_minmax,columns=cnamesDataset1)
        self.DataframeTransformado1 = pd.concat([self.DataframeTransformado1, self.dfOriginal[['TIPOCLIENTE']]], axis = 1)
        self.DataframeTransformado1.to_csv("apiAnalisis/Datasets/DatasetBanco/5.DatasetBancoTransformadoMinMax.csv", sep=";",index = False) #sep es el separado, por defector es ","
        return "listo"

