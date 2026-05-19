import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI(title="Employee CSV API")

CSV_FILE = "data.csv"


# Schema for adding new data via POST
class Employee(BaseModel):
    id: int
    name: str
    role: str
    department: str


@app.get("/")
def read_root():
    return {
        "message": "FastAPI CSV API is running"
    }


# GET Method: Read CSV data
@app.get("/csv-data")
def get_csv_data():

    if not os.path.exists(CSV_FILE):
        return {
            "message": "CSV file not found",
            "data": []
        }

    try:
        df = pd.read_csv(CSV_FILE)

        return {
            "count": len(df),
            "data": df.to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# POST Method: Add new employee data
@app.post("/csv-data")
def add_csv_data(employee: Employee):

    try:
        # Convert incoming JSON to DataFrame
        new_data = pd.DataFrame([employee.model_dump()])

        # Append or create CSV
        if os.path.exists(CSV_FILE):

            new_data.to_csv(
                CSV_FILE,
                mode="a",
                header=False,
                index=False
            )

        else:

            new_data.to_csv(
                CSV_FILE,
                mode="w",
                header=True,
                index=False
            )

        return {
            "message": "Data added successfully",
            "data": employee
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )