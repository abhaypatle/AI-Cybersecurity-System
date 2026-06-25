import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

data = pd.DataFrame({
    "traffic_rate": [10,20,30,40,500,15,22,35,600],
    "failed_logins": [0,1,0,2,50,0,1,1,60]
})

model = IsolationForest(contamination=0.2, random_state=42)
model.fit(data)

os.makedirs("../models", exist_ok=True)
joblib.dump(model, "../models/threat_model.pkl")

print("Model Saved Successfully")