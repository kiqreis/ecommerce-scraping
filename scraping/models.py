import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ProductInfo:
    product_name: str
    price: Optional[int]
    category: str
    url: str
    timestamp: str = field(default_factory=lambda: time.strftime("%d-%m-%Y %H:%M:%S"))
