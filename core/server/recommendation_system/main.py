import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))


def main() -> None:
    from system import RecommendationSystem

    learning_rates = [
        1e-2,
        1e-3,
        1e-4,
    ]
    dims = [
        (256, [512, 256, 128], 1),
        (512, [1024, 512, 256], 1),
        (1024, [2048, 1024, 512], 1),
        (256, [512, 256, 128, 64, 32], 1),
        (512, [1024, 512, 256, 128, 64], 1),
        (1024, [2048, 1024, 512, 256, 128], 1),
        (256, [512, 256, 128, 64, 32, 16, 8], 1),
        (512, [1024, 512, 256, 128, 64, 32, 16], 1),
        (1024, [2048, 1024, 512, 256, 128, 64, 32], 1),
    ]
    num_of_epochs = 10

    prefix = "exp"
    models = [
        (dims[j], learning_rates[i], num_of_epochs)
        for i in range(len(learning_rates))
        for j in range(len(dims))
    ]

    RecommendationSystem.compare_models(models, prefix)

    num_of_epochs = 100

    prefix = "lead"
    models = [
        ((256, [512, 256, 128], 1), 1e-3, num_of_epochs),
        ((256, [512, 256, 128], 1), 1e-2, num_of_epochs),
        ((1024, [2048, 1024, 512, 256, 128], 1), 1e-2, num_of_epochs),
        ((256, [512, 256, 128, 64, 32], 1), 1e-3, num_of_epochs),
        ((256, [512, 256, 128, 64, 32, 16, 8], 1), 1e-3, num_of_epochs),
    ]

    RecommendationSystem.compare_models(models, prefix)


if __name__ == "__main__":
    main()
