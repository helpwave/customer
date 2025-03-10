from datetime import datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models.customer import User
from models.customer_product import (
    CustomerProduct,
    CustomerProductBase,
    CustomerProductCreate,
)
from models.invoice import Invoice
from models.product import Product
from models.voucher import Voucher
from utils.database.session import get_database
from utils.security.token import get_user

router = APIRouter(prefix="/customer/product", tags=["CustomerProduct"])


@router.post("/", response_model=CustomerProductBase)
async def create(
    data: CustomerProductCreate,
    user: User = Depends(get_user),
    session=Depends(get_database),
):
    customer = user.customer

    if not customer:
        raise HTTPException(404, detail="Customer not found.")

    product = session.query(Product).filter_by(uuid=data.product_uuid).first()

    if not product:
        raise HTTPException(404, detail="Product not found.")

    if data.product_plan_uuid not in [plan.uuid for plan in product.plans]:
        raise HTTPException(404, detail="Plan does not exist on that product.")

    if data.voucher_uuid:
        voucher = (
            session.query(Voucher).filter_by(uuid=data.voucher_uuid).first()
        )

        if not voucher or not voucher.valid:
            raise HTTPException(404, detail="Voucher not valid.")

        voucher.redeemed_count += 1

    customer_product = CustomerProduct(
        customer_uuid=user.customer_uuid,
        product_uuid=data.product_uuid,
        product_plan_uuid=data.product_plan_uuid,
        voucher_uuid=data.voucher_uuid,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
    )

    invoice = Invoice(
        customer_uuid=user.customer.uuid, date=datetime.now(), total_amount=10
    )

    session.add(invoice)
    session.add(customer_product)
    session.commit()

    session.refresh(customer_product)

    return customer_product


@router.get("/{uuid}", response_model=CustomerProductBase)
async def read(
    uuid: UUID, user: User = Depends(get_user), session=Depends(get_database)
):
    customer_product = (
        session.query(CustomerProduct).filter_by(uuid=uuid).first()
    )

    if (
        not customer_product
        or customer_product.customer_uuid != user.customer_uuid
    ):
        raise HTTPException(status_code=404, detail="Product not found.")

    return customer_product


@router.get("/self/", response_model=list[CustomerProductBase])
async def read_all_by_customer(user: User = Depends(get_user)):
    if not user.customer:
        return []

    return user.customer.products


@router.delete("/{uuid}")
async def delete(
    uuid: UUID, user: User = Depends(get_user), session=Depends(get_database)
):
    customer_product = (
        session.query(CustomerProduct).filter_by(uuid=uuid).first()
    )

    if (
        not customer_product
        or customer_product.customer_uuid != user.customer_uuid
    ):
        raise HTTPException(status_code=404, detail="Product not found.")

    customer_product.cancellation_date = datetime.now()

    session.commit()
