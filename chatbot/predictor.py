import pickle
from pathlib import Path

import numpy as np

from chatbot.preprocess import clean_text

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / "models"

with open(MODEL_DIR / "model.pkl", "rb") as f:
    model = pickle.load(f)

with open(MODEL_DIR / "vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open(MODEL_DIR / "label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)


def predict(question):

    cleaned = clean_text(question)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)

    intent = label_encoder.inverse_transform(prediction)[0]

    confidence = 0.0

    # Logistic Regression
    if hasattr(model, "predict_proba"):

        confidence = float(
            np.max(model.predict_proba(vector))
        )

    # Linear SVM
    else:

        decision = model.decision_function(vector)

        if decision.ndim == 1:

            confidence = 0.40

        else:

            confidence = 0.40

    return {

        "intent": intent,

        "confidence": confidence

    }