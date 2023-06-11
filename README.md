# Gas-sensor-for-home-activity

## *Exploration of Machine Learning models for online classification of MOX-Humidity-Temperature sensor metrics*

The following is part of the final assignment of Fundamentals of Machine Learning, course 2022-23.

Project authors:

+ Carlos Anivarro Batiste: carlos.anivarro@estudiante.uam.es

+ Daniel Barahona Martin: daniel.barahonam@estudiante.uam.es

+ Daniel Cerrato Sanchez: daniel.cerrato@estudiante.uam.es

+ David T. Garitagoitia Romero: david.garitagoitia@estudiante.uam.es

For citations using BibTeX:

```
@inproceedings{aniv2023exploracion,
    title={Exploración de modelos de aprendizaje automático para la clasificación online de mediciones de sensores MOX-Humedad-Temperatura},
    author={Anivarro, Carlos and Barahona, Daniel and Cerrato, Daniel and Garitagoitia, David T.},
    year={2023},
    organization={UAM}
}
```

***

The project is done using the Gas Sensor for home activity monitoring dataset, from its official UCI website: https://archive.ics.uci.edu/ml/datasets/Gas+sensors+for+home+activity+monitoring

The main project is structured on the following files and directories:

+ **data**: contains all `.dat` files with the dataset, in both the original form and our construction.

+ **images**: contains a collection of graphs generated during the "study of dataset" phase.

+ **src**: contains various source code files:

    - **utils**: contains code files to help with the formatting of the original `.dat` files.

    - **dataset.py**: an encapsulation of the dataset for usability purposes.

    - **plot_sensors.py**: originally from the UCI project, this script helps to plot the MOX-Hum-Temp series from the original dataset.

+ **.ipynb files**: these are the Jupyter Notebook files with the majority of the project's work.

The rest of the files are for testing ("messing around") purposes.

Project supervised by Gonzalo Martínez Muñoz (Universidad Autónoma de Madrid): gonzalo.martinez@uam.es

***

To run the notebooks (Windows):

1. Create and activate a Python virtual environment:

```
$ python -m venv env
$ .\env\Scripts\activate
```

2. Install the dependencies:

```
$ pip install -r .\requirements.txt
```

3. Run Jupyter on a local server with:

```
$ jupyter notebook
```

***

Original authors:
Ramon Huerta, Thiago Mosqueiro, Jordi Fonollosa, Nikolai Rulkov, Irene Rodriguez-Lujan. Online Decorrelation of Humidity and Temperature in Chemical Sensors for Continuous Monitoring. Chemometrics and Intelligent Laboratory Systems 2016.
