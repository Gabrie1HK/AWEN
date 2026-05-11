from fastapi import FastAPI

app = FastAPI(title = "AWEN")

@app.get("/")
def root():
    return {"aló es casi mi nombre"}

