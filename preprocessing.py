import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

def load_and_preprocess(path):
    os.makedirs(MODEL_DIR, exist_ok=True)

    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    # ---------------- CLEAN ----------------
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    # ---------------- REMOVE DUPLICATES ----------------
    df.drop_duplicates(inplace=True)

    print("Dataset shape after cleaning:", df.shape)

    # ---------------- LABEL ENCODING ----------------
    if df['Label'].dtype == 'object':
        le = LabelEncoder()
        df['Label'] = le.fit_transform(df['Label'])
        joblib.dump(le, os.path.join(MODEL_DIR, "label_encoder.pkl"))

    # ---------------- REMOVE LEAKAGE ----------------
    drop_cols = ['Label']

    for col in df.columns:
        if 'label' in col.lower() or 'attack' in col.lower():
            drop_cols.append(col)

    X = df.drop(columns=list(set(drop_cols)), errors='ignore')

    # Keep only numeric
    X = X.select_dtypes(include=[np.number])

    y = df['Label']

    print("Features used:", X.shape[1])

    # ---------------- SCALING ----------------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))

    return X_scaled, y