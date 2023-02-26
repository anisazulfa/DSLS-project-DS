# Irregularities traffic case

case machine learning from waze for cities

## Setup

Start the project with environment setup

    $ pip install virtualenv
    $ virtualenv [enviroment name]
    $ source [enviroment name]/bin/activate
    $ pip install -r requirements.txt

or run this script for windows users

    $ pip install virtualenv
    $ venv [enviroment name]
    $ .\[enviroment name]\Scripts\activate
    $ pip install -r requirements.txt

## Train Model

    $ python src/data_pipeling.py # run data pipeline
    $ python src/preprocessing.py # run preprocessing data
    $ python src/modelling.py # run modeling data

## API

    $ python src/api.py # run api
    $ streamlit run src/streamlit.py # run streamlit 
