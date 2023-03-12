from pydantic import BaseModel

class AuthorBase(BaseModel):
    '''
        Tweet's authors in Database.
    '''
    id: str
    username: str
    image_url: str

class UserBase(AuthorBase):
    '''
        Candidate users.
    '''
    last_update: str 

class UserDisplay(BaseModel):
    # id: str
    username: str
    # image_url: str

    class Config:
        orm_mode = True