from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CoffeeInput(BaseModel):
    coffee_weight: float
    ratio: float


class PourStage(BaseModel):
    name: str
    water_amount: float
    cumulative_water: float
    time: str
    instruction: str


class CoffeeOutput(BaseModel):
    coffee_weight: float
    ratio: float
    total_water: float
    stages: list[PourStage]


@app.post("/")
def calculate(data: CoffeeInput) -> CoffeeOutput:
    total_water = data.coffee_weight * data.ratio

    # 闷蒸 15%，三段各 28.33%
    bloom_pct = 0.15
    pour_pct = 0.2833

    bloom_water = round(total_water * bloom_pct, 1)
    pour1_water = round(total_water * pour_pct, 1)
    pour2_water = round(total_water * pour_pct, 1)
    pour3_water = round(total_water - bloom_water - pour1_water - pour2_water, 1)

    stages = [
        PourStage(
            name="闷蒸",
            water_amount=bloom_water,
            cumulative_water=bloom_water,
            time="0:00 - 0:30",
            instruction=f"从中心向外画圈注水 {bloom_water}g，确保咖啡粉均匀湿润，等待排气"
        ),
        PourStage(
            name="第一段注水",
            water_amount=pour1_water,
            cumulative_water=round(bloom_water + pour1_water, 1),
            time="0:30 - 1:00",
            instruction=f"从中心向外缓慢画圈注水 {pour1_water}g，保持稳定水流"
        ),
        PourStage(
            name="第二段注水",
            water_amount=pour2_water,
            cumulative_water=round(bloom_water + pour1_water + pour2_water, 1),
            time="1:00 - 1:30",
            instruction=f"继续画圈注水 {pour2_water}g，保持水位稳定"
        ),
        PourStage(
            name="第三段注水",
            water_amount=pour3_water,
            cumulative_water=round(total_water, 1),
            time="1:30 - 2:00",
            instruction=f"最后注入 {pour3_water}g，完成萃取，等待滴滤完成"
        ),
    ]

    return CoffeeOutput(
        coffee_weight=data.coffee_weight,
        ratio=data.ratio,
        total_water=round(total_water, 1),
        stages=stages
    )
