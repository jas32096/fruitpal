import typing
import sqlite3
from decimal import Decimal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class CostResponseItem(BaseModel):
    COUNTRY: str = Field(..., min_length=2, max_length=2)
    TOTAL_COST: str = Field(..., regex=r'^\d+(\.?\d+)?$')
    FIXED_OVERHEAD: str = Field(..., regex=r'^\d+(\.?\d+)?$')
    VARIABLE_COST: str = Field(..., regex=r'^\d+(\.?\d+)?$')

    class Config:
        schema_extra = {
            "example": {
                "COUNTRY": "MX",
                "TOTAL_COST": "21999.20",
                "FIXED_OVERHEAD": "32.00",
                "VARIABLE_COST": "54.24"
            }
        }


@app.get('/', response_model=typing.List[CostResponseItem])
def costs(commodity: str, price: Decimal, tons: Decimal):
    con = sqlite3.connect('data.db')
    con.row_factory = sqlite3.Row
    cur = con.execute('SELECT * FROM commodities WHERE commodity = ?', (commodity,))

    return sorted([
        {
            'COUNTRY': row['COUNTRY'],
            'TOTAL_COST': str(tons * (variable_cost := price + Decimal(row['VARIABLE_COST'])) + Decimal(row['FIXED_OVERHEAD'])),
            'FIXED_OVERHEAD': row['FIXED_OVERHEAD'],
            'VARIABLE_COST': str(variable_cost)
        }
    for row in cur], key=lambda x: x['TOTAL_COST'], reverse=True)
