from pydantic import BaseModel, Field


class userAccount(BaseModel):
    user_fname:str
    user_lname:str
    user_email:str
    user_password:str
    user_phone:str
    is_admin:bool = Field(default=False)  # Default value for is_admin is set to False
    is_active:bool = Field(default=True)  # Default value for is_active is set to True
    is_super_user:bool = Field(default=False)  # Default value for is_super_user is set to False


class updateUserAccount(BaseModel):
    user_fname:str
    user_lname:str
    user_email:str
    user_password:str
    user_phone:str
    
class LoginUser(BaseModel):
    username: str
    user_password: str
