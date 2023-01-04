# -*- coding: utf-8 -*-
"""
Preprocesado del dataset en bruto de la UCI para adaptarlo a
las necesidades del proyecto.

Author:   Carlos Anivarro Batiste
Author:   Daniel Barahona Martin
Author:   Daniel Cerrato Sanchez
Author:   David Garitagoitia Romero
"""
import os
import numpy as np
import pandas as pd
from src.utils.ds_formatter import format_all


OLD_F_METADATA = "./data/HT_Sensor_metadata.dat"
F_METADATA = "./data/HT_Sensor_metadata_new.dat"
OLD_F_DATASET = "./data/HT_Sensor_dataset.dat"
F_DATASET = "./data/HT_Sensor_dataset_new.dat"

F_FINAL_DATASET = "./data/Final_dataset.dat"

FEATURES_ORIGINAL = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'Temp.', 'Humidity']
FEATURES = [
  'R1', 'R1_mean', 'R1_median', 'R1_dev',
  'R2', 'R2_mean', 'R2_median', 'R2_dev',
  'R3', 'R3_mean', 'R3_median', 'R3_dev',
  'R4', 'R4_mean', 'R4_median', 'R4_dev',
  'R5', 'R5_mean', 'R5_median', 'R5_dev',
  'R6', 'R6_mean', 'R6_median', 'R6_dev',
  'R7', 'R7_mean', 'R7_median', 'R7_dev',
  'R8', 'R8_mean', 'R8_median', 'R8_dev',
  'Temp.', 'Temp._mean', 'Temp._median', 'Temp._dev',
  'Humidity', 'Hum_mean', 'Hum_median', 'Hum_dev',
  'class',
]


def get_dataset(build_dataset=False, time_window=5, margin=10):
  """
  Devuelve un Dataframe con el dataset si este existe, y si no lo crea
  Tambien se puede indicar si se quiere recalcular el dataset
  
  Args:
    build_dataset: Para indicar si queremos recalcular el dataset
    time_window: Ventana de tiempo en minutos para tomar las medidas
    
  Return:
    Un Dataframe de pandas con el dataset formateado con nuestros atributos
  """
  # Si el fichero no existe o esta vacio, construirlo
  if build_dataset or os.stat(F_FINAL_DATASET).st_size == 0 or not os.path.exists(F_FINAL_DATASET):
    build_dataframe(F_FINAL_DATASET, time_window, margin)
  
  ds = pd.read_csv(F_FINAL_DATASET, sep=",")
  return ds
  
  
 
def build_dataframe(ds_filename, time_window, MARGIN):
  """
  Construye un dataset con atributos al uso para poder
  ejecutar experimentos de ML y lo guarda a un CSV
  
  Args:
    ds_filename: Nombre del fichero CSV al que escribir el dataset
    time_window: Ventana de tiempo en minutos para tomar las medidas
  """
  format_all(OLD_F_METADATA, F_METADATA, OLD_F_DATASET, F_DATASET)
  
  md = pd.read_csv(F_METADATA, sep=",")
  d = pd.read_csv(F_DATASET, sep=",")
  d.set_index(np.arange(d.shape[0]), inplace=True)
  
  with open(ds_filename, 'w') as f:
    # Headers
    f.write(','.join(FEATURES) + '\n')
    
    """
    1. Por cada serie (misma ID) en HT_Sensor_dataset_new.dat
      2. Calcular media, mediana y desv. de cada sensor, temperatura y humedad en base a los ultimos 5 minutos
      3. Añadir la nueva entrada a Final_dataset.dat
    """
    for _, md_row in md.iterrows():
      ide = md_row['id']
      clase = md_row['class']
      print(f'{ide} {clase} .... ', end='')
      
      for _, d_row in d.iterrows():
        # Si no son la misma serie, pasamos al siguiente
        if md_row['id'] != d_row['id']: continue

        # Ignorar el background de las muestras
        if d_row['time']*60 < -MARGIN or d_row['time']*60 > md_row['dt']*60+MARGIN:
          continue

        search_to = d_row['time']*60            # Muestra actual a minutos
        search_from = search_to - time_window   # Ventana de 5 minutos desde la que empezar a buscar

        # Debe estar dentro de la ventana de tiempo y tener el mismo ID.
        window = d[(d['time']*60 >= search_from) & (d['time']*60 < search_to) & (d['id'] == md_row['id'])]
        if window.empty: continue
        
        for f_o in FEATURES_ORIGINAL:
          # 1. Calcular medias, medianas y desviaciones de los atributos del df 'window'
          mean = window[f_o].mean()
          # median = window[f_o].median()
          dev = window[f_o].std(ddof=0)
          d_row[f'{f_o}_mean'] = mean
          # d_row[f'{f_o}_median'] = median
          d_row[f'{f_o}_dev'] = dev
          
        # Guardar clase
        if d_row['time'] < 0 or d_row['time'] > md_row['dt']:
          d_row['class'] = 'background'
        else:
          d_row['class'] = md_row['class']
        
        # 2. Esos nuevos valores obtenidos, meterlos a la entrada 'd_row' y guardarla: f.write(new_row)
        x = d_row[2:].to_string(index=False).split('\n')
        new_row = [','.join(ele.split()) for ele in x]
        f.write(','.join(new_row) + '\n')
      
      print('OK')
    

# def train_test_split(df, frac_test, attrs=FEATURES_ORIGINAL):
#   """
#   Divide un dataset en subconjuntos de entrenamiento y validacion
  
#   Args:
#     frac_test: Porcentaje (sobre 100) de muestras para validacion
#     attrs: Lista de atributos para datos (SIN clase)
    
#   Return:
#     X_train:  dataframe con datos de entrenamiento
#     y_train:  dataframe con clases de entrenamiento
#     X_test:   dataframe con datos de validacion
#     y_test:   dataframe con clases de validacion
#   """
#   # Construir particiones train/test
#   num_ids = len(set(df['id']))
#   num_test = np.floor((frac_test/100) * num_ids)
#   test_indices = np.random.choice(list(set(df['id'])), size=num_test, replace=False)
  
#   is_for_test = []
#   for id in df['id']:
#     if id in test_indices:
#       is_for_test.append(True)
#     else:
#       is_for_test.append(False)
#   is_for_test = np.asarray(is_for_test)
  
#   train_df = df[~is_for_test]
#   test_df = df[is_for_test]
  
#   # Dividir entre atributos y clases
#   X_train, y_train = train_df[attrs].values, train_df['class'].values
#   X_test, y_test = test_df[attrs].values, test_df['class'].values
  
#   return X_train, y_train, X_test, y_test