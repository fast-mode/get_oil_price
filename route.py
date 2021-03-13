from fastapi import APIRouter
from . import crud

bp = APIRouter()

@bp.get("/ls")
def get_oil_price(city_name:str):
    return crud.get_oil_price(city_name)
    # return {'92#': '6.57', '95#': '6.98', '98#': '7.65', '0#': '6.20'}
