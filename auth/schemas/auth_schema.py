from sqlmodel import SQLModel
from pydantic import EmailStr

class UserRegister(SQLModel):
    username:str
    email: EmailStr
    password:str

class UserLogin(SQLModel):
    email: EmailStr
    password:str

    