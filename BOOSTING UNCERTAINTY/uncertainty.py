"""Solution for boosting uncertainty problem"""

from dataclasses import dataclass
from typing import List

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

def predict_with_first_n_trees(model: GradientBoostingRegressor, X: np.ndarray, n: int) -> np.ndarray:
    predictions = np.zeros((X.shape[0], n))
    for i, pred in enumerate(model.staged_predict(X)):
        if i < n:
            predictions[:, i] = pred
        else:
            break
    return predictions


@dataclass
class PredictionDict:
    pred: np.ndarray = np.array([])
    uncertainty: np.ndarray = np.array([])
    pred_virt: np.ndarray = np.array([])
    lcb: np.ndarray = np.array([])
    ucb: np.ndarray = np.array([])


def virtual_ensemble_iterations(
    model: GradientBoostingRegressor, k: int = 20
) -> List[int]:

    n_estimators = model.n_estimators
    iterations = []

    iterations = [i for i in range(n_estimators//2-1, n_estimators,k)]

    return iterations



def virtual_ensemble_predict(model: GradientBoostingRegressor, X, k=10):
    trees = model.estimators_
    num_trees = len(trees)
    count_vr =  virtual_ensemble_iterations(
    model, k)
    ens_preds = np.zeros((X.shape[0],len(count_vr))) 
    staged_preds = list(model.staged_predict(X))
    for j,num in enumerate(count_vr):

        ens_preds[:,j] = staged_preds[num].T

    return ens_preds
    

def predict_with_uncertainty(model: GradientBoostingRegressor, X: np.ndarray, k: int = 20) -> PredictionDict:
    
    pred =  virtual_ensemble_predict(model, X, k)
    uncertainty = np.var(pred, axis=1)
    pred_virt = np.mean(pred, axis=1)
    lcb = pred_virt - 3 * np.sqrt(uncertainty)
    ucb = pred_virt + 3 * np.sqrt(uncertainty)
    return PredictionDict(pred, uncertainty, pred_virt, lcb, ucb)