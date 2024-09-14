from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role: str
    phone_number: str
    dob: Optional[date] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = False
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class UserRead(BaseModel):
    userID: int
    first_name: str
    last_name: str
    email: str
    role: str
    phone_number: str
    dob: Optional[date]
    street_address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[str]
    country: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True

class PortfolioCreate(BaseModel):
    userID: int
    name: str

class PortfolioRead(BaseModel):
    portfolioID: int
    userID: int
    name: str
    created_at: str

    class Config:
        orm_mode = True

class AssetCreate(BaseModel):
    name: str
    type: str
    value: float

class AssetRead(BaseModel):
    assetID: int
    name: str
    type: str
    value: float
    created_at: str

    class Config:
        orm_mode = True

class InvestmentCreate(BaseModel):
    portfolioID: int
    assetID: int
    amount: float
    investment_date: date

class InvestmentRead(BaseModel):
    investmentID: int
    portfolioID: int
    assetID: int
    amount: float
    investment_date: date

    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    userID: int
    amount: float
    description: Optional[str] = None

class TransactionRead(BaseModel):
    transactionID: int
    userID: int
    amount: float
    transaction_date: str
    description: Optional[str]

    class Config:
        orm_mode = True

class BrokerCreate(BaseModel):
    name: str
    contact_info: Optional[str] = None

class BrokerRead(BaseModel):
    brokerID: int
    name: str
    contact_info: Optional[str]
    created_at: str

    class Config:
        orm_mode = True
