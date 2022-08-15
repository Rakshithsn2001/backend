import string
from unicodedata import numeric
from click import option
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional
from sqlalchemy import Integer


class userCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: str


class userOut(userCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class tokenData(BaseModel):
    id: Optional[str] = None


class tokenOut(BaseModel):
    access_token: str
    token_type: str


class userCollect(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr
    phone_number: str


class userCollectOut(userCollect):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class user_location_data_in(BaseModel):
    latitude: str
    longitude: str
    address: str


class user_location_data_out(user_location_data_in):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class dac_out(BaseModel):
    owner_id: int
    phone_number: str
    digital_access_code: str
    created_at: datetime

    class Config:
        orm_mode = True


class user_data_out(userOut):
    user_data: userCollectOut
    user_location_data: user_location_data_out
    user_digital_access_code: dac_out

    class Config:
        orm_mode = True


class user_data_location_dac_out(BaseModel):
    user_location_data: user_location_data_out
    user_digital_access_code: dac_out

    class Config:
        orm_mode = True
