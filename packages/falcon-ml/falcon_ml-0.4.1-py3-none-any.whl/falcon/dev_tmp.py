from catboost.datasets import msrank, msrank_10k
from falcon import AutoML
from sklearn.metrics import balanced_accuracy_score
from lightgbm import LGBMClassifier
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier

def msrank_test(fast = True):
    if fast: 
        train, test = msrank_10k()
    else: 
        train, test = msrank()
    train.pop(1), test.pop(1)
    y_train = train.pop(0)
    y_test = test.pop(0)
    AutoML(task = 'tabular_classification', train_data = (train, y_train), test_data=(test, y_test))


def lgbm(fast = True):
    if fast: 
        train, test = msrank_10k()
    else: 
        train, test = msrank()
    train.pop(1), test.pop(1)
    y_train = train.pop(0).to_numpy()
    y_test = test.pop(0).to_numpy()
    train = train.to_numpy()
    test = test.to_numpy()
    clf = LGBMClassifier()
    clf.fit(train, y_train)
    pred = clf.predict(test)
    pred = np.squeeze(pred)
    print(balanced_accuracy_score(pred, y_test))


def hgb(fast = True):
    if fast: 
        train, test = msrank_10k()
    else: 
        train, test = msrank()
    train.pop(1), test.pop(1)
    y_train = train.pop(0).to_numpy()
    y_test = test.pop(0).to_numpy()
    train = train.to_numpy()
    test = test.to_numpy()
    clf = HistGradientBoostingClassifier()
    clf.fit(train, y_train)
    pred = clf.predict(test)
    pred = np.squeeze(pred)
    print(balanced_accuracy_score(pred, y_test))