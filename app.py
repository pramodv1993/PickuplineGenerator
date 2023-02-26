from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return { "Pickupline Generator": "Welcome to Pickup line generator" }