from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models.product import Product, ProductBase
from utils.database.session import get_database

router = APIRouter(prefix="/product", tags=["Product"])


@router.get("/", response_model=list[ProductBase])
async def read_all(session=Depends(get_database)):
    return session.query(Product).all()


@router.get("/{uuid}", response_model=ProductBase)
async def read(uuid: UUID, session=Depends(get_database)):
    product = session.query(Product).filter_by(uuid=uuid).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    return product
