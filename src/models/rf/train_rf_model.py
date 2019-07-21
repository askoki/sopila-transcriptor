import os
import sys
import datetime
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score
sys.path.insert(1, os.path.join(sys.path[0], '..', '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from settings import MODEL_DIR
from features.helpers.data_helpers import plot_rf_model_statistics, \
    get_train_data, write_rf_model_statistics


if not sys.argv[1]:
    print('Enter model name defined in settings.py')
    sys.exit()

ML_MODEL = str(sys.argv[1])

if not sys.argv[2]:
    print(
        'Enter training parameters in the following order: n_estimators, \
        criterion, min_samples_split, min_samples_leaf, max_features, \
        max_depth, bootstrap'
    )
    sys.exit()


string_parameters = sys.argv[2].strip('[]').split(',')
parameters = []
for param in string_parameters:
    try:
        parameters.append(int(param))
    except ValueError:
        if param == 'True' or param == 'False':
            parameters.append(param == 'True')
        else:
            parameters.append(param)

if not sys.argv[3]:
    print('Pass True as an argument if you would like to save a model.')
    sys.exit()

save_model = (sys.argv[3] == 'True')

# END OF ARGUMENTS


x_train, y_train = get_train_data(ML_MODEL)

x_train, x_val, y_train, y_val = train_test_split(
    x_train, y_train, train_size=0.8, random_state=42
)


print(parameters)

name = ML_MODEL
for i in range(len(parameters)):
    name += '_' + str(parameters[i])

# Kreiranje random forest klasifikatora
rnd_clf = RandomForestClassifier(
    n_estimators=parameters[0],
    criterion=parameters[1],
    min_samples_split=parameters[2],
    min_samples_leaf=parameters[3],
    max_features=parameters[4],
    max_depth=parameters[5],
    bootstrap=parameters[6],
    n_jobs=28,
    verbose=2
)

# Train model and test it on validation set
print('Before:')
print(datetime.datetime.now())

rnd_clf.fit(X=x_train, y=y_train)

print('After:')
print(datetime.datetime.now())

if save_model:
    dump(
        rnd_clf,
        os.path.join(MODEL_DIR, ML_MODEL, name + '.joblib')
    )

y_predicted_training = rnd_clf.predict(x_train)

train_accuracy = rnd_clf.score(X=x_train, y=y_train)
train_precision = precision_score(
    y_train,
    y_predicted_training,
    average='micro'
)
train_recall = recall_score(y_train, y_predicted_training, average='micro')

y_predicted = rnd_clf.predict(x_val)

val_accuracy = rnd_clf.score(X=x_val, y=y_val)
val_precision = precision_score(y_val, y_predicted, average='micro')
val_recall = recall_score(y_val, y_predicted, average='micro')

metrics_dict = {
    'acc_train': train_accuracy,
    'precision_train': train_precision,
    'recall_train': train_recall,
    'acc_val': val_accuracy,
    'precision_val': val_precision,
    'recall_val': val_recall
}

write_rf_model_statistics(
    name, metrics_dict, x_train, x_val, parameters, ML_MODEL
)
plot_rf_model_statistics(
    'accuracy',
    train_accuracy,
    val_accuracy,
    name,
    ML_MODEL
)

print(train_accuracy)
print(val_accuracy)
