from typing import Callable

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset


class LocationDataset(Dataset):

    def __init__(self, data: pd.DataFrame, labels: np.ndarray) -> None:
        self._data = data
        self._labels = labels

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index: int) -> tuple[pd.DataFrame, np.int8]:
        return self._data.iloc[[index]], self._labels[index]


class LocationDataLoader(DataLoader):

    def __init__(self, dataset: LocationDataset, preprocess: Callable[[pd.DataFrame], np.ndarray], **params) -> None:
        self._preprocess = preprocess
        super().__init__(dataset, collate_fn=self.collate_fn, **params)

    def collate_fn(self, batch: list[tuple[pd.DataFrame, np.int8]]) -> tuple[torch.Tensor, torch.Tensor]:
        data, labels = zip(*batch)

        X = self._preprocess(pd.concat(data, ignore_index=True))
        y = np.array(labels)

        return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32).view(-1, 1)
