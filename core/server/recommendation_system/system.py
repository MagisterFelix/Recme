import math
import os
import pickle
import re
from pathlib import Path
from typing import Self

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from alive_progress import alive_bar, config_handler
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.metrics import (ConfusionMatrixDisplay, RocCurveDisplay, accuracy_score, auc, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_curve)

from core.server.recommendation_system.config import Settings, default_settings
from core.server.recommendation_system.network import NeuralNetwork
from core.server.recommendation_system.preprocessing import (CategoricalEncoder, Compressor, NumericalScaler,
                                                             TextVectorizer)
from core.server.recommendation_system.utils import LocationDataLoader, LocationDataset


class RecommendationSystem:

    _instance: Self | None = None

    def __new__(cls, settings: Settings = default_settings) -> Self:
        if not isinstance(settings, Settings):
            raise TypeError("Invalid type of settings.")

        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, settings: Settings = default_settings) -> None:
        os.chdir(Path(__file__).resolve().parent)

        config_handler.set_global(title_length=20, monitor_end=False, stats_end=False)
        torch.manual_seed(seed=42)

        self._settings = settings

        self._types = {
            "name": str,
            "category": str,
            "rating": np.uint8,
            "num_of_reviews": np.uint32,
            "latitude": np.float16,
            "longitude": np.float16,
            "context": str,
            "summary": str,
            "recommend": np.int8
        }

        nltk.data.path.append("data/nltk")

        if not os.path.exists("data/nltk"):
            nltk.download("punkt_tab", download_dir="data/nltk")
            nltk.download("wordnet", download_dir="data/nltk")
            nltk.download("stopwords", download_dir="data/nltk")

        if not os.path.exists(f"models/{self._settings.model_name}"):
            os.makedirs(f"models/{self._settings.model_name}")

        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self._preprocessors = {
            "encoders": {
                "category": CategoricalEncoder(max_categories=8192),
                "rating": NumericalScaler(),
                "num_of_reviews": NumericalScaler(),
                "rating_reviews_ratio": NumericalScaler(),
                "context": TextVectorizer(max_features=4096),
                "summary": TextVectorizer(max_features=16384)
            },
            "compressor": Compressor(n_components=self._settings.model_dims[0])
        }

        if os.path.exists(f"models/{self._settings.model_name}/preprocessors.pkl"):
            self._load_preprocessors()
        else:
            self._prepare_preprocessors()

        self._model = NeuralNetwork(*self._settings.model_dims).to(self._device)

        if os.path.exists(f"models/{self._settings.model_name}/model.pth"):
            self._load_model()
        else:
            if not os.path.exists(f"models/{self._settings.model_name}/output"):
                os.makedirs(f"models/{self._settings.model_name}/output")
            else:
                output_dir = os.listdir(f"models/{self._settings.model_name}/output")

                if len(output_dir) > 0:
                    for file in output_dir:
                        os.remove(f"models/{self._settings.model_name}/output/{file}")

            self._prepare_model()

    @staticmethod
    def compare_models(models: list[tuple[tuple[int, list[int], int], float, int]], prefix: str) -> None:
        if not os.path.exists(f"output/{prefix}"):
            os.makedirs(f"output/{prefix}")
        else:
            output_dir = os.listdir(f"output/{prefix}")

            if len(output_dir) > 0:
                for file in output_dir:
                    os.remove(f"output/{prefix}/{file}")

        def save_output(x: tuple[str], y: tuple[float], params: dict) -> None:
            best_val = max(y)
            best = [i for i, val in enumerate(y) if val == best_val]

            output = " | ".join([
                f"Best-{params["y_label"]}: {best_val:.4f}",
                f"Best-Models: {", ".join([x[val] for val in best])}"
            ])

            with open(f"output/{prefix}/log.txt", "a") as file:
                file.write(f"{output}\n")

            plt.rcParams.update({"font.size": 16})
            plt.figure(figsize=(16, 9))

            plt.bar(x, y, color=["C1" if i in best else "C0" for i in range(len(x))])

            plt.title(params["title"])
            plt.xlabel(params["x_label"])
            plt.ylabel(params["y_label"])

            plt.xticks([])
            for i, val in enumerate(y):
                plt.text(i, val, f"{val:.2f}", ha="center", va="bottom")
                plt.text(i, 0.025 * max(y), x[i], ha="center", va="bottom", color="w", fontweight="bold", rotation=90)

            plt.tight_layout()

            plt.savefig(f"output/{prefix}/{params["filename"]}")

            plt.cla()
            plt.clf()
            plt.close()

        results = []

        for (model_dims, learning_rate, num_of_epochs) in models:
            model_name = f"{prefix}_in_{model_dims[0]}_hl_{len(model_dims[1])}_lr_{learning_rate}"

            settings = Settings(
                model_name=model_name,
                model_dims=model_dims,
                learning_rate=learning_rate,
                num_of_epochs=(num_of_epochs, 1),
                confidence_threshold=0.5,
                train_data="data/train_data.csv",
                val_data="data/val_data.csv",
                test_data="data/test_data.csv"
            )

            recommendation_system = RecommendationSystem(settings)

            last_log = recommendation_system._load_logs()[-1]

            accuracy = float(m.group(1)) if (m := re.search(r"Test-Accuracy: ([0-9.]+)", last_log)) else 0.0
            f1_score = float(m.group(1)) if (m := re.search(r"Test-F1-Score: ([0-9.]+)", last_log)) else 0.0

            results.append((model_name, accuracy, f1_score))

        name, accuracy, f1_score = zip(*results)

        accuracy_params = {
            "title": "Accuracy of models",
            "x_label": "Models",
            "y_label": "Accuracy",
            "filename": "accuracy_comparison.png"
        }
        save_output(name, accuracy, accuracy_params)

        f1_score_params = {
            "title": "F1-Score of models",
            "x_label": "Models",
            "y_label": "F1-Score",
            "filename": "f1_score_comparison.png"
        }
        save_output(name, f1_score, f1_score_params)

    def _save_train_figures(self, data_x: list[list[int]], data_y: list[list[float]], params: dict) -> None:
        plt.figure(figsize=(16, 9))

        for i, (x, y) in enumerate(zip(data_x, data_y)):
            plt.plot(x, y, label=params["labels"][i], color=params["colors"][i], linestyle="-")

        plt.title(params["title"])
        plt.xlabel(params["x_label"])
        plt.ylabel(params["y_label"])
        plt.legend()

        plt.savefig(f"models/{self._settings.model_name}/output/{params["filename"]}")

        plt.cla()
        plt.clf()
        plt.close()

    def _save_test_figures(self, figure: RocCurveDisplay | ConfusionMatrixDisplay, params: dict) -> None:
        figure.plot()

        if isinstance(figure, RocCurveDisplay):
            plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="No Skill")

        plt.title(params["title"])

        plt.savefig(f"models/{self._settings.model_name}/output/{params["filename"]}")

        plt.cla()
        plt.clf()
        plt.close()

    def _save_logs(self, output: str) -> None:
        with open(f"models/{self._settings.model_name}/output/logs.txt", "a") as file:
            file.write(f"{output}\n")

    def _load_logs(self) -> list[str]:
        with open(f"models/{self._settings.model_name}/output/logs.txt", "r") as file:
            return file.readlines()

    def _save_preprocessors(self) -> None:
        with open(f"models/{self._settings.model_name}/preprocessors.pkl", "wb") as file:
            pickle.dump(self._preprocessors, file)

    def _load_preprocessors(self) -> None:
        with open(f"models/{self._settings.model_name}/preprocessors.pkl", "rb") as file:
            self._preprocessors = pickle.load(file)

    def _save_model(self) -> None:
        model_state = self._model.state_dict()
        torch.save(model_state, f"models/{self._settings.model_name}/model.pth")

    def _load_model(self) -> None:
        model_state = torch.load(f"models/{self._settings.model_name}/model.pth")
        self._model.load_state_dict(model_state)
        self._model.eval()

    def _prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop(["name", "latitude", "longitude"], axis=1)

        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words("english"))

        def clean_text(text: str) -> str:
            text = text.lower()
            text = re.sub(r"[^A-Za-z0-9_]+", " ", text)
            text = text.strip()

            tokens = word_tokenize(text)
            tokens = [
                lemmatizer.lemmatize(word) for word in tokens
                if word not in stop_words
            ]

            if not tokens:
                result = "missing information"
            else:
                result = " ".join(tokens)

            return result

        df["num_of_reviews"] = np.log1p(df["num_of_reviews"])
        df["rating_reviews_ratio"] = (df["rating"] - 3) * df["num_of_reviews"]

        df.loc[:, "category"] = df["category"].apply(clean_text)
        df.loc[:, "context"] = df["context"].apply(clean_text)
        df.loc[:, "summary"] = df["summary"].apply(clean_text)

        return df

    def _fit_encoders(self, df: pd.DataFrame) -> None:
        for key in self._preprocessors["encoders"]:
            self._preprocessors["encoders"][key].fit(df[[key]])

    def _extract_features(self, df: pd.DataFrame) -> np.ndarray:
        features = np.hstack(
            [
                self._preprocessors["encoders"][key].transform(df[[key]])
                for key in self._preprocessors["encoders"]
            ],
            dtype=np.float32
        )

        return features

    def _fit_compressor(self, features: np.ndarray) -> None:
        self._preprocessors["compressor"].fit(features)

    def _compress_features(self, features: np.ndarray) -> np.ndarray:
        features = self._preprocessors["compressor"].transform(features)
        return features

    def _preprocess(self, df: pd.DataFrame) -> np.ndarray:
        features = self._extract_features(df)
        preprocessed = self._compress_features(features)
        return preprocessed

    def _prepare_preprocessors(self) -> None:
        total = math.ceil(len(pd.read_csv(self._settings.train_data)) / self._settings.model_dims[0])

        with alive_bar(total=total * 2, title="Preprocessing...") as bar:

            with pd.read_csv(
                self._settings.train_data,
                dtype=self._types,
                chunksize=self._settings.model_dims[0],
            ) as reader:
                for chunk in reader:
                    df = self._prepare_data(chunk)
                    self._fit_encoders(df)

                    bar()

            with pd.read_csv(
                self._settings.train_data,
                dtype=self._types,
                chunksize=self._settings.model_dims[0],
            ) as reader:
                for chunk in reader:
                    df = self._prepare_data(chunk)
                    features = self._extract_features(df)
                    self._fit_compressor(features)

                    bar()

        self._save_preprocessors()

    def _train(self, df_train: pd.DataFrame, df_val: pd.DataFrame) -> None:
        num_epochs = self._settings.num_of_epochs[0]

        with alive_bar(total=num_epochs, title="Training...") as bar:

            X_train, y_train = df_train.drop("recommend", axis=1), df_train["recommend"].to_numpy()

            train_dataset = LocationDataset(X_train, y_train)
            train_dataloader = LocationDataLoader(
                train_dataset,
                preprocess=self._preprocess,
                batch_size=self._settings.model_dims[0],
                shuffle=True
            )

            X_val, y_val = df_val.drop("recommend", axis=1), df_val["recommend"].to_numpy()

            val_dataset = LocationDataset(X_val, y_val)
            val_dataloader = LocationDataLoader(
                val_dataset,
                preprocess=self._preprocess,
                batch_size=self._settings.model_dims[0],
                shuffle=False
            )

            criterion = nn.BCELoss()
            optimizer = optim.Adam(self._model.parameters(), lr=self._settings.learning_rate)

            min_val_loss = np.inf

            loss_train, loss_val = [0.0 for _ in range(num_epochs)], [0.0 for _ in range(num_epochs)]
            accuracy_train, accuracy_val = [0.0 for _ in range(num_epochs)], [0.0 for _ in range(num_epochs)]

            for epoch in range(num_epochs):
                self._model.train()

                train_loss = 0.0
                y_true, y_pred = [], []

                for X_batch, y_batch in train_dataloader:
                    optimizer.zero_grad()

                    outputs = self._model(X_batch.to(self._device))

                    loss = criterion(outputs, y_batch.to(self._device))
                    loss.backward()

                    optimizer.step()

                    train_loss += loss.item()

                    true = y_batch.cpu().numpy().flatten()
                    pred = (outputs >= self._settings.confidence_threshold).float().cpu().numpy().flatten()

                    y_true.extend(true)
                    y_pred.extend(pred)

                train_loss /= len(train_dataloader)
                train_accuracy = accuracy_score(y_true, y_pred)

                self._model.eval()

                val_loss = 0.0
                y_true, y_pred = [], []

                with torch.no_grad():
                    for X_batch, y_batch in val_dataloader:
                        outputs = self._model(X_batch.to(self._device))

                        loss = criterion(outputs, y_batch.to(self._device))

                        val_loss += loss.item()

                        true = y_batch.cpu().numpy().flatten()
                        pred = (outputs >= self._settings.confidence_threshold).float().cpu().numpy().flatten()

                        y_true.extend(true)
                        y_pred.extend(pred)

                val_loss /= len(val_dataloader)
                val_accuracy = accuracy_score(y_true, y_pred)

                if val_loss < min_val_loss:
                    min_val_loss = val_loss
                    self._save_model()

                output = " | ".join([
                    f"Epoch [{epoch + 1:>{len(str(self._settings.num_of_epochs[0]))}}/{num_epochs}]",
                    f"Train-Loss: {train_loss:.4f}",
                    f"Validation-Loss: {val_loss:.4f}",
                    f"Train-Accuracy: {train_accuracy:.4f}",
                    f"Validation-Accuracy: {val_accuracy:.4f}"
                ])
                self._save_logs(output)

                loss_train[epoch], loss_val[epoch] = float(train_loss), float(val_loss)
                accuracy_train[epoch], accuracy_val[epoch] = float(train_accuracy), float(val_accuracy)

                bar()

        epochs = list(range(1, self._settings.num_of_epochs[0] + 1))

        loss_params = {
            "title": "Training / Validation Loss",
            "x_label": "Epoch",
            "y_label": "Loss",
            "labels": ["Training Loss", "Validation Loss"],
            "colors": ["C0", "C1"],
            "filename": "train_val_loss.png"
        }
        self._save_train_figures([epochs, epochs], [loss_train, loss_val], loss_params)

        accuracy_params = {
            "title": "Training / Validation Accuracy",
            "x_label": "Epoch",
            "y_label": "Accuracy",
            "labels": ["Training Accuracy", "Validation Accuracy"],
            "colors": ["C0", "C1"],
            "filename": "train_val_accuracy.png"
        }
        self._save_train_figures([epochs, epochs], [accuracy_train, accuracy_val], accuracy_params)

        self._load_model()

    def _test(self, df_test: pd.DataFrame) -> None:
        X, y = df_test.drop("recommend", axis=1), df_test["recommend"].to_numpy()

        test_dataset = LocationDataset(X, y)
        test_dataloader = LocationDataLoader(
            test_dataset,
            preprocess=self._preprocess,
            batch_size=self._settings.model_dims[0],
            shuffle=False
        )

        self._model.eval()

        y_true, y_pred, y_score = [], [], []

        with torch.no_grad():
            for X_batch, y_batch in test_dataloader:
                outputs = self._model(X_batch.to(self._device))

                true = y_batch.cpu().numpy().flatten()
                pred = (outputs >= self._settings.confidence_threshold).float().cpu().numpy().flatten()
                score = outputs.float().cpu().numpy().flatten()

                y_true.extend(true)
                y_pred.extend(pred)
                y_score.extend(score)

        test_accuracy = accuracy_score(y_true, y_pred)
        test_recall = recall_score(y_true, y_pred)
        test_precision = precision_score(y_true, y_pred)
        test_f1_score = f1_score(y_true, y_pred)

        output = " | ".join([
            f"Test-Accuracy: {test_accuracy:.4f}",
            f"Test-Recall: {test_recall:.4f}",
            f"Test-Precision: {test_precision:.4f}",
            f"Test-F1-Score: {test_f1_score:.4f}"
        ])
        self._save_logs(output)

        fpr, tpr, _ = roc_curve(y_true, y_score)
        roc_auc = auc(fpr, tpr)
        auc_roc_curve_figure = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc)

        auc_roc_curve_params = {
            "title": "ROC Curve",
            "filename": "auc_roc_curve.png"
        }
        self._save_test_figures(auc_roc_curve_figure, auc_roc_curve_params)

        cm = confusion_matrix(y_true, y_pred)
        confusion_matrix_figure = ConfusionMatrixDisplay(confusion_matrix=cm)

        confusion_matrix_params = {
            "title": "Confusion Matrix",
            "filename": "confusion_matrix.png"
        }
        self._save_test_figures(confusion_matrix_figure, confusion_matrix_params)

    def _prepare_model(self) -> None:
        df_train = self._prepare_data(pd.read_csv(self._settings.train_data))
        df_val = self._prepare_data(pd.read_csv(self._settings.val_data))
        self._train(df_train, df_val)

        df_test = self._prepare_data(pd.read_csv(self._settings.test_data))
        self._test(df_test)

    def _predict(self, X: np.ndarray) -> torch.Tensor:
        X_tensor = torch.tensor(X, dtype=torch.float32).to(self._device)

        self._model.eval()

        with torch.no_grad():
            return self._model(X_tensor).squeeze()

    def _do_recommend(self, data: dict) -> bool:
        df = self._prepare_data(pd.DataFrame.from_records([data]))
        preprocessed = self._preprocess(df)

        prediction = self._predict(preprocessed)

        return prediction.item() >= self._settings.confidence_threshold

    def fine_tune(self, data: dict) -> None:
        df = self._prepare_data(pd.DataFrame.from_records([data]))

        num_epochs = self._settings.num_of_epochs[1]

        X, y = df.drop("recommend", axis=1), df["recommend"].to_numpy()

        X_train_tensor = torch.tensor(self._preprocess(X), dtype=torch.float32)
        y_train_tensor = torch.tensor(y, dtype=torch.float32).view(-1, 1)

        criterion = nn.BCELoss()
        optimizer = optim.Adam(self._model.parameters(), lr=self._settings.learning_rate)

        self._model.train()

        while num_epochs > 0:
            optimizer.zero_grad()

            outputs = self._model(X_train_tensor.to(self._device))

            loss = criterion(outputs, y_train_tensor.to(self._device))
            loss.backward()

            optimizer.step()

            num_epochs -= 1

        self._save_model()

    def get_recommendations(self, data: list[dict]) -> set[int]:
        recommendations = set()

        for item in data:
            if not self._do_recommend(item):
                continue

            recommendations.add(item["id"])

        return recommendations
