#!/usr/bin/env python
# coding: utf-8

# ![image.png](attachment:image.png)

# # ANÁLISIS DE DATOS

# El análisis de datos es un proceso de inspección, limpieza, transformación y modelado de datos con el objetivo de descubrir información útil, informar conclusiones y respaldar la toma de decisiones. 
# 
# El análisis de datos tiene múltiples facetas y enfoques, que abarcan diversas técnicas bajo una variedad de nombres como minería de datos, business intelligence, aprendizaje automático, análisis del bigdata, etc.
# 
# El análisis de datos es la piedra angular en diferentes dominios de negocios, ciencias y ciencias sociales.

# ![EstructuraDataset.png](Imagenes/EstructuraDataset.png)

# ### Tipo de Variable
# 
# 
# **1. Categóricas:** Las variables categóricas tienen valores que describen una «cualidad» o «característica» de una unidad de datos, como «qué tipo» o «qué categoría». Por lo tanto, las variables categóricas son variables cualitativas y tienden a estar representadas por un valor no numérico.
# 
# **Nominales:** estas son variables compuestas por dos o más categorías cuyo valor se asigna basado en la identidad del objeto. Algunos ejemplos son sexo, color de ojos o tipo de animal.
# 
# **Ordinales:** estas son variables compuestas por dos o más categorías en las que el orden es importante en el valor. Algunos ejemplos son el rango de clases de los estudiantes o las escalas de las encuestas de satisfacción (insatisfecho, neutro, satisfecho).
# 
# **2. Numéricas:** Las variables numéricas tienen valores que describen una cantidad medible como un número. Responden a preguntas del tipo «cuánto» o «cuántos». Por lo tanto, las variables numéricas son variables cuantitativas.
# 
# **Continuas:** estas son variables que son cuantitativas y pueden medirse a lo largo de una secuencia o un rango de valores. Existen dos tipos de variables continuas; las variables de intervalo puede tener cualquier valor dentro del rango de valores. Algunos ejemplos son temperatura o tiempo. Las variables de relaciones son las variables de intervalo especiales donde un valor de cero (0) significa que no hay ninguna variable. Entre los ejemplos se incluyen ingresos o el volumen de ventas.
# 
# **Discretas:** estos tipos de variables continuas son cuantitativos pero tienen un valor específico de un conjunto de valores finito. Los ejemplos incluyen el número de sensores habilitados en una red, o el número de automóviles en un estacionamiento.

# ![TiposVariables.png](Imagenes/TiposVariables.png)

# ## 1. Importar Librerías

# In[2]:


# importar libreria para cargar y analizar datos del dataset
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt 
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder
from sklearn.compose import make_column_transformer, ColumnTransformer
import seaborn as sns


# ## 2. Cargar Dataset
# 

# Numero de Variables (o atributos): 17
# 
# **Variables:**
# 
# 1. DNI (No aporta al análisis)
# 2. PLAZOMESESCREDITO             (Variable Numérica - Discreta)
# 3. HISTORIALCREDITO                                                                             (Variable Categórica - Ordinal)
# 4. PROPOSITOCREDITO                                             (Variable Categórica - Nominal)
# 5. MONTOCREDITO                  (Variable Numérica - Continua)
# 6. SALDOCUENTAAHORROS                                                                           (Variable Categórica - Ordinal)
# 7. TIEMPOEMPLEO                                                                                 (Variable Categórica - Ordinal)
# 8. TASAPAGO                      (Variable Numérica - Continua)
# 9. ESTADOCIVILYSEXO                                                                             (Variable Categórica - Ordinal)
# 10. GARANTE                                                     (Variable Categórica - Nominal)
# 11. AVALUOVIVIENDA               (Variable Numérica - Continua)
# 12. ACTIVOS                                                                                     (Variable Categórica - Ordinal)
# 13. EDAD                         (Variable Numérica - Discreta)
# 14. VIVIENDA                                                                                    (Variable Categórica - Ordinal)
# 15. CANTIDADCREDITOSEXISTENTES   (Variable Numérica - Discreta)
# 16. EMPLEO                                                                                      (Variable Categórica - Ordinal)
# 17. TRABAJADOREXTRANJERO                                        (Variable Categórica - Nominal)
# 
# **Salida:**
# 
# TIPOCLIENTE (BUENO:1, MALO:2)                                   (Variable Categórica - Nominal)

# In[70]:


import pandas as pd
dataset = "3.DatasetBanco.csv"
#Cargar el dataset en la variable df.
dfOriginal = pd.read_csv(dataset, sep=";")
dataframe=dfOriginal
dataframe.head()


# In[71]:


salida = dfOriginal.TIPOCLIENTE.values

print(dataframe.shape)
dataframe=dataframe.drop(['DNI'], axis=1)
dataframe=dataframe.drop(['TIPOCLIENTE'], axis=1)
print(dataframe.shape)
dataframe.head()


# ## 3. Realizar preprocesamiento
# 
# **Documentación ColumnTransformer:**
# https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html

# In[72]:


categorical_ordinal = ['HISTORIALCREDITO','SALDOCUENTAAHORROS','TIEMPOEMPLEO','ESTADOCIVILYSEXO','ACTIVOS','VIVIENDA','EMPLEO']
categorical_nominal = ['PROPOSITOCREDITO','GARANTE','TRABAJADOREXTRANJERO']
numerical = ['PLAZOMESESCREDITO','MONTOCREDITO','TASAPAGO','AVALUOVIVIENDA','EDAD','CANTIDADCREDITOSEXISTENTES']
preprocesador1 = make_column_transformer(
    (OrdinalEncoder(),categorical_ordinal),
    (OneHotEncoder(sparse=False),categorical_nominal),
    remainder='passthrough'
    )

X = preprocesador1.fit_transform(dataframe)
print(X.shape[1])
print(X.shape)

print(salida.shape)
#X=np.append(X, salida, axis=1)

np.set_printoptions(formatter={'float': lambda X: "{0:0.0f}".format(X)})

#print(preprocesador1)

cnamesDataset1 = categorical_ordinal
cnamesDataset2 = preprocesador1.transformers_[1][1].get_feature_names(categorical_nominal)
cnamesDataset3 = numerical
#print(cnamesDataset2)

cnamesDataset1.extend(cnamesDataset2)
cnamesDataset1.extend(cnamesDataset3)
print(cnamesDataset1)

DataframePreprocesado = pd.DataFrame(data=X,columns=cnamesDataset1)
DataframePreprocesado = pd.concat([DataframePreprocesado, dfOriginal[['TIPOCLIENTE']]], axis = 1)
DataframePreprocesado.to_csv("4.DatasetBancoPreprocesado.csv", sep=";",index = False) #sep es el separado, por defector es ","
DataframePreprocesado.head()


# ## 4. Realizar Análisis Descriptivo

# In[87]:


#Análisis de correlaciones entre variables
cr=DataframePreprocesado.corr()
plt.figure(figsize=(13, 13))
ax = sns.heatmap(cr)
plt.savefig('attribute_correlations.png', tight_layout=True)


# In[74]:


cr=round(cr,3)
cr


# In[75]:


#Análisis descriptivo
DataframePreprocesado.describe() 


# In[91]:


#Visualización para análisis
variableAnálisis='MONTOCREDITO'
variableSalida='TASAPAGO'
DataframePreprocesado.plot(x=variableAnálisis, y=variableSalida, style='o')  
plt.title('Análisis Correlación')  
plt.xlabel(variableAnálisis)  
plt.ylabel(variableSalida)  
plt.show() 


# ## 5. Realizar Transformación

# In[77]:


from sklearn import preprocessing

# Min max scaling
DataframePreprocesado=DataframePreprocesado.drop(['TIPOCLIENTE'], axis=1)
data_scaler_minmax = preprocessing.MinMaxScaler(feature_range=(0, 1))
data_scaled_minmax = data_scaler_minmax.fit_transform(DataframePreprocesado)
print("\nDatos normalizados con escala Min Max:\n", data_scaled_minmax)

DataframeTransformado1 = pd.DataFrame(data=data_scaled_minmax,columns=cnamesDataset1)
DataframeTransformado1 = pd.concat([DataframeTransformado1, dfOriginal[['TIPOCLIENTE']]], axis = 1)
DataframeTransformado1.to_csv("5.DatasetBancoTransformadoMinMax.csv", sep=";",index = False) #sep es el separado, por defector es ","
DataframeTransformado1.head()


# In[78]:


# Normalize data
data_normalized_l1 = preprocessing.normalize(DataframePreprocesado, norm='l1')
data_normalized_l2 = preprocessing.normalize(DataframePreprocesado, norm='l2')
print("\nDatos normalizados con L1:\n", data_normalized_l1)
print("\nDatos normalizados con L2:\n", data_normalized_l2)

DataframeTransformado2 = pd.DataFrame(data=data_normalized_l1,columns=cnamesDataset1)
DataframeTransformado2 = pd.concat([DataframeTransformado2, dfOriginal[['TIPOCLIENTE']]], axis = 1)
DataframeTransformado2.to_csv("6.DatasetBancoTransformadoNormL1.csv", sep=";",index = False) #sep es el separado, por defector es ","
DataframeTransformado2.head()

DataframeTransformado3 = pd.DataFrame(data=data_normalized_l2,columns=cnamesDataset1)
DataframeTransformado3 = pd.concat([DataframeTransformado3, dfOriginal[['TIPOCLIENTE']]], axis = 1)
DataframeTransformado3.to_csv("7.DatasetBancoTransformadoNormL2.csv", sep=";",index = False) #sep es el separado, por defector es ","
DataframeTransformado3.head()


# In[79]:


# Estandarización: media en 0
XEstandarizado = preprocessing.scale(DataframePreprocesado)
print("\nDatos estandarizados:\n", XEstandarizado)

DataframeTransformado4 = pd.DataFrame(data=XEstandarizado,columns=cnamesDataset1)
DataframeTransformado4 = pd.concat([DataframeTransformado4, dfOriginal[['TIPOCLIENTE']]], axis = 1)
DataframeTransformado4.to_csv("8.DatasetBancoTransformadoScale.csv", sep=";",index = False) #sep es el separado, por defector es ","
DataframeTransformado4.head()


# In[88]:


#Análisis de correlaciones entre variables
cr=DataframeTransformado2.corr()
plt.figure(figsize=(13, 13))
ax = sns.heatmap(cr)
plt.savefig('attribute_correlations.png', tight_layout=True)


# In[81]:


cr=round(cr,3)
cr


# In[92]:


#Visualización para analisis manual
variableAnálisis='MONTOCREDITO'
variableSalida='TASAPAGO'
DataframeTransformado4.plot(x=variableAnálisis, y=variableSalida, style='o')  
plt.title('Análisis Correlación')  
plt.xlabel(variableAnálisis)  
plt.ylabel(variableSalida)  
plt.show() 


# In[ ]:





# In[ ]:




