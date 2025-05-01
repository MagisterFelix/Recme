import torch
import torch.nn as nn


class NeuralNetwork(nn.Module):

    def __init__(self, in_dim: int, hidden_dims: list[int], out_dim: int) -> None:
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(in_dim, hidden_dims[0]),
            nn.LeakyReLU(),
            nn.Dropout(),
            *[
                layer for i in range(len(hidden_dims) - 1)
                for layer in (
                    nn.Linear(hidden_dims[i], hidden_dims[i + 1]),
                    nn.LeakyReLU(),
                    nn.Dropout()
                )
            ],
            nn.Linear(hidden_dims[-1], out_dim),
            nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)
