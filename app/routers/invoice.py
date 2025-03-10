from uuid import UUID

import stripe
from fastapi import APIRouter, Depends, HTTPException, Query

from models.invoice import Invoice, InvoiceBase
from models.user import User
from utils.config import settings
from utils.database.session import get_database
from utils.security.token import get_user

router = APIRouter(prefix="/invoice", tags=["Invoice"])


@router.get("/self", response_model=list[InvoiceBase])
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
                    "currency": "usd",
                    "product_data": {
                        "name": "T-shirt",
                    },
                    "unit_amount": 2000,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=settings.EXTERNAL_URL
        + "/invoice/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=settings.EXTERNAL_URL
        + "/invoice/cancel?session_id={CHECKOUT_SESSION_ID}",
    )

    return session.url


@router.get("/success")
async def get_payment_status(
    session_id: str = Query(..., description="Stripe Session ID")
):
    session = stripe.checkout.Session.retrieve(session_id)
    print(session)
    return {"status": session.payment_status, "session": session}
