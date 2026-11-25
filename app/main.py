from pathlib import Path
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MODEL_PATH = Path(__file__).parent / "model.joblib"
model = joblib.load(MODEL_PATH)

app = FastAPI(title="Iris Prediction API", version="1.0.0")

class IrisInput(BaseModel):
    sepal_length: float = Field(gt=0, example=5.1)
    sepal_width: float = Field(gt=0, example=3.5)
    petal_length: float = Field(gt=0, example=1.4)
    petal_width: float = Field(gt=0, example=0.2)

@app.get("/")
def root():
    return {"message": "Iris Data Science API is running"}

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
def predict(data: IrisInput):
    values = np.array([[data.sepal_length, data.sepal_width,
                        data.petal_length, data.petal_width]])
    prediction = int(model.predict(values)[0])
    names = ["setosa", "versicolor", "virginica"]
    probabilities = model.predict_proba(values)[0].tolist()
    return {
        "prediction": names[prediction],
        "class_id": prediction,
        "probabilities": {
            names[i]: round(float(probabilities[i]), 4)
            for i in range(len(names))
        }
    }
