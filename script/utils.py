
import pandas as pd
import numpy as np

from scipy import stats
from scipy import interp
from scipy import spatial
from scipy import cluster
from collections import Counter
from sklearn.svm import LinearSVC
from sklearn.model_selection import KFold
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_predict

def compute_roc(z, labels, classifier=LinearSVC(C=0.001), cv_folds=10):
    """Compute the ROC (false positive rate, true positive rate) using cross-validation.

    Parameters
    ----------
    z:          DataFrame (n_samples, n_latent_factors) of latent factor values
    y:          Series (n_samples,) of ground-truth labels to try to predict
    classifier: Classifier object to use, default ``LinearSVC(C=.001)``

    Returns
    -------
    roc_curves: dict, one key per class as well as "mean", each value is a dataframe
                containing the tpr (true positive rate) and fpr (false positive rate)
                defining that class (or the mean) ROC.
    """
    
    #unique_label = sorted(labels.unique())
    num_clusters = dict(zip(sorted(labels.unique()), 
                       [i for i in range(30)]))
    y = pd.Series([num_clusters[l] for l in labels])
    class_names = sorted(labels.unique())
    z_to_use = z
    y_true_bin = label_binarize(y, classes=sorted(y.unique()))
    y_proba = cross_val_predict(
        classifier, z_to_use, y, cv=cv_folds, method="decision_function"
    )

    # Compute ROC curve and ROC area for each class
    roc_curves = dict()
    for i, cl_name in enumerate(class_names):
        fpr, tpr, thresholds = roc_curve(y_true_bin[:, i], y_proba[:, i])
        roc_curves[str(cl_name)] = pd.concat(
            [pd.Series(fpr, name="FPR"), pd.Series(tpr, name="TPR")], axis=1
        )
        
    mean_fpr = np.unique(
        np.concatenate([roc_curves[str(cl_name)].FPR for cl_name in class_names])
    )

    # Then interpolate all ROC curves at this points
    mean_tpr = np.zeros_like(mean_fpr)
    
    
    for cl_name in class_names:
        cl_name = str(cl_name)
        mean_tpr += interp(mean_fpr, roc_curves[cl_name].FPR, roc_curves[cl_name].TPR)

    # Finally average it
    mean_tpr /= len(class_names)

    roc_curves["mean"] = pd.concat(
        [pd.Series(mean_fpr, name="FPR"), pd.Series(mean_tpr, name="TPR")], axis=1
    )
    return roc_curves
