import os
import sys
import datetime
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..',))

import numpy as np
from settings import MODEL_DIR, USE_GPU
from features.helpers.data_helpers import get_train_data, get_test_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV


# def evaluate(title, model, test_features, test_labels):
#     predictions = model.predict(test_features)
#     errors = abs(predictions - test_labels)
#     mape = 100 * np.mean(errors / test_labels)
#     accuracy = 100 - mape
#     with open('random_search.txt', 'a+') as f:
#         print('Model name ' + title, file=f)
#         print('Model Performance', file=f)
#         print('Average Error: {:0.4f} degrees.'.format(
#             np.mean(errors)), file=f)
#         print('Accuracy = {:0.2f}%.'.format(accuracy), file=f)

#     return accuracy

if USE_GPU:
    # use if you are running on a PC with many GPU-s
    # needs to be at the beginning of the file
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    # the GPU id to use, usually either "0" or "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    # just disables the warning, doesn't enable AVX/FMA
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"

x_train, y_train = get_train_data()

# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start=50, stop=1000, num=20)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]

# Create the random grid
random_grid = {
    'n_estimators': n_estimators,
    'max_features': max_features,
    'max_depth': max_depth,
    'min_samples_split': min_samples_split,
    'min_samples_leaf': min_samples_leaf,
    'bootstrap': bootstrap
}

# Kreiranje random forest klasifikatora
rnd_clf = RandomForestClassifier(
    n_jobs=-1,
    verbose=2,
)

rf_random = RandomizedSearchCV(
    estimator=rnd_clf,
    param_distributions=random_grid,
    n_iter=100,
    cv=3,
    verbose=2,
    random_state=42,
    n_jobs=-1
)

rf_random.fit(X=x_train, y=y_train)
print(rf_random.best_params_)


# x_test, y_test = get_test_data()

# # create and erase file
# open('random_search.txt', 'w+').close()

# base_model = RandomForestClassifier(n_estimators=10, random_state=42)
# base_model.fit(x_train, y_train)
# base_accuracy = evaluate('base model', base_model, x_test, y_test)

# best_random = rf_random.best_estimator_
# random_accuracy = evaluate('best random', best_random, x_test, y_test)

# print(
#     'Improvement of {:0.2f}%.'.format(
#         100 * (random_accuracy - base_accuracy) / base_accuracy)
# )
