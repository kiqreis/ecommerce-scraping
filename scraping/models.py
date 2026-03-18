from datetime import datetime, timezone
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ProductInfo:
    product_name: str
    price: Optional[int]
    category: str
    url: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
