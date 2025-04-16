from uuid import UUID

import stripe
from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request
from models.invoice import Invoice, InvoiceBase, InvoiceStatusEnum
from models.user import User
from utils.config import settings, stripe_return_url
from utils.database.session import get_database
from utils.helpers.payment import find_or_create_vat
from utils.security.token import get_user

router = APIRouter(prefix="/invoice", tags=["Invoice"])


@router.get("/self/", response_model=list[InvoiceBase])
async def read_all(user: User = Depends(get_user)):
    if not user.customer:
        raise HTTPException(404, detail="No customer found.")

    return user.customer.invoices


@router.post("/pay/{uuid}", response_model=str)
async def pay(
    uuid: UUID, user: User = Depends(get_user), session=Depends(get_database)
):
    invoice = session.query(Invoice).filter_by(uuid=uuid).first()

    if not invoice or invoice.customer_uuid != user.customer_uuid:
        raise HTTPException(404, detail="Invoice not found.")

    if invoice.status == InvoiceStatusEnum.PAID:
        raise HTTPException(400, detail="Invoice already paid.")

    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": invoice.title or str(invoice.uuid),
                        "description": invoice.customer_product.product.description,
                        "images": [
                            invoice.customer_product.product.image_url
                            or "https://cdn.helpwave.de/logo.png"
                        ],
                        "metadata": {
                            "invoice": str(invoice.uuid),
                            "customer": str(invoice.customer.uuid),
                            "product": str(invoice.customer_product.product.uuid),
                            "product_plan": str(
                                invoice.customer_product.product_plan.uuid
                            ),
                        },
                    },
                    "unit_amount": int(invoice.total_amount * 100),
                },
                "quantity": 1,
                "tax_rates": [find_or_create_vat()],
            }
        ],
        customer_email=invoice.customer.email,
        mode="payment",
        ui_mode="embedded",
        return_url=stripe_return_url,
    )

    return session.client_secret


@router.post("/subscribe/{uuid}", response_model=str)
async def subscribe(
    uuid: UUID, user: User = Depends(get_user), session=Depends(get_database)
):
    invoice = session.query(Invoice).filter_by(uuid=uuid).first()

    if not invoice or invoice.customer_uuid != user.customer_uuid:
        raise HTTPException(404, detail="Invoice not found.")

    if invoice.status == InvoiceStatusEnum.PAID:
        raise HTTPException(400, detail="Invoice already paid.")

    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": invoice.title or str(invoice.uuid),
                        "description": invoice.customer_product.product.description,
                        "images": [
                            invoice.customer_product.product.image_url
                            or "https://cdn.helpwave.de/logo.png"
                        ],
                        "metadata": {
                            "invoice": str(invoice.uuid),
                            "customer": str(invoice.customer.uuid),
                            "product": str(invoice.customer_product.product.uuid),
                            "product_plan": str(
                                invoice.customer_product.product_plan.uuid
                            ),
                        },
                    },
                    "unit_amount": int(invoice.total_amount * 100),
                    "recurring": {
                        "interval": "month",
                        "interval_count": 1,
                    },
                },
                "quantity": 1,
                "tax_rates": [find_or_create_vat()],
            }
        ],
        mode="subscription",
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


@router.post("/webhook/")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None),
    session=Depends(get_database),
):
    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=stripe_signature,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

    if event["type"] == "checkout.session.completed":
        checkout_session = event["data"]["object"]

        session_id = checkout_session["id"]
        full_session = stripe.checkout.Session.retrieve(
            session_id, expand=["line_items.data.price.product"]
        )

        try:
            product_metadata = full_session["line_items"]["data"][0]["price"][
                "product"
            ]["metadata"]
            invoice_uuid = product_metadata.get("invoice")
            if not invoice_uuid:
                raise ValueError("Missing invoice UUID in metadata")
        except (KeyError, IndexError, ValueError) as e:
            raise HTTPException(
                status_code=400, detail=f"Metadata extraction failed: {str(e)}"
            )

        invoice = session.query(Invoice).filter_by(uuid=invoice_uuid).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        invoice.status = InvoiceStatusEnum.PAID
        session.commit()

    return {"status": "success"}
