import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

CSV_FILE = "data.csv"

class Employee(BaseModel):
    id: int
    name: str
    role: str
    department: str

@app.get("/")
def read_root():
    return{"Hello": "World"}

@app.get("/csv-data")
def get_csv_data():
    if not os.path.exists(CSV_FILE):
        raise HTTPException(status_code=404, detail="csv file not found")

    df = pd.read_CSV(CSV_FILE)
    return df.to_dict(oient="records")

@app.post("/csv-data")
def add_csv_data(employee: Employee):
    #prepare the new row
    new_data = pd.DataFrame([employee.model_dump()])

    if os.path.exists(CSV_FILE):
        new_data.to_CSV(CSV_FILE, mode="a", header=False,Index=False)
    else:
        new_data.to_csv(CSV_FILE, mode="w", header=True, index=False)

    return {"message": "Data added successfully","data": employee}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}



    

