"""Solution for boosting uncertainty problem"""

from dataclasses import dataclass
from typing import List

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor


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
    ...
    return iterations


def virtual_ensemble_predict(
    model: GradientBoostingRegressor, X: np.ndarray, k: int = 20
) -> np.ndarray:
    ...
    return stage_preds


def predict_with_uncertainty(
    model: GradientBoostingRegressor, X: np.ndarray, k: int = 20
) -> PredictionDict:
    ...
    return prediction_dict
