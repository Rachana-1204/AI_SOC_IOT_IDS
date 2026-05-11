import pandas as pd
import numpy as np

# Load raw CICIDS dataset
# Change filename if needed
raw_file = "data.csv"

# Read dataset
df = pd.read_csv(raw_file)

# Clean column names
df.columns = df.columns.str.strip()

# Replace infinity values
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Drop missing values
df.dropna(inplace=True)

# Convert labels to binary
# BENIGN = 0
# ATTACK = 1
if 'Label' in df.columns:
    df['Label'] = df['Label'].apply(
        lambda x: 0 if x == 'BENIGN' else 1
    )

# Best 20 Features
best_features = [
    'Flow Duration',
    'Total Fwd Packets',
    'Total Backward Packets',
    'Total Length of Fwd Packets',
    'Total Length of Bwd Packets',
    'Fwd Packet Length Max',
    'Fwd Packet Length Mean',
    'Bwd Packet Length Max',
    'Bwd Packet Length Mean',
    'Flow Bytes/s',
    'Flow Packets/s',
    'Flow IAT Mean',
    'Flow IAT Std',
    'Fwd IAT Total',
    'Bwd IAT Total',
    'SYN Flag Count',
    'ACK Flag Count',
    'Average Packet Size',
    'Avg Fwd Segment Size',
    'Avg Bwd Segment Size'
]

# Keep selected features + label
selected_columns = best_features + ['Label']
df = df[selected_columns]

# Reduce dataset size for faster training
if len(df) > 20000:
    df = df.sample(n=20000, random_state=42)

# Save cleaned dataset
df.to_csv("data.csv", index=False)

print("✅ Cleaned dataset created successfully!")
print(df.head())