sopila-transcriptor
==============================

Automated music processing of traditional Croatian instrument - sopila

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── real_data      <- Data for transciption of real music pieces.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │   └── sheets         <- Generated PDF music sheet predictions
    │   └── statistics     <- Accuracy, precision, recall and F1 score for training, validation and test data.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    |   |   ├── make_alternate_data.py
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   ├── create_processed_data <- Creates processed data for all models
    │   │   └── alternate_data_create.py <- Creates processed real music recording for model prediction
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    |   |   ├── rf         <- Random forest train and predict scripts
    │   │   └── cnn        <- Convolitional Neural Network train and predict scripts
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── make_sheets.py
    │
    ├── tox.ini            <- tox file with settings for running tox; see tox.testrun.org
    └── settings.py        <- Project specific settings


--------
Environment instructions:

1. conda env create -f sopela_env.yml
Different env for using visualization/make_sheets.py due to python version incompatibility
2. conda env create -f make_sheets_env.yml
3. conda activate sopela_env
4. pip install -r requirements.txt
<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
