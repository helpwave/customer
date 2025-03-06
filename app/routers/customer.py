from fastapi import APIRouter, Depends, HTTPException

from models.customer import (
    Customer,
    CustomerBase,
    CustomerCreate,
    CustomerUpdate,
    User,
)
from models.static import RoleEnum
from utils.database.session import get_database
from utils.security.token import get_user

router = APIRouter(prefix="/customer", tags=["Customer"])


@router.post("/", response_model=CustomerBase)
async def create(
    data: CustomerCreate,
    user: User = Depends(get_user),
    session=Depends(get_database),
):
    if user.customer:
        raise HTTPException(400, detail="User already created a Customer.")

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

    user.customer_uuid = customer.uuid
    user.role = RoleEnum.ADMIN
    session.commit()

    return customer


@router.get("/", response_model=CustomerBase)
async def read(user: User = Depends(get_user)):
    customer = user.customer

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")

    return customer


@router.put("/", response_model=CustomerBase)
async def update(
    data: CustomerUpdate,
    user: User = Depends(get_user),
    session=Depends(get_database),
):
    customer = user.customer

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
