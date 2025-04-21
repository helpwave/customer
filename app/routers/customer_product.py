from datetime import datetime
from uuid import UUID

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Body, Depends, HTTPException

from models.customer import User
from models.customer_product import (
    CustomerProduct,
    CustomerProductBase,
    CustomerProductCalculation,
    CustomerProductCalculationRequest,
    CustomerProductCreate,
    CustomerProductsCalculation,
    ExtendedCustomerProductBase,
    ProductCalculationResult,
)
from models.customer_product_contract import CustomerProductContract
from models.invoice import Invoice
from models.product import Product
from models.product_contract import ProductContract
from models.product_plan import ProductPlan
from models.static import PlanTypeEnum
from models.voucher import Voucher
from utils.calculation.pricing import (
    calculate_full_pricing_in_euro,
    calculate_pricing_in_euro,
)
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

    if session.query(CustomerProduct.uuid).filter_by(
            product_uuid=product.uuid).first():
        raise HTTPException(400, detail="Product already booked.")

    product_plan = None

    for plan in product.plans:
        if plan.uuid != data.product_plan_uuid:
            continue

        product_plan = plan
        break

    if not product_plan:
        raise HTTPException(404, detail="Plan does not exist on that product.")

    voucher = None

    if data.voucher_uuid:
        voucher = session.query(Voucher).filter_by(
            uuid=data.voucher_uuid).first()

        if not voucher or not voucher.valid or voucher.product_plan != product_plan.uuid:
            raise HTTPException(404, detail="Voucher not valid.")

        voucher.redeemed_count += 1

    required_contract_uuids = set(
        row[0]
        for row in session.query(ProductContract.contract_uuid)
        .filter_by(product_uuid=product.uuid)
        .all()
    )
    accepted_contracts = set(data.accepted_contracts)

    if not required_contract_uuids.issubset(accepted_contracts):
        missing_contracts = required_contract_uuids - set(accepted_contracts)
        raise HTTPException(
            400,
            detail=f"Not all contracts accepted. Missing: {
                ", ".join(
                    map(
                        str,
                        missing_contracts))}",
        )

    customer_product = CustomerProduct(
        customer_uuid=user.customer.uuid,
        product_uuid=data.product_uuid,
        product_plan_uuid=data.product_plan_uuid,
        voucher_uuid=data.voucher_uuid,
        start_date=datetime.now(),
        end_date=(
            datetime.now() + relativedelta(months=+product_plan.recurring_month)
            if product_plan.type == PlanTypeEnum.RECURRING
            else None
        ),
    )

    session.add(customer_product)
    session.commit()
    session.refresh(customer_product)

    for required_contract_uuid in required_contract_uuids:
        customer_product_contract = CustomerProductContract(
            product_customer_uuid=customer_product.uuid,
            contract_uuid=required_contract_uuid,
        )
        session.add(customer_product_contract)

    invoice = Invoice(
        customer_uuid=user.customer.uuid,
        customer_product_uuid=customer_product.uuid,
        title=f"{product.name} ({product_plan.name})",
        date=datetime.now(),
        total_amount=calculate_pricing_in_euro(product_plan, voucher),
    )

    session.add(invoice)
    session.commit()

    return customer_product


@router.get("/{uuid}", response_model=CustomerProductBase)
async def read(
    uuid: UUID, user: User = Depends(get_user), session=Depends(get_database)
):
    customer_product = session.query(
        CustomerProduct).filter_by(uuid=uuid).first()

    if not customer_product or customer_product.customer_uuid != user.customer_uuid:
        raise HTTPException(status_code=404, detail="Product not found.")

    return customer_product


@router.get("/self/", response_model=list[ExtendedCustomerProductBase])
async def read_all_by_customer(user: User = Depends(get_user)):
    if not user.customer:
        return []

    return user.customer.products


@router.post("/calculate/", response_model=CustomerProductsCalculation)
async def calculate(
    products: list[CustomerProductCalculationRequest] = Body(
        ...,
        description="List of product calculation requests. Each must have a unique product_uuid."
    ),
    session=Depends(get_database)
):
    seen_uuids = set()
    product_results: list[ProductCalculationResult] = []
    total_final_price = 0
    total_before_price = 0
    total_saving = 0

    for request_data in products:
        product_uuid = request_data.product_uuid

        if product_uuid in seen_uuids:
            raise HTTPException(
                status_code=400,
                detail=f"Duplicate product_uuid: {product_uuid}")
        seen_uuids.add(product_uuid)

        product = session.query(Product).filter_by(uuid=product_uuid).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found.")

        plan = session.query(ProductPlan).filter_by(
            uuid=request_data.product_plan_uuid).first()
        if not plan or plan.product.uuid != product.uuid:
            raise HTTPException(status_code=404,
                                detail="Plan does not exist on that product.")

        voucher = None
        if request_data.voucher_uuid:
            voucher = session.query(Voucher).filter_by(
                uuid=request_data.voucher_uuid).first()
            if not voucher or not voucher.valid or voucher.product_plan != plan.uuid:
                raise HTTPException(
                    status_code=404, detail="Voucher not valid.")

        final_price, before_price = calculate_full_pricing_in_euro(
            plan, voucher)
        saving = before_price - final_price

        total_final_price += final_price
        total_before_price += before_price
        total_saving += saving

        product_results.append(ProductCalculationResult(
            product_uuid=product_uuid,
            calculation=CustomerProductCalculation(
                final_price=final_price,
                before_price=before_price,
                saving=saving
            )
        ))

    return CustomerProductsCalculation(
        overall=CustomerProductCalculation(
            final_price=total_final_price,
            before_price=total_before_price,
            saving=total_saving
        ),
        products=product_results
    )


@router.delete("/{uuid}")
async def delete(
    uuid: UUID, user: User = Depends(get_user), session=Depends(get_database)
):
    customer_product = session.query(
        CustomerProduct).filter_by(uuid=uuid).first()

    if not customer_product or customer_product.customer_uuid != user.customer_uuid:
        raise HTTPException(status_code=404, detail="Product not found.")

    customer_product.cancellation_date = datetime.now()

    session.commit()
