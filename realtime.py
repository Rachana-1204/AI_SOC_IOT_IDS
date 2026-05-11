import pandas as pd
import time

from utils import detect_anomaly

print("🚀 Starting Real-Time Detection...\n")

# Load data
df = pd.read_csv("data.csv")

# Remove label column
X = df.drop('Label', axis=1)

# Shuffle rows
X = X.sample(frac=1).reset_index(drop=True)

for i in range(len(X)):

    row = X.iloc[i:i+1]

    prediction = detect_anomaly(row)[0]

    if prediction == 1:
        print(f"⚠️ ALERT: Anomaly detected at row {i}")
    else:
        print(f"✅ Normal traffic at row {i}")

    time.sleep(1)