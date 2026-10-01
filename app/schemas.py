from typing import List

from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Authentication
# ---------------------------------------------------------

class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=80
    )

    email: str

    password: str = Field(
        min_length=6,
        max_length=128
    )


class LoginRequest(BaseModel):

    email: str

    password: str


# ---------------------------------------------------------
# Home Planner
# ---------------------------------------------------------

class HomeRequest(BaseModel):

    budget: float = Field(gt=0)

    rooms: List[str] = []

    style: str = "Modern"

    items: List[str] = []

    priorities: str = "value for money"


# ---------------------------------------------------------
# Party Planner
# ---------------------------------------------------------

class PartyRequest(BaseModel):

    budget: float = Field(gt=0)

    guests: int = Field(
        gt=0,
        le=10000
    )

    event_type: str

    venue_city: str = ""

    food_preference: str = "mixed"

    decoration_style: str = "simple"

    priorities: str = "value for money"


# ---------------------------------------------------------
# Jewelry Planner
# ---------------------------------------------------------

class JewelryRequest(BaseModel):

    budget: float = Field(gt=0)

    occasion: str

    style: str = "Elegant"

    outfit_color: str = ""

    outfit_description: str = ""
