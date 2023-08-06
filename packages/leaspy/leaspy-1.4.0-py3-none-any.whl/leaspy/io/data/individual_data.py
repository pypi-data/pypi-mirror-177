from bisect import bisect

import numpy as np

from leaspy.exceptions import LeaspyDataInputError, LeaspyTypeError
from leaspy.utils.typing import Any, Dict, FeatureType, IDType, List


class IndividualData:
    """
    Container for an individual's data

    Parameters
    ----------
    idx : IDType
        Unique ID
        
    Attributes
    ----------
    idx : IDType
        Unique ID
    timepoints : np.ndarray[float, 1D]
        Timepoints associated with the observations
    observations : np.ndarray[float, 2D]
        Observed data points.
        Shape is ``(n_timepoints, n_features)``
    cofactors : Dict[FeatureType, Any]
        Cofactors in the form {cofactor_name: cofactor_value}
    """

    def __init__(self, idx: IDType):
        self.idx: IDType = idx
        self.timepoints: np.ndarray = None
        self.observations: np.ndarray = None
        self.cofactors: Dict[FeatureType, Any] = {}

    def add_observations(self, timepoints: List[float], observations: List[List[float]]) -> None:
        """
        Include new observations and associated timepoints

        Parameters
        ----------
        timepoints : array-like[float, 1D]
            Timepoints associated with the observations to include
        observations : array-like[float, 2D]
            Observations to include

        Raises
        ------
        :exc:`.LeaspyDataInputError`
        """
        for t, obs in zip(timepoints, observations):
            if self.timepoints is None:
                self.timepoints = np.array([t])
                self.observations = np.array([obs])
            elif t in self.timepoints:
                raise LeaspyDataInputError(f"Trying to overwrite timepoint {t} "
                                           f"of individual {self.idx}")
            else:
                index = bisect(self.timepoints, t)
                self.timepoints = np.concatenate([
                    self.timepoints[:index],
                    [t],
                    self.timepoints[index:]
                ])
                self.observations = np.concatenate([
                    self.observations[:index],
                    [obs],
                    self.observations[index:]
                ])

    def add_cofactors(self, d: Dict[FeatureType, Any]) -> None:
        """
        Include new cofactors

        Parameters
        ----------
        d : Dict[FeatureType, Any]
            Cofactors to include, in the form `{name: value}`

        Raises
        ------
        :exc:`.LeaspyDataInputError`
        :exc:`.LeaspyTypeError`
        """
        if not (
            isinstance(d, dict)
            and all(isinstance(k, str) for k in d.keys())
        ):
            raise LeaspyTypeError("Invalid argument type for `d`")

        for k, v in d.items():
            if k in self.cofactors.keys() and v != self.cofactors[k]:
                raise LeaspyDataInputError(f"Cofactor {k} is already present "
                                           f"for patient {self.idx}")
            self.cofactors[k] = v
