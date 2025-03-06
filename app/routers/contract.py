from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models.contract import (
        Contract,
        ContractBase,
)
from utils.database.session import get_database

router = APIRouter(prefix="/contract", tags=["Contract"])


@router.get("/{uuid}", response_model=ContractBase)
async def read(uuid: UUID, session=Depends(get_database)):
    contract = session.query(Contract).filter_by(uuid=uuid).first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found.")

    return contract

@router.get("/", response_model=list[ContractBase])
async def read_all(session=Depends(get_database)):
    return session.query(Contract).all()

 
