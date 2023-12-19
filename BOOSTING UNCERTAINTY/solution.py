from typing import Any

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection._split import _BaseKFold
import pandas as pd
from sklearn.model_selection._split import _BaseKFold, indexable, _num_samples
def mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred)/y_true))


def smape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    
    return np.mean(2*np.abs(y_pred - y_true)/(np.abs(y_true) + np.abs(y_pred)  ))

def wape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    
    return np.sum(np.abs(y_pred - y_true)) / np.sum(np.abs(y_true)) 



def bias(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    
    return np.sum(y_pred-y_true)/np.sum(np.abs(y_true))

class GroupTimeSeriesSplit(_BaseKFold):

    def __init__(self, n_splits=5, max_train_size=None, test_size=None, gap=0):
        super().__init__(
            n_splits=n_splits,
            shuffle=False,
            random_state=None,
        )
        self.max_train_size = max_train_size
        self.test_size = test_size
        self.gap = gap

    def split(self, X, y=None, groups=None):
   

        if groups is None:
            raise ValueError("The 'groups' parameter should not be None.")

        X, y, groups = indexable(X, y, groups)

        # Get unique values of groups and their corresponding indices
        grps, grps_ix = np.unique(groups, return_inverse=True)
        n_samples = _num_samples(grps)

        # Set default test_size if not specified
        n_splits = self.n_splits
        n_folds = n_splits + 1
        gap = self.gap
        test_size = (
            self.test_size if self.test_size is not None else n_samples // n_folds
        )

        # Make sure we have enough samples for the given split parameters
        if n_folds > n_samples:
            raise ValueError(
                f"Cannot have number of folds={n_folds} greater"
                f" than the number of samples={n_samples}."
            )

        if n_samples - gap - (test_size * n_splits) <= 0:
            raise ValueError(
                f"Too many splits={n_splits} for number of samples"
                f"={n_samples} with test_size={test_size} and gap={gap}."
            )

        # Generate indices for each split
        indices = np.arange(n_samples)
        test_starts = range(n_samples - n_splits * test_size, n_samples, test_size)

        # Generate splits
        for test_start in test_starts:
            train_end = test_start - gap
            
            if self.max_train_size and self.max_train_size < train_end:
                train = indices[train_end - self.max_train_size : train_end]
                test = indices[test_start : test_start + test_size]
            else:
                train = indices[:train_end]
                test = indices[test_start : test_start + test_size]

            # Yield indices in X corresponding to the groups
            yield (
                np.flatnonzero(np.in1d(grps_ix, train)),
                np.flatnonzero(np.in1d(grps_ix, test)),
            )

def best_model() -> Any:
    model = GradientBoostingRegressor(max_depth=5
                                      ,random_state=121,n_estimators=200,learning_rate = 0.1)
    return model
