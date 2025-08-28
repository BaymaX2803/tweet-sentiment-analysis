from pydantic import BaseModel

class Tweet(BaseModel):
    text: str
    model: str # Added model field to specify which LLM to use