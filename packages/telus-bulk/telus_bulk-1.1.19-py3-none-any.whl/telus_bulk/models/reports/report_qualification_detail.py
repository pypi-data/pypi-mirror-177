from typing import List, Optional, Any
from datetime import datetime
from fastapi_camelcase import CamelModel
from telus_bulk.models.reports import ReportAddress


class ReportQualification(CamelModel):
    csq_id: Optional[str] = None
    product_type: str
    created_at: Optional[datetime | str | Any] = None
    address: List[ReportAddress]
