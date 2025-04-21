from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models.customer_product import CustomerProduct
from models.product import Product, ProductBase
from models.user import User
from utils.database.session import get_database
from utils.security.token import get_user

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


@router.get("/available/", response_model=list[ProductBase])
async def available(user: User = Depends(get_user),
                    session=Depends(get_database)):

    if not user.customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not created yet.")

    booked_product_uuids = session.query(CustomerProduct.product_uuid).filter(
        CustomerProduct.customer_uuid == user.customer_uuid).subquery()
    available_products = session.query(Product).filter(
        ~Product.uuid.in_(booked_product_uuids)).all()

    return available_products
