import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import matplotlib.pyplot as plt

# === Step 2: Load Your Engineered Dataset ===
data_path = "archive/UNSW_NB15_engineered_minimal.csv"
df = pd.read_csv(data_path)

# === Step: Encode All Categorical Columns ===
label_encoder = LabelEncoder()

# Identify columns with string values (excluding 'label' and others we don't want to encode)
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

# Apply label encoding to each categorical column
for col in categorical_cols:
    if col != 'label':  # Exclude the label column
        df[col] = label_encoder.fit_transform(df[col])

# === Step 3: Prepare Features & Labels ===
X = df.drop(columns=['label', 'id', '    id', 'attack_cat'], errors='ignore')
y = df['label']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# === Step 4: Train the Model ===
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# === Step 5: Evaluate the Model ===
y_pred = model.predict(X_test)
print("🎯 Accuracy:", accuracy_score(y_test, y_pred))
print("📊 Classification Report:\n", classification_report(y_test, y_pred))

# === Step 6: Save the Model ===
joblib.dump(model, 'rf_model_minimal_features.pkl')
print("💾 Model saved as rf_model_minimal_features.pkl")

# === Step 7: Visualize Feature Importances ===
importances = model.feature_importances_
features = X.columns
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(12, 6))
plt.title("Feature Importances")
plt.bar(range(len(importances)), importances[indices])
plt.xticks(range(len(importances)), [features[i] for i in indices], rotation=90)
plt.tight_layout()
plt.show()
