import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from settings import MODEL_DIR, TEST_DIR

# from features.helpers.file_helpers import save_list_to_file
# from features.helpers.data_helpers import natural_sort, plot_confusion_matrix
# from sklearn.metrics import confusion_matrix

# number of classes required argument
num_classes = int(sys.argv[1])

# provide model name
model_name = str(sys.argv[2]) + '_tloss'
matrix_name = sys.argv[3] + '_tloss'

print(rnd_clf.score(X=x_test, y=y_test))

feat_importances = pd.Series(rnd_clf.feature_importances_, index=FEATURE_NAMES)
feat_importances.nsmallest(13).plot(kind='barh')
plt.show()

