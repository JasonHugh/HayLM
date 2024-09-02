from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated

class User(BaseModel):
    id: int = None
    name: Annotated[str, StringConstraints(min_length=3, max_length=10)]
    phone: Annotated[str, StringConstraints(pattern=r'^1\d{10}$')]
    SN: Annotated[str, StringConstraints(min_length=11, max_length=11)]
    password: str

if __name__ == "__main__":
    User.model_validate()