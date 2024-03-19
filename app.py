from fastapi import FastAPI, HTTPException
import random
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/hello")
async def say_hello(name):
    return {"message": "Hello, " + name + "! 👋"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")