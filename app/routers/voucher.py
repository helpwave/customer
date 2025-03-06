from fastapi import APIRouter, Depends, HTTPException

from models.voucher import Voucher, VoucherBase
from utils.database.session import get_database

router = APIRouter(prefix="/voucher", tags=["Voucher"])


@router.get("/{code}", response_model=VoucherBase)
async def valid(code: str, session=Depends(get_database)):
    voucher = session.query(Voucher).filter_by(code=code).first()

    if not voucher:
        raise HTTPException(status_code=404, detail="Voucher not found.")

    return voucher
