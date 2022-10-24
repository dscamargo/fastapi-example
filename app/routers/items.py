import http
from datetime import datetime
from typing import Optional, Union, List
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from starlette.responses import Response


def find_item(element_id: str):
    selected = None
    for x in items:
        print(x, element_id)
        if x.id == element_id:
            selected = x
    return selected


class Item(BaseModel):
    id: Union[str, None] = None
    name: str
    price: float = Field(gt=0, description="Price must be greater than zero", title="Valor do produto")
    active: Union[bool, None] = True
    removed: Union[bool, None] = False
    created_at: Union[datetime, None] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "any-id",
                "name": "Produto 01",
                "price": 100.20,
                "active": True,
                "removed": True,
                "created_at": datetime.now()
            }
        }


items: List[Item] = []

router = APIRouter(
    prefix="/items",
    tags=["Item"]
)


@router.get(
    "/",
    response_model=List[Item],
    description="Retorna todos os items cadastrados"
)
def list_items():
    return items


@router.post(
    "/",
    response_model=Item,
    description="Realizar cadastro do item",
    responses={
        201: {"description": "Created", "model": Item},
    },
)
def create_item(item: Item, response: Response):
    item.id = str(uuid4())
    item.created_at = datetime.now()
    items.append(item)
    response.status_code = http.HTTPStatus.CREATED
    return item


@router.get(
    "/{item_id}",
    response_model=Optional[Item],
    description="Busca item pelo ID",
    responses={
        404: {"description": "Item não encontrado"}
    }
)
def show_item(item_id: str):
    item = find_item(item_id)
    if item is None:
        raise HTTPException(404, detail="Item não encontrado")
    return item
