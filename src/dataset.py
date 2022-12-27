# -*- coding: utf-8 -*-
"""
Preprocesado del dataset en bruto de la UCI para adaptarlo a
las necesidades del proyecto.

Author:   Carlos Anivarro Batiste
Author:   Daniel Barahona Martin
Author:   Daniel Cerrato Sanchez
Author:   David Garitagoitia Romero
"""
import numpy as np
import pandas as pd


META_F = "./data/HT_Sensor_metadata.dat"
DATA_F = "./data/HT_Sensor_dataset.dat"
FEATURES_ORIGINAL = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'Temp.', 'Humidity']


class Dataset():
  """
  Clase usada para encapsular el dataset
  
  Atributos:
    df: Dataframe de Pandas con los datos separados por atributos
  """

  
  def __init__(self, md_fn, d_fn):
    """
    
    Args:
      md_fn: Ruta del fichero de metadatos
      d_fn: Ruta del fichero de dataset
    """
    self.meta_f = md_fn
    self.data_f = d_fn
    self.df = self.build_dataframe()
    
  
  def join_metadata_dataset(self):
    """
    Une los metadatos con la BD principal de las series usando el campo
    'id' para el join
    """
    
    df_meta = pd.read_csv(self.meta_f, delimiter=',+', engine='python')
    df_data = pd.read_csv(self.data_f, delimiter=',+', engine='python')
    
    df_data.set_index('id', inplace=True)
    # Hacer un inner join de metadatos con series
    df_data.join(df_meta, how='inner')
    
    # Recalcular time (para que no haya tiempos negativos)
    df_data['time'] += df_data['t0']
    
    df_data.set_index(np.arange(df_data.shape[0]), inplace=True)
    
    return df_data
    
   
  def build_dataframe(self):
    """
    Construye un dataset con atributos al uso para poder
    ejecutar experimentos de ML
    
    IDEAS DE ATRIBUTOS:
      - Media y mediana de los ultimos X mins
      - Desviación de los ultimos X mins
      - Umbral de desviación para ver si es vino o cambio de pendiente
      - Numero de muestras del intervalo de los últimos X minutos
      - Lo de las 5 “sigmas”

      'X' debería ser no muy grande: si queremos hacer datos en tiempo real,
      poner una ventana pequeña, por ejemplo 5 minutos.
    
    Return:
      Un Dataframe de pandas con el dataset
    """
    join_df = self.join_metadata_dataset()
    
    # TODO construir dataset con atributos elegidos
    
    return join_df
    
    
  def train_test_split(self, frac_test, attrs=FEATURES_ORIGINAL):
    """
    Divide un dataset en subconjuntos de entrenamiento y validacion
    
    Args:
      frac_test: Porcentaje (sobre 100) de muestras para validacion
      attrs: Lista de atributos para datos (SIN clase)
      
    Return:
      X_train:  dataframe con datos de entrenamiento
      y_train:  dataframe con clases de entrenamiento
      X_test:   dataframe con datos de validacion
      y_test:   dataframe con clases de validacion
    """
    # Construir particiones train/test
    num_ids = len(set(self.df['id']))
    num_test = np.floor((frac_test/100) * num_ids)
    test_indices = np.random.choice(list(set(self.df['id'])), size=num_test, replace=False)
    
    is_for_test = []
    for id in self.df['id']:
      if id in test_indices:
        is_for_test.append(True)
      else:
        is_for_test.append(False)
    is_for_test = np.asarray(is_for_test)
    
    train_df = self.df[~is_for_test]
    test_df = self.df[is_for_test]
    
    # Dividir entre atributos y clases
    X_train, y_train = train_df[attrs].values, train_df['class'].values
    X_test, y_test = test_df[attrs].values, test_df['class'].values
    
    return X_train, y_train, X_test, y_test