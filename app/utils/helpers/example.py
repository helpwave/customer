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

        product_azd = Product(
            name="App Zum Doc",
            description="Kommunizieren Sie mit Ihren Patienten!",
            image_url="https://app-zum-doc.de/images/appzumdoc_20222.png",
        )

        product_netzmanager = Product(
            name="mediQuu Netzmanager",
            description="Verwaltungstool für Arztnetze und Praxisverbunde.",
            image_url="https://login.mediquu.de/assets/images/mediquu_logo_2022.png",
        )

        product_viva = Product(
            name="mediQuu viva",
            description="Die Patientenakte für Zusatzleistungen (iSd. SGB V §140a) synchronisiert mit allen teilnehmenden Praxen.",
        )

        session.add(product_azd)
        session.add(product_netzmanager)
        session.add(product_viva)
        session.commit()
        session.refresh(product_azd)
        session.refresh(product_netzmanager)
        session.refresh(product_viva)

        azd_plan1 = ProductPlan(
            product_uuid=product_azd.uuid,
            name="monatlich",
            type=PlanTypeEnum.RECURRING,
            recurring_month=1,
            cost_euro=199.99,
        )
        azd_plan2 = ProductPlan(
            product_uuid=product_azd.uuid,
            name="jährlich",
            type=PlanTypeEnum.RECURRING,
            recurring_month=12,
            cost_euro=1999.99,
        )

        netzmanager_plan1 = ProductPlan(
            product_uuid=product_netzmanager.uuid,
            name="jährlich",
            type=PlanTypeEnum.RECURRING,
            recurring_month=12,
            cost_euro=17040.00,
        )

        viva_plan1 = ProductPlan(
            product_uuid=product_viva.uuid,
            name="monatlich",
            type=PlanTypeEnum.RECURRING,
            recurring_month=1,
            cost_euro=800.00,
        )
        viva_plan2 = ProductPlan(
            product_uuid=product_viva.uuid,
            name="Analytics monatlich",
            type=PlanTypeEnum.RECURRING,
            recurring_month=1,
            cost_euro=1200.00,
        )

        session.add(azd_plan1)
        session.add(azd_plan2)
        session.add(netzmanager_plan1)
        session.add(viva_plan1)
        session.add(viva_plan2)
        session.commit()
        session.refresh(azd_plan1)
        session.refresh(azd_plan2)
        session.refresh(netzmanager_plan1)
        session.refresh(viva_plan1)
        session.refresh(viva_plan2)

        now = datetime.now()

        voucher = Voucher(
            code="TEST10",
            description="Free for you! <3",
            product_plan_uuid=azd_plan1.uuid,
            discount_percentage=100,
            valid_from=now,
            valid_until=now + timedelta(days=7),
            max_redemptions=2,
        )
        session.add(voucher)
        session.commit()

        version = "0460675bb237984e211344881df9f611cde2ff74"

        contract_agb_azd = Contract(
            key=ContractKeyEnum.AGB_APP_ZUM_DOC,
            version=version,
            url=f"https://cdn.legal.helpwave.de/{version}/agb_app_zum_doc.pdf",
        )

        contract_avv_global = Contract(
            key=ContractKeyEnum.AVV,
            version=version,
            url=f"https://cdn.legal.helpwave.de/{version}/avv.pdf",
        )

        contract_sub_global = Contract(
            key=ContractKeyEnum.SUB,
            version=version,
            url=f"https://cdn.legal.helpwave.de/{version}/sub.pdf",
        )

        contract_agb_netzmanager = Contract(
            key=ContractKeyEnum.AGB_MEDIQUU_NETZMANAGER,
            version=version,
            url=f"https://cdn.legal.helpwave.de/{version}/agb_netzmanager.pdf",
        )

        session.add(contract_agb_azd)
        session.add(contract_avv_global)
        session.add(contract_sub_global)
        session.add(contract_agb_netzmanager)
        session.commit()
        session.refresh(contract_agb_azd)
        session.refresh(contract_avv_global)
        session.refresh(contract_sub_global)
        session.refresh(contract_agb_netzmanager)

        product_contract_agb_azd = ProductContract(
            product_uuid=product_azd.uuid, contract_uuid=contract_agb_azd.uuid
        )

        product_contract_avv_global = ProductContract(
            product_uuid=product_azd.uuid, contract_uuid=contract_avv_global.uuid
        )

        product_contract_sub_gloabl = ProductContract(
            product_uuid=product_azd.uuid, contract_uuid=contract_sub_global.uuid
        )

        product_contract_agb_netzmanager = ProductContract(
            product_uuid=product_azd.uuid, contract_uuid=contract_agb_netzmanager.uuid
        )

        session.add(product_contract_agb_azd)
        session.add(product_contract_avv_global)
        session.add(product_contract_sub_gloabl)
        session.add(product_contract_agb_netzmanager)
        session.commit()
