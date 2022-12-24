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


META_F = "./data/ori/HT_Sensor_metadata.dat"
DATA_F = "./data/ori/HT_Sensor_dataset.dat"
FEATURES_ORIGINAL = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'Temp.', 'Humidity']


class Dataset(Object):
  """
  Clase usada para encapsular el dataset
  
  Atributos:
    df: Dataframe de Pandas con los datos separados por atributos
  """

  
  def __init__(self):
    self.df = self.build_dataframe()
    
  
  def join_metadata_dataset(metadata_f, dataset_f):
    """
    Une los metadatos con la BD principal de las series usando el campo
    'id' para el join
    
    Attrs:
      metadata_f: Nombre del fichero con los metadatos
      dataset_f: Nombre del fichero con las series
    """
    df_meta = pd.read_csv(meta_f, delimiter='\t+', engine='python')
    df_data = pd.read_csv(dataset_f, delimiter='\s+', engine='python')
    
    df_db.set_index('id', inplace=True)
    # Hacer un inner join de metadatos con series
    df_db.join(df_meta, how='inner')
    
    # Recalcular time (para que no haya tiempos negativos)
    df_db['time'] += df_db['t0']
    
    df_db.set_index(np.arange(df_db.shape[0]), inplace=True)
    
    return df_db
    
   
  def build_dataframe(self):
    """
    Construye un dataset con atributos al uso para poder
    ejecutar experimentos de ML
    
    IDEAS DE ATRIBUTOS:
      - Media y mediana de los ultimos X mins
      - Desviación de los últimos X mins
      - Umbral de desviación para ver si es vino o cambio de pendiente
      - Numero de muestras del intervalo de los últimos X minutos
      - Lo de las 5 “sigmas”

      'X' debería ser no muy grande: si queremos hacer datos en tiempo real,
      poner una ventana de los ultimos 15 minutos es un poco obstáculo
    
    Return:
      Un Dataframe de pandas con el dataset
    """
    join_df = join_metadata_dataset(META_F, DATA_F)
    
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
    for id in self.df.id:
      if id in test_indices:
        is_for_test.append(True)
      else:
        is_for_test.append(False)
    is_for_test = np.asarray(is_for_test)
    
    train_df = self.df[~is_for_test]
    test_df = self.df[is_for_test]
    
    # Dividir entre atributos y clases
    X_train, y_train = train_df[attrs].values, df_train['class'].values
    X_test, y_test = test_df[attrs].values, test_df['class'].values
    
    return X_train, y_train, X_test, y_test