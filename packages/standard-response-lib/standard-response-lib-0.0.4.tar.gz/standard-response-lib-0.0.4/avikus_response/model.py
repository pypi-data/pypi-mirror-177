from typing import Optional, Dict

from pydantic import BaseModel


class StandardResponse(BaseModel):
    code: int
    message: str
    result: Optional[Dict]
    detail: Optional[str]

    def __getitem__(self, item):
        return getattr(self, item)
