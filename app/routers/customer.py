from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from models.customer import (
    Customer,
    CustomerBase,
    CustomerCreate,
    CustomerUpdate,
)
from utils.database.session import get_database

router = APIRouter(prefix="/customer", tags=["Customer"])


@router.put("/", response_model=CustomerBase)
async def create(data: CustomerCreate, session=Depends(get_database)):
    customer = Customer(
        name=data.name,
        email=data.email,
        website_url=data.website_url,
        address=data.address,
        house_number=data.house_number,
        care_of=data.care_of,
        postal_code=data.postal_code,
        city=data.city,
        country=data.country,
    )

    session.add(customer)
    session.commit()

    session.refresh(customer)

    return customer


@router.get("/{uuid}", response_model=CustomerBase)
async def read(uuid: UUID, session=Depends(get_database)):
    customer = session.query(Customer).filter_by(uuid=uuid).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")

    return customer


@router.post("/", response_model=CustomerBase)
async def update(data: CustomerUpdate, session=Depends(get_database)):
    customer = session.query(Customer).filter_by(uuid=data.uuid).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")

    customer.name = data.name
    customer.email = data.email
    customer.website_url = data.website_url
    customer.address = data.address
    customer.house_number = data.house_number
    customer.care_of = data.care_of
    customer.postal_code = data.postal_code
    customer.city = data.city
    customer.country = data.country

    session.commit()
    session.refresh(customer)

    return customer


@router.delete("/{uuid}")
async def delete(uuid: UUID, session=Depends(get_database)):
    customer = session.query(Customer).filter_by(uuid=uuid).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")

    session.delete(customer)
    session.commit()
