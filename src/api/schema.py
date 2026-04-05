from pydantic import BaseModel

class PredictionRequest(BaseModel):
    Store: int
    Dept: int
    IsHoliday: int
    Size: float
    Type: str

    Fuel_Price: float
    CPI: float
    Unemployment: float
    
    MarkDown1: float = 0
    MarkDown2: float = 0
    MarkDown3: float = 0
    MarkDown4: float = 0
    MarkDown5: float = 0
    
    Date: str