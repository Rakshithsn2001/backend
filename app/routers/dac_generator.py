from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import oauth2
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/create_digital_access_code",
    tags=['create']
)


@router.get('/{ph_no}', status_code=status.HTTP_201_CREATED, response_model=schemas.dac_out)
def generate_code(ph_no: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    search_phone_number = db.query(models.Digital_access_code).filter(
        models.Digital_access_code.phone_number == ph_no)
    if search_phone_number.first():
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Already created')

    def generate_digital_access_code():
        while True:
            code = utils.generate_number()
            search_dac_query = db.query(models.Digital_access_code).filter(
                models.Digital_access_code.digital_access_code == code)
            if not search_dac_query.first():
                return code
    data_payload = models.Digital_access_code(
        owner_id=current_user.id, phone_number=ph_no, digital_access_code=generate_digital_access_code())
    try:
        db.add(data_payload)
        db.commit()
        db.refresh(data_payload)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{type(ex).__name__,ex.args},Error')
    return data_payload
