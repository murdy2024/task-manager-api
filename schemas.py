from pydantic import BaseModel
class Task(BaseModel):
    title: str
    completed: bool
class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    class config:
        from_attributes = True