
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class CardBase(BaseModel):
    company_name: str
    slug: str
    google_review_link: str
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    payment_link: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    tiktok: Optional[str] = None
    theme_color: Optional[str] = "#2563EB"


class CardCreate(CardBase):
    pass


class CardUpdate(BaseModel):
    company_name: Optional[str] = None
    google_review_link: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    payment_link: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    tiktok: Optional[str] = None
    theme_color: Optional[str] = None


class CardPublic(BaseModel):
    id: int
    company_name: str
    slug: str
    google_review_link: str
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    payment_link: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    tiktok: Optional[str] = None
    theme_color: Optional[str] = "#2563EB"
    qr_url: Optional[str] = None

    class Config:
        orm_mode = True


class FeedbackCreate(BaseModel):
    satisfaction: bool
    comment: Optional[str] = None


class FeedbackOut(BaseModel):
    id: int
    satisfaction: bool
    comment: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class QuoteCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    message: Optional[str] = None


class QuoteOut(BaseModel):
    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    message: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
