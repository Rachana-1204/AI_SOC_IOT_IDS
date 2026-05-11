# utils.py

import pandas as pd
import numpy as np
import joblib
import shap
import re

from tensorflow.keras.models import load_model

# =====================================================
# LOAD TRAINED MODELS
# =====================================================

iso_model = joblib.load(
    'model/isolation_forest.pkl'
)

xgb_model = joblib.load(
    'model/xgboost_model.pkl'
)

scaler = joblib.load(
    'model/scaler.pkl'
)

feature_names = joblib.load(
    'model/features.pkl'
)

autoencoder = load_model(

    'model/autoencoder.h5',

    compile=False
)

# =====================================================
# SAFE DATA CLEANING
# =====================================================

def clean_input_data(data):

    # ---------------------------------------------
    # ADD MISSING FEATURES
    # ---------------------------------------------

    for col in feature_names:

        if col not in data.columns:

            data[col] = 0

    # ---------------------------------------------
    # KEEP ONLY TRAINED FEATURES
    # ---------------------------------------------

    data = data[feature_names]

    # ---------------------------------------------
    # CLEAN EACH COLUMN
    # ---------------------------------------------

    for col in data.columns:

        cleaned_column = []

        for value in data[col]:

            try:

                # Convert to string
                value = str(value)

                # Remove brackets/quotes/spaces
                value = re.sub(

                    r'[\[\]\'\"\s]',

                    '',

                    value
                )

                # Handle empty values
                if value == '':

                    value = 0

                # Convert scientific notation safely
                value = float(value)

            except:

                value = 0

            cleaned_column.append(value)

        data[col] = cleaned_column

    # ---------------------------------------------
    # REMOVE INF / NaN
    # ---------------------------------------------

    data = data.replace(

        [np.inf, -np.inf],

        0
    )

    data = data.fillna(0)

    return data

# =====================================================
# DETECT ANOMALY
# =====================================================

def detect_anomaly(data):

    # ---------------------------------------------
    # CLEAN INPUT
    # ---------------------------------------------

    data = clean_input_data(data)

    # ---------------------------------------------
    # SCALE DATA
    # ---------------------------------------------

    data_scaled = scaler.transform(data)

    # ---------------------------------------------
    # ISOLATION FOREST
    # ---------------------------------------------

    iso_pred = iso_model.predict(
        data_scaled
    )

    iso_pred = [

        1 if x == -1 else 0

        for x in iso_pred
    ]

    # ---------------------------------------------
    # XGBOOST
    # ---------------------------------------------

    xgb_pred = xgb_model.predict(
        data_scaled
    )

    xgb_pred = [

        int(x)

        for x in xgb_pred
    ]

    # ---------------------------------------------
    # AUTOENCODER
    # ---------------------------------------------

    reconstructed = autoencoder.predict(

        data_scaled,

        verbose=0
    )

    mse = np.mean(

        np.power(
            data_scaled - reconstructed,
            2
        ),

        axis=1
    )

    threshold = np.percentile(
        mse,
        85
    )

    ae_pred = [

        1 if error > threshold else 0

        for error in mse
    ]

    # ---------------------------------------------
    # MAJORITY VOTING
    # ---------------------------------------------

    final_predictions = []

    for i in range(len(data)):

        votes = (

            iso_pred[i]
            + xgb_pred[i]
            + ae_pred[i]
        )

        if votes >= 2:

            final_predictions.append(1)

        else:

            final_predictions.append(0)

    return final_predictions

# =====================================================
# SHAP EXPLANATION
# =====================================================

def explain_prediction(data):

    # ---------------------------------------------
    # CLEAN INPUT
    # ---------------------------------------------

    data = clean_input_data(data)

    # ---------------------------------------------
    # SCALE
    # ---------------------------------------------

    data_scaled = scaler.transform(data)

    # Use only first row for speed
    data_scaled = data_scaled[:1]

    # ---------------------------------------------
    # SHAP EXPLAINER
    # ---------------------------------------------

    explainer = shap.TreeExplainer(
        xgb_model
    )

    shap_values = explainer.shap_values(
        data_scaled
    )

    return shap_values

# =====================================================
# GENERATE SIMULATED IoT TRAFFIC
# =====================================================

def generate_live_traffic(num_samples=20):

    normal_data = np.random.normal(

        loc=0,
        scale=1,

        size=(
            int(num_samples * 0.6),
            len(feature_names)
        )
    )

    attack_data = np.random.normal(

        loc=8,
        scale=5,

        size=(
            int(num_samples * 0.4),
            len(feature_names)
        )
    )

    traffic = np.vstack([

        normal_data,
        attack_data
    ])

    df = pd.DataFrame(

        traffic,

        columns=feature_names
    )

    return df

# =====================================================
# ATTACK NAME GENERATOR
# =====================================================

def get_attack_name():

    attacks = [

        'DDoS Attack',
        'Botnet Activity',
        'Port Scan',
        'Brute Force',
        'Malware Traffic',
        'SQL Injection',
        'Ransomware Activity',
        'MITM Attack',
        'Credential Attack',
        'Suspicious IoT Traffic'
    ]

    return np.random.choice(attacks)

# =====================================================
# ATTACK EXPLANATION
# =====================================================

def get_attack_explanation():

    explanations = [

        'Abnormal packet size detected',

        'Suspicious SYN packet behavior identified',

        'High traffic frequency exceeded threshold',

        'Unusual protocol communication observed',

        'Malicious flow duration pattern detected',

        'Repeated unauthorized requests found',

        'Network behavior deviated from normal profile',

        'Anomaly score exceeded AI threshold',

        'Potential malware communication detected',

        'IoT device behavior appears compromised'
    ]

    return np.random.choice(explanations)