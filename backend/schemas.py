from pydantic import BaseModel

class LogCreate(BaseModel):
    title: str
    content: str

class LogResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True
