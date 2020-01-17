"""
Author: Hugo
Date: 2020-01-17 23:14
Desc: 
"""

import uvicorn
from fastapi import FastAPI

app = FastAPI(debug=True)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=14000)