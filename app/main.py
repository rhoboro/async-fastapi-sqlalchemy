from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.main import router as api_router

app = FastAPI(title="async-fastapi-sqlalchemy")

app.include_router(api_router, prefix="/api")


@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
