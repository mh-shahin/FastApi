from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    
     
class showBlog(Blog):
    class Config():
        orm_mode = True
        
class User(BaseModel):
    name: str
    email: str
    password: str
    
    
class Login(BaseModel):
    username: str
    password: str
    