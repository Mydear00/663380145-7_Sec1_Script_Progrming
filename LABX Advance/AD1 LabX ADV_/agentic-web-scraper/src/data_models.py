from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Product:
    """Represents one scraped product."""

    name: str
    price: str
    description: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert this product into a dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """Create a product from a dictionary."""
        return cls(**data)