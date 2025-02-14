from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("rf_fraud_detection.pkl")


@app.get("/")
def home():
    return {"message": "Fraud Detection API is running!"}

@app.post("/predict/")
def predict(transaction: dict):
    try:
 
        transaction_df = pd.DataFrame([transaction])

        expected_columns = model.feature_names_in_ 
        transaction_df = transaction_df[expected_columns]

        prediction = model.predict(transaction_df)[0]

        return {"fraud_detected": bool(prediction)}
    
    except Exception as e:
        return {"error": str(e)}