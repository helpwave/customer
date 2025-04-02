import logging
from datetime import datetime, timedelta

from models.contract import Contract
from models.product import Product
from models.product_contract import ProductContract
from models.product_plan import ProductPlan
from models.static import ContractKeyEnum, PlanTypeEnum
from models.voucher import Voucher
from utils.database.connection import SessionLocal


def create_example_data():
    session = SessionLocal()

    if not session.query(Product).first():
        logging.info("Initializing app with example data set")

        product = Product(
            name="App Zum Doc",
            description="Kommunizieren Sie mit Ihren Patienten!",
        )
        session.add(product)
        session.commit()
        session.refresh(product)

        plan1 = ProductPlan(
            product_uuid=product.uuid,
            type=PlanTypeEnum.RECURRING,
            recurring_month=1,
            cost_euro=199.99,
        )
        plan2 = ProductPlan(
            product_uuid=product.uuid,
            type=PlanTypeEnum.RECURRING,
            recurring_month=12,
            cost_euro=1999.99,
        )

        session.add(plan1)
        session.add(plan2)
        session.commit()
        session.refresh(plan1)
        session.refresh(plan2)

        now = datetime.now()

        voucher = Voucher(
            code="TEST10",
            description="Free for you! <3",
            product_plan_uuid=plan1.uuid,
            discount_percentage=100,
            valid_from=now,
            valid_until=now + timedelta(days=7),
            max_redemptions=2,
        )
        session.add(voucher)
        session.commit()

        contract = Contract(
            key=ContractKeyEnum.AGB_APP_ZUM_DOC,
            version="b60cf20350af5d0f8c037aac3267c9a2593f99cd",
            url="https://cdn.legal.helpwave.de/main/agb_app_zum_doc.pdf",
        )

        session.add(contract)
        session.commit()
        session.refresh(contract)

        product_contract = ProductContract(
            product_uuid=product.uuid, contract_uuid=contract.uuid
        )

        session.add(product_contract)
        session.commit()
