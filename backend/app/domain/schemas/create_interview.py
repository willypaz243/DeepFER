from datetime import datetime

from pydantic import BaseModel, Field


class CreateInterview(BaseModel):
    title: str = Field(
        ...,
        examples=["My Interview"],
        description="The title of the interview",
    )
    descrption: str = Field(
        ...,
        examples=["This is a great interview!"],
        description="A short description of the interview",
    )
    start_time: int = Field(
        ...,
        examples=[datetime(2025, 1, 3, 9, 30, 0)],
        description="The Unix timestamp for when the interview should start",
    )
    duration: int = Field(
        ...,
        examples=[60],
        description="The duration of the interview in minutes",
    )
