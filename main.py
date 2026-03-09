from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {
        "status": "Success",
        "message": "Server Lumo running, create by Ha V. Tran (Tyranno)",
        "project": "Lumo Hub - STARTUP CHALLENGE 2026",
        "author": "Ha V. Tran (Tyranno)  "
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7001)