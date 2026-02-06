import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

# ----------------------------
# Ensure models directory exists
# ----------------------------
os.makedirs("models", exist_ok=True)

# ----------------------------
# Generate realistic security event data
# Features:
# [login_hour, device_known, location_known, access_count, role_level]
# ----------------------------
np.random.seed(42)

normal_events = 800
anomalous_events = 200

# ---- Normal behavior (typical SME users) ----
normal_data = np.column_stack([
    np.random.randint(8, 20, normal_events),     # login during working hours
    np.ones(normal_events),                      # known device
    np.ones(normal_events),                      # known location
    np.random.randint(1, 10, normal_events),     # normal access count
    np.random.randint(1, 3, normal_events)       # low–mid privilege
])

# ---- Anomalous behavior (suspicious activity) ----
anomaly_data = np.column_stack([
    np.random.randint(0, 24, anomalous_events),  # unusual login time
    np.random.randint(0, 2, anomalous_events),   # unknown device
    np.random.randint(0, 2, anomalous_events),   # unknown location
    np.random.randint(20, 60, anomalous_events), # excessive access
    np.random.randint(2, 4, anomalous_events)    # high privilege
])

# Combine dataset
X = np.vstack([normal_data, anomaly_data])

# ----------------------------
# Train Isolation Forest model
# ----------------------------
model = IsolationForest(
    n_estimators=200,
    contamination=0.15,
    random_state=42
)

model.fit(X)

# ----------------------------
# Save ONLY the model (as requested)
# ----------------------------
joblib.dump(model, "models/isolation_forest.joblib")

print("✔ Isolation Forest model trained successfully")
print("✔ Model saved as models/isolation_forest.joblib")
print("✔ TrustLens AI model ready")
