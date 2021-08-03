from pydantic import BaseModel
import numpy as np
# class de parametrss bike
class Bike(BaseModel):
    hum_min: float
    hum_max: float
    hum_mean: float
    hum_q25: float
    hum_q50: float
    hum_q75: float

    windspeed_min: float
    windspeed_max: float
    windspeed_mean: float
    windspeed_q25: float
    windspeed_q50: float
    windspeed_q75: float

    temp_min: float
    temp_max: float
    temp_mean: float
    temp_q25: float
    temp_q50: float
    temp_q75: float

    atemp_min: float
    atemp_max: float
    atemp_mean: float
    atemp_q25: float
    atemp_q50: float
    atemp_q75: float

    clear: float
    cloudy: float
    rainy: float
    snowy: float

    cnt: float = 2729.0
    cnt_j_1: float = 1796.0
    cnt_j_2: float = 1341.0
    cnt_j_3: float = 3095.0
    cnt_j_4: float = 2114.0
    cnt_j_5: float = 441.0
    cnt_j_6: float = 1013.0
    cnt_j_7: float = 920.0


