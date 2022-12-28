# -*- coding: utf-8 -*-
"""
Los datos en bruto no presentan un formato CSV de separador unico.

Este modulo lo formateara a un CSV con separador ','

Author:   Carlos Anivarro Batiste
Author:   Daniel Barahona Martin
Author:   Daniel Cerrato Sanchez
Author:   David Garitagoitia Romero
"""


def format_all(md_old_fn, md_new_fn, d_old_fn, d_new_fn):
    """
    Formatea el fichero de metadatos y de dataset.
    
    Los nuevos ficheros a generar no pueden tener el mismo nombre
    que los ficheros antiguos, esta funcion no permite sobreescritura.
    
    Args:
        md_old_fn:  Nombre del fichero de metadatos a formatear
        md_new_fn:  Nombre del nuevo fichero de metadatos a generar
        d_old_fn:   Nombre del fichero de dataset a formatear
        d_new_fn:   Nombre del nuevo fichero de dataset a generar
    """
    format_metadata(md_old_fn, md_new_fn)
    format_dataset(d_old_fn, d_new_fn)


def format_dataset(old_fn, new_fn):
    """
    Formatea el fichero de dataset a CSV con ','.
    
    Args:
        old_fn: Nombre del fichero a formatear
        new_fn: Nombre del nuevo fichero a generar
    """
    
    with open(old_fn, 'r') as f:
      with open(new_fn, 'w') as to_f:
        # Headers
        f.readline()
        
        headers = "id,time,R1,R2,R3,R4,R5,R6,R7,R8,Temp.,Humidity\r\n"
        to_f.write(headers)
        
        for line in f:
          new_line = line[:-3].replace('  ', ',') # 2 spaces per attribute
          new_line += '\r\n'
          to_f.write(new_line)


def format_metadata(old_fn, new_fn):
    """
    Formatea el fichero de metadatos a CSV con ','.
    
    Args:
        old_fn: Nombre del fichero a formatear
        new_fn: Nombre del nuevo fichero a generar
    """
    
    with open(old_fn, 'r') as f:
      with open(new_fn, 'w') as to_f:
        # Headers
        f.readline()
        
        headers = "id,date,class,t0,dt\r\n"
        to_f.write(headers)
        
        for line in f:
          new_line = line.replace('\t', ',') # 1 tab per attribute
          to_f.write(new_line)
            