import sklearn
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report,confusion_matrix
from matplotlib import pyplot as plt
#got this from confusion_matrix tutorial
def plot_confusion_matrix(y_true, predictions, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = sklearn.metrics.confusion_matrix(y_true, predictions)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, predictions)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


def get_integer_mapping(le):
    '''
    Return a dict mapping labels to their integer values
    from an SKlearn LabelEncoder
    le = a fitted SKlearn LabelEncoder
    '''
    res = {}
    for cl in le.classes_:
        res.update({cl:le.transform([cl])[0]})

    return res
#main function was used from tutorial for using csv in pandas to run a classifier in sklearn:
# https://medium.com/dunder-data/from-pandas-to-scikit-learn-a-new-exciting-workflow-e88e2271ef62
def main():
    accuracy_counter = 0
    trainfile = open('train_merged_FEATURES123LIWC.csv')
    train = pd.read_csv(trainfile, header=0)
    y_train = train['act_tag']
    le = LabelEncoder().fit(y_train)
    integerMapping = get_integer_mapping(le)
    for elem in ['sd', 'b', 'sv', 'aa', '%', 'ba', 'qy', 'x', 'ny', 'fc']:
        print(integerMapping[elem])
    y_final = le.transform(y_train)
    x_train = train.drop(['swda_filename', 'transcript index', 'act_tag', 'original text', 'cleaned text'], axis=1)
    testfile = open('test_merged_FEATURES123LIWC.csv')
    test = pd.read_csv(testfile, header=0)
    y_test = test['act_tag']
    encoded_y_test = LabelEncoder().fit(y_train).transform(y_test)
    x_test = test.drop(['swda_filename', 'transcript index', 'act_tag' , 'original text', 'cleaned text'], axis=1)

    classifier = OneVsRestClassifier(MLPClassifier()).fit(x_train, y_final)
    predictions = classifier.predict(x_test)

    for act_tag in range(0,len(predictions)):
        if predictions[act_tag] == encoded_y_test[act_tag]:
            accuracy_counter += 1
    #print(accuracy_counter/len(predictions) * 100)
    print(confusion_matrix(encoded_y_test,predictions))


main()
