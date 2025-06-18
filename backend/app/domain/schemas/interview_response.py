from pydantic import BaseModel

from ..entities.interview import Interview


class InterviewResponse(BaseModel, Interview):
    @staticmethod
    def from_entity(cls, entity: Interview) -> "InterviewResponse":
        return cls(**entity.__dict__)
