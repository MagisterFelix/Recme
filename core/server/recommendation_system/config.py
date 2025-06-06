from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    model_name: str
    model_dims: tuple[int, list[int], int]
    learning_rate: float
    num_of_epochs: tuple[int, int]
    confidence_threshold: float

    train_data: str
    val_data: str
    test_data: str


default_settings = Settings(
    model_name="default",
    model_dims=(256, [512, 256, 128], 1),
    learning_rate=1e-3,
    num_of_epochs=(100, 10),
    confidence_threshold=0.5,
    train_data="data/train_data.csv",
    val_data="data/val_data.csv",
    test_data="data/test_data.csv"
)
