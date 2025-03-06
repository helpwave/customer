from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from models.customer import Customer
from models.customer_product import (
    CustomerProduct,
    CustomerProductBase,
    CustomerProductCreate,
)
from models.product import Product
from utils.database.session import get_database

router = APIRouter(prefix="/customer/product", tags=["CustomerProduct"])


@router.put("/", response_model=CustomerProductBase)
async def create(data: CustomerProductCreate, session=Depends(get_database)):
    customer = (
        session.query(Customer).filter_by(uuid=data.customer_uuid).first()
    )

    if not customer:
        # TODO check customer permissions of user
        raise HTTPException(404, detail="Customer not found.")

    product = session.query(Product).filter_by(uuid=data.product_uuid).first()

    if not product:
        raise HTTPException(404, detail="Product not found.")

    if data.product_plan_uuid not in [plan.uuid for plan in product.plans]:
        raise HTTPException(404, detail="Plan does not exist on that product.")

    customer_product = CustomerProduct(
        customer_uuid=data.customer_uuid,  # TODO replace it with current user customer
        product_uuid=data.product_uuid,
        product_plan=data.product_plan_uuid,
    )

    session.add(customer_product)
    session.commit()

    session.refresh(customer_product)

    return customer_product


@router.get("/{uuid}", response_model=CustomerProductBase)
async def read(uuid: UUID, session=Depends(get_database)):
    customer_product = (
        session.query(CustomerProduct).filter_by(uuid=uuid).first()
    )

    if not customer_product:
        raise HTTPException(status_code=404, detail="Product not found.")

    return customer_product


@router.get("/by/{uuid}", response_model=list[CustomerProductBase])
async def read_all_by_customer(uuid: UUID, session=Depends(get_database)):
    customer_products = (
        session.query(CustomerProduct).filter_by(customer_uuid=uuid).all()
    )

    # TODO check permission on customer id

    return customer_products


@router.delete("/{uuid}")
async def delete(uuid: UUID, session=Depends(get_database)):
    customer_product = (
        session.query(CustomerProduct).filter_by(uuid=uuid).first()
    )

    if not customer_product:
        raise HTTPException(status_code=404, detail="Product not found.")

    customer_product.cancellation_date = datetime.now()

    session.commit()
