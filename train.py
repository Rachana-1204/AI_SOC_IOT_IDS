import pandas as pd
import numpy as np
import joblib
import os

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from xgboost import XGBClassifier

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.callbacks import EarlyStopping

# =====================================================
# CREATE MODEL FOLDER
# =====================================================

os.makedirs("model", exist_ok=True)

# =====================================================
# LOAD DATASET
# =====================================================

print("Loading dataset...")

df = pd.read_csv("data.csv")

# =====================================================
# FEATURES & LABELS
# =====================================================

X = df.drop('Label', axis=1)
y = df['Label']

# =====================================================
# SAVE FEATURE NAMES
# =====================================================

joblib.dump(
    list(X.columns),
    'model/features.pkl'
)

print("✅ Feature names saved!")

# =====================================================
# FEATURE SCALING
# =====================================================

print("Scaling features...")

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# Save scaler
joblib.dump(
    scaler,
    'model/scaler.pkl'
)

print("✅ Scaler saved!")

# =====================================================
# TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =====================================================
# ISOLATION FOREST
# =====================================================

print("\nTraining Isolation Forest...")

iso_model = IsolationForest(
    contamination=0.25,
    random_state=42
)

iso_model.fit(X_train)

# Save model
joblib.dump(
    iso_model,
    'model/isolation_forest.pkl'
)

print("✅ Isolation Forest saved!")

# =====================================================
# XGBOOST
# =====================================================

print("\nTraining XGBoost...")

xgb_model = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    eval_metric='logloss',
    random_state=42
)

xgb_model.fit(
    X_train,
    y_train
)

# Predictions
xgb_pred = xgb_model.predict(
    X_test
)

# Accuracy
xgb_acc = accuracy_score(
    y_test,
    xgb_pred
)

print(f"\n✅ XGBoost Accuracy: {xgb_acc:.4f}")

# Classification Report
print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        xgb_pred
    )
)

# Confusion Matrix
print("\nConfusion Matrix:\n")

print(
    confusion_matrix(
        y_test,
        xgb_pred
    )
)

# Save model
joblib.dump(
    xgb_model,
    'model/xgboost_model.pkl'
)

print("✅ XGBoost model saved!")

# =====================================================
# AUTOENCODER
# =====================================================

print("\nTraining Autoencoder...")

input_dim = X_train.shape[1]

# Input Layer
input_layer = Input(
    shape=(input_dim,)
)

# Encoder
encoded = Dense(
    32,
    activation='relu'
)(input_layer)

encoded = Dense(
    16,
    activation='relu'
)(encoded)

encoded = Dense(
    8,
    activation='relu'
)(encoded)

# Decoder
decoded = Dense(
    16,
    activation='relu'
)(encoded)

decoded = Dense(
    32,
    activation='relu'
)(decoded)

decoded = Dense(
    input_dim,
    activation='linear'
)(decoded)

# Build Model
autoencoder = Model(
    inputs=input_layer,
    outputs=decoded
)

# Compile
autoencoder.compile(
    optimizer='adam',
    loss='mse'
)

# =====================================================
# TRAIN ONLY ON NORMAL TRAFFIC
# =====================================================

X_normal = X_train[
    y_train == 0
]

# Early Stopping
early_stop = EarlyStopping(
    monitor='loss',
    patience=3,
    restore_best_weights=True
)

# Train
history = autoencoder.fit(
    X_normal,
    X_normal,
    epochs=20,
    batch_size=32,
    shuffle=True,
    callbacks=[early_stop],
    verbose=1
)

# =====================================================
# SAVE AUTOENCODER
# =====================================================

print("\nSaving Autoencoder...")

autoencoder.save(
    'model/autoencoder.h5'
)

print("✅ Autoencoder saved successfully!")

# =====================================================
# FINAL MESSAGE
# =====================================================

print("\n🎉 ALL MODELS TRAINED SUCCESSFULLY!")

print("\nSaved Files:")

print("✔ features.pkl")
print("✔ scaler.pkl")
print("✔ isolation_forest.pkl")
print("✔ xgboost_model.pkl")
print("✔ autoencoder.h5")