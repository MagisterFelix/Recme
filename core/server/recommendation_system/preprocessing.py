from collections import Counter

import numpy as np
import pandas as pd
from scipy.sparse._csr import spmatrix
from sklearn.decomposition import IncrementalPCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class CategoricalEncoder:

    def __init__(self, max_categories: int, weight: float = 1.0) -> None:
        self._max_categories = max_categories
        self._weight = weight
        self._counter = Counter()

        self._encoder = OneHotEncoder(
            handle_unknown="ignore",
            max_categories=self._max_categories,
            sparse_output=False,
        )

    def fit(self, data: pd.DataFrame) -> None:
        self._counter.update(data.to_numpy().reshape(-1, 1).flatten())
        most_common_categories = [category[0] for category in self._counter.most_common(self._max_categories)]

        self._encoder = OneHotEncoder(
            categories=[most_common_categories],
            handle_unknown="ignore",
            max_categories=self._max_categories,
            sparse_output=False,
        )
        self._encoder.fit(data)

    def transform(self, data: pd.DataFrame) -> np.ndarray | spmatrix:
        return self._encoder.transform(data) * self._weight

    def fit_transform(self, data: pd.DataFrame) -> np.ndarray | spmatrix:
        self.fit(data)
        return self.transform(data)


class NumericalScaler:

    def __init__(self, weight: float = 1.0) -> None:
        self._weight = weight

        self._scaler = StandardScaler()

    def fit(self, data: pd.DataFrame) -> None:
        self._scaler.partial_fit(data)

    def transform(self, data: pd.DataFrame) -> np.ndarray:
        return self._scaler.transform(data).reshape(-1, 1) * self._weight

    def fit_transform(self, data: pd.DataFrame) -> np.ndarray:
        self.fit(data)
        return self.transform(data)


class TextVectorizer:

    def __init__(self, max_features: int, weight: float = 1.0) -> None:
        self._max_features = max_features
        self._weight = weight
        self._counter = Counter()

        self._vectorizer = TfidfVectorizer(
            strip_accents="unicode",
            max_features=self._max_features,
        )

    def fit(self, data: pd.DataFrame) -> None:
        self._counter.update(data.iloc[:, 0].str.cat(sep=" ").split())
        most_common_vocabulary = [word[0] for word in self._counter.most_common(self._max_features)]

        self._vectorizer = TfidfVectorizer(
            vocabulary=most_common_vocabulary,
            strip_accents="unicode",
            max_features=self._max_features,
        )
        self._vectorizer.fit(data.iloc[:, 0])

    def transform(self, data: pd.DataFrame) -> np.ndarray:
        return np.asarray(self._vectorizer.transform(data.iloc[:, 0]).todense()) * self._weight

    def fit_transform(self, data: pd.DataFrame) -> np.ndarray:
        self.fit(data)
        return self.transform(data)


class Compressor:

    def __init__(self, n_components: int) -> None:
        self._n_components = n_components
        self._compressor = IncrementalPCA(n_components=self._n_components)

    def fit(self, data: np.ndarray) -> None:
        self._compressor.partial_fit(data)

    def transform(self, data: np.ndarray) -> np.ndarray:
        return self._compressor.transform(data)

    def fit_transform(self, data: np.ndarray) -> np.ndarray:
        self.fit(data)
        return self.transform(data)
