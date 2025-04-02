from uuid import UUID

import stripe
from fastapi import APIRouter, Depends, HTTPException, Query

from models.invoice import Invoice, InvoiceBase
from models.user import User
from utils.config import stripe_return_url
from utils.database.session import get_database
from utils.security.token import get_user

router = APIRouter(prefix="/invoice", tags=["Invoice"])


@router.get("/self/", response_model=list[InvoiceBase])
async def read_all(user: User = Depends(get_user)):
    if not user.customer:
        raise HTTPException(404, detail="No customer found.")

    invoices = user.customer.invoices

    return invoices


@router.post("/pay/{uuid}", response_model=str)
async def pay(
    uuid: UUID, user: User = Depends(get_user), session=Depends(get_database)
):
    invoice = session.query(Invoice).filter_by(uuid=uuid).first()

    if not invoice or invoice.customer_uuid != user.customer_uuid:
        raise HTTPException(404, detail="Invoice not found.")

    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": str(invoice.uuid),
                    },
                    "unit_amount": invoice.total_amount,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        ui_mode="embedded",
        return_url=stripe_return_url,
    )

    return session.client_secret


@router.get("/status/")
async def get_payment_status(
    session_id: str = Query(..., description="Stripe Session ID")
):
    session = stripe.checkout.Session.retrieve(session_id)

    return {"status": session.payment_status, "session": session}
