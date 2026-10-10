import json
import pickle
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from preprocess import clean_text


# =====================================
# PATHS
# =====================================

BASE_DIR = Path(__file__).resolve().parent

INTENT_FILE = BASE_DIR / "intents.json"

MODEL_DIR = BASE_DIR.parent / "models"

MODEL_DIR.mkdir(exist_ok=True)


# =====================================
# LOAD DATA
# =====================================

with open(INTENT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

texts = []
labels = []

for intent in data["intents"]:

    tag = intent["tag"]

    for pattern in intent["patterns"]:

        texts.append(clean_text(pattern))
        labels.append(tag)


# =====================================
# LABEL ENCODER
# =====================================

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(labels)


# =====================================
# TF-IDF
# =====================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(texts)


# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)


# =====================================
# LOGISTIC REGRESSION
# =====================================

model = LogisticRegression(

    max_iter=2000,

    random_state=42

)

model.fit(X_train, y_train)


# =====================================
# EVALUATION
# =====================================

prediction = model.predict(X_test)

accuracy = accuracy_score(

    y_test,

    prediction

)

print("=" * 50)

print("MODEL TRAINING")

print("=" * 50)

print(f"Model     : Logistic Regression")

print(f"Accuracy  : {accuracy:.2%}")

print("=" * 50)


# =====================================
# SAVE
# =====================================

with open(MODEL_DIR / "model.pkl", "wb") as f:
    pickle.dump(model, f)

with open(MODEL_DIR / "vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open(MODEL_DIR / "label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print()

print("✅ model.pkl Saved")

print("✅ vectorizer.pkl Saved")

print("✅ label_encoder.pkl Saved")

print()

print("🎉 Training Completed Successfully")