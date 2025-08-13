from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    
    
class showBlog(Blog):
    class Config():
        orm_mode = True