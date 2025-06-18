from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from price_analysis import market_price_estimation

app = FastAPI(title="Market Price Analysis API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MarketEstimation(BaseModel):
    product_name: str
    cost_price: int
    user_price: int


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Market Prices Estimation API!",
        "version": "1.0",
        "endpoints": {
            "/": "This welcome message",
            "/market-prices-estimation/": "POST endpoint for price analysis"
        }
    }


@app.post("/market-prices-estimation/")
async def market_prices_estimation_endpoint(request: MarketEstimation):
    try:
        response = market_price_estimation(request.product_name, request.cost_price, request.user_price)

        if not isinstance(response, dict):
            raise ValueError("market_price_estimation must return a dictionary")

        return JSONResponse(status_code=200, content=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))