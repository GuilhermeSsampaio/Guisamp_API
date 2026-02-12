from pydantic import EmailStr, BaseModel, ConfigDict

class UserRegister(BaseModel):
    username:str
    email: EmailStr
    password:str

class UserLogin(BaseModel):
    email: EmailStr
    password:str


    