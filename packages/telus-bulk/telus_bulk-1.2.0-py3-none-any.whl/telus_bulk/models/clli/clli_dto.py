from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic import Field


class Clli(CamelModel):
    city: Optional[str] = Field(default=None)
    province: Optional[str] = Field(default=None)
    clli: Optional[str] = Field(default=None)
    distance: Optional[str] = Field(default=None)
